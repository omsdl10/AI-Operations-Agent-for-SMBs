from fastapi import status
from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.models.business import Business
from app.models.user import User, UserRole
from app.repositories.business_repository import BusinessRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, SignupRequest, TokenPair
from app.services.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)


class AuthService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.users = UserRepository(db)
        self.businesses = BusinessRepository(db)

    def signup(self, payload: SignupRequest) -> tuple[User, TokenPair]:
        existing_user = self.users.get_by_email(payload.email)
        if existing_user:
            raise AppException(
                message="A user with this email already exists.",
                status_code=status.HTTP_409_CONFLICT,
                code="user_exists",
            )

        business = self.businesses.create(Business(name=payload.business_name))
        user = self.users.create(
            User(
                business_id=business.id,
                email=payload.email.lower(),
                full_name=payload.full_name,
                hashed_password=hash_password(payload.password),
                role=UserRole.owner.value,
            )
        )
        self.db.commit()
        self.db.refresh(user)
        return user, self.create_tokens(user.id)

    def login(self, payload: LoginRequest) -> tuple[User, TokenPair]:
        user = self.users.get_by_email(payload.email)
        if not user or not verify_password(payload.password, user.hashed_password):
            raise AppException(
                message="Invalid email or password.",
                status_code=status.HTTP_401_UNAUTHORIZED,
                code="invalid_credentials",
            )
        if not user.is_active:
            raise AppException(
                message="This user account is inactive.",
                status_code=status.HTTP_403_FORBIDDEN,
                code="inactive_user",
            )
        return user, self.create_tokens(user.id)

    def create_tokens(self, user_id: str) -> TokenPair:
        return TokenPair(
            access_token=create_access_token(user_id),
            refresh_token=create_refresh_token(user_id),
        )

