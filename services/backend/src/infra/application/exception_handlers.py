import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.config import AppConfig
from src.infra.application.exception import (
    AppError,
    UnauthorizedError,
    ForbiddenError,
    NotFoundError,
)
from src.apps.documents.exceptions import (
    DocumentError,
    DocumentConnectionError,
    DocumentTimeoutError,
    DocumentAuthenticationError,
    DownloadDocumentNotFound,
    PreviewDocumentNotFound,
)

logger = logging.getLogger(__name__)


async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Handles Pydantic / FastAPI validation errors (input data issues).
    """
    logger.warning("Validation error at %s: %s", request.url.path, exc.errors())
    errors = [{"message": error["msg"]} for error in exc.errors()]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"errors": errors},
    )


async def authorization_error_handler(request: Request, exc: AppError) -> JSONResponse:
    """
    Handles all authorization-related errors (401, 403, or external auth failures).
    """
    logger.warning("Authorization error at %s: %s", request.url.path, exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={"errors": [{"message": exc.detail}]},
    )


async def not_found_error_handler(request: Request, exc: AppError | StarletteHTTPException) -> JSONResponse:
    """
    Handles not-found errors for any resource or document.
    """
    logger.info("Resource not found at %s", request.url.path)
    message = getattr(exc, "detail", "Resource not found")
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"errors": [{"message": message}]},
    )


async def upstream_error_handler(request: Request, exc: DocumentError) -> JSONResponse:
    """
    Handles upstream / document service issues like timeouts or connection errors.
    """
    if isinstance(exc, DocumentTimeoutError):
        code = status.HTTP_504_GATEWAY_TIMEOUT
    else:
        code = status.HTTP_502_BAD_GATEWAY

    logger.error("Upstream document error at %s: %s", request.url.path, exc.default_detail)
    return JSONResponse(
        status_code=code,
        content={"errors": [{"message": exc.default_detail}]},
    )


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    """
    Handles general application-level errors (expected business logic issues).
    """
    logger.warning("AppError at %s: %s", request.url.path, exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={"errors": [{"message": exc.detail}]},
    )


async def internal_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handles all uncaught / unexpected exceptions.
    """
    logger.exception("Unhandled internal error at %s: %s", request.url.path, str(exc))
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"errors": [{"message": "Internal server error"}]},
    )


def register_exception_handlers(app: FastAPI, config: AppConfig) -> None:

    # Validation
    app.add_exception_handler(RequestValidationError, validation_error_handler)  # type: ignore[arg-type]

    # Authorization (401 / 403)
    app.add_exception_handler(UnauthorizedError, authorization_error_handler)  # type: ignore[arg-type]
    app.add_exception_handler(ForbiddenError, authorization_error_handler)  # type: ignore[arg-type]
    app.add_exception_handler(DocumentAuthenticationError, authorization_error_handler)  # type: ignore[arg-type]

    # Not Found (404)
    app.add_exception_handler(NotFoundError, not_found_error_handler)  # type: ignore[arg-type]
    app.add_exception_handler(DownloadDocumentNotFound, not_found_error_handler)  # type: ignore[arg-type]
    app.add_exception_handler(PreviewDocumentNotFound, not_found_error_handler)  # type: ignore[arg-type]
    app.add_exception_handler(StarletteHTTPException, not_found_error_handler)  # type: ignore[arg-type]

    # Upstream / service communication (502 / 504)
    app.add_exception_handler(DocumentConnectionError, upstream_error_handler)  # type: ignore[arg-type]
    app.add_exception_handler(DocumentTimeoutError, upstream_error_handler)  # type: ignore[arg-type]

    # Application / domain
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]

    # Internal (catch-all)
    app.add_exception_handler(Exception, internal_error_handler)  # type: ignore[arg-type]
