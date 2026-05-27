from app.schemas.base import APIResponse, DataT


def success_response(data: DataT | None = None, message: str = "OK") -> APIResponse[DataT]:
    return APIResponse(message=message, data=data)

