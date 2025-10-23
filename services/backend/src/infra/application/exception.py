from typing import Any
from fastapi import HTTPException, status


class AppError(HTTPException):
    status_code: int = status.HTTP_400_BAD_REQUEST
    default_detail: str = "An unexpected error occurred"

    def __init__(
        self,
        detail: Any = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        final_detail = detail or self.default_detail
        super().__init__(
            status_code=self.status_code,
            detail=final_detail,
            headers=headers,
        )


class BadRequestError(AppError):
    default_detail = "Bad request"
    status_code = status.HTTP_400_BAD_REQUEST


class UnauthorizedError(AppError):
    default_detail = "Unauthorized access"
    status_code = status.HTTP_401_UNAUTHORIZED


class ForbiddenError(AppError):
    default_detail = "Forbidden action"
    status_code = status.HTTP_403_FORBIDDEN


class NotFoundError(AppError):
    default_detail = "Resource not found"
    status_code = status.HTTP_404_NOT_FOUND
