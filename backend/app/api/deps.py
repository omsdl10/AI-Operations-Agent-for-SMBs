from collections.abc import Generator

from fastapi import Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.db.session import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.services.security import decode_token

bearer_scheme = HTTPBearer(auto_error=False)


def get_db_session() -> Generator[Session, None, None]:
    yield from get_db()


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db_session),
) -> User:
    if credentials is None:
        raise AppException(
            message="Authentication credentials were not provided.",
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="not_authenticated",
        )

    payload = decode_token(credentials.credentials)
    if not payload or payload.get("type") != "access":
        raise AppException(
            message="Invalid or expired access token.",
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="invalid_access_token",
        )

    user = UserRepository(db).get_by_id(str(payload.get("sub")))
    if not user or not user.is_active:
        raise AppException(
            message="Authenticated user is unavailable.",
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="user_unavailable",
        )
    return user


def require_roles(*allowed_roles: str):
    def dependency(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise AppException(
                message="You do not have permission to perform this action.",
                status_code=status.HTTP_403_FORBIDDEN,
                code="insufficient_permissions",
            )
        return current_user

    return dependency
