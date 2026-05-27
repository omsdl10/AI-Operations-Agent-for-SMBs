from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.logging import get_logger
from app.schemas.base import ErrorDetail, ErrorResponse

logger = get_logger(__name__)


class AppException(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        code: str = "app_error",
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.code = code


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    logger.warning("%s %s failed: %s", request.method, request.url.path, exc.message)
    payload = ErrorResponse(
        error=ErrorDetail(code=exc.code, message=exc.message),
    )
    return JSONResponse(status_code=exc.status_code, content=payload.model_dump())


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    logger.warning("%s %s validation failed: %s", request.method, request.url.path, exc.errors())
    payload = ErrorResponse(
        error=ErrorDetail(
            code="validation_error",
            message="Request validation failed.",
            details={"errors": exc.errors()},
        ),
    )
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=payload.model_dump())


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("%s %s failed unexpectedly", request.method, request.url.path)
    payload = ErrorResponse(
        error=ErrorDetail(code="internal_server_error", message="An unexpected error occurred."),
    )
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=payload.model_dump())


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)

