from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db_session
from app.core.exceptions import AppException
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import AuthResponse, LoginRequest, RefreshTokenRequest, SignupRequest, TokenPair
from app.schemas.base import APIResponse
from app.schemas.user import UserRead
from app.services.auth_service import AuthService
from app.services.security import create_access_token, decode_token
from app.utils.responses import success_response

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=APIResponse[AuthResponse], status_code=status.HTTP_201_CREATED)
async def signup(payload: SignupRequest, db: Session = Depends(get_db_session)) -> APIResponse[AuthResponse]:
    user, tokens = AuthService(db).signup(payload)
    return success_response(
        data=AuthResponse(tokens=tokens, user=UserRead.model_validate(user)),
        message="Signup successful.",
    )


@router.post("/login", response_model=APIResponse[AuthResponse])
async def login(payload: LoginRequest, db: Session = Depends(get_db_session)) -> APIResponse[AuthResponse]:
    user, tokens = AuthService(db).login(payload)
    return success_response(
        data=AuthResponse(tokens=tokens, user=UserRead.model_validate(user)),
        message="Login successful.",
    )


@router.post("/refresh", response_model=APIResponse[TokenPair])
async def refresh_token(
    payload: RefreshTokenRequest,
    db: Session = Depends(get_db_session),
) -> APIResponse[TokenPair]:
    token_payload = decode_token(payload.refresh_token)
    if not token_payload or token_payload.get("type") != "refresh":
        raise AppException(
            message="Invalid refresh token.",
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="invalid_refresh_token",
        )

    user = UserRepository(db).get_by_id(str(token_payload.get("sub")))
    if not user or not user.is_active:
        raise AppException(
            message="Invalid refresh token.",
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="invalid_refresh_token",
        )

    tokens = TokenPair(
        access_token=create_access_token(user.id),
        refresh_token=payload.refresh_token,
    )
    return success_response(data=tokens, message="Token refreshed.")


@router.post("/logout", response_model=APIResponse[None])
async def logout(current_user: User = Depends(get_current_user)) -> APIResponse[None]:
    return success_response(data=None, message="Logout successful.")


@router.get("/me", response_model=APIResponse[UserRead])
async def me(current_user: User = Depends(get_current_user)) -> APIResponse[UserRead]:
    return success_response(data=UserRead.model_validate(current_user), message="Current user loaded.")

