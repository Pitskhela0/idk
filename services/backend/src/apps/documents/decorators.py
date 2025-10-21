"""
Decorators for common service-layer patterns.
"""
import logging
from functools import wraps
from typing import Callable, TypeVar, ParamSpec

import httpx

from src.apps.documents.exceptions import (
    DocumentConnectionError,
    DocumentTimeoutError,
    DocumentAuthenticationError,
    DocumentError,
)

logger = logging.getLogger(__name__)

P = ParamSpec("P")
T = TypeVar("T")


def handle_http_errors(operation_name: str):
    """
    Decorator to handle common HTTP errors for document operations.

    Args:
        operation_name: Name of the operation for logging (e.g., "search", "download")

    Usage:
        @handle_http_errors("search")
        async def search(self, request: SearchRequest) -> SearchResponse:
            ...
    """

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            try:
                return await func(*args, **kwargs)

            except httpx.TimeoutException as e:
                logger.error(
                    "Timeout during %s operation: %s",
                    operation_name,
                    str(e),
                )
                raise DocumentTimeoutError() from e

            except httpx.ConnectError as e:
                logger.error(
                    "Connection error during %s: %s",
                    operation_name,
                    str(e),
                )
                raise DocumentConnectionError() from e

            except httpx.HTTPStatusError as e:
                if e.response.status_code == 401:
                    logger.error(
                        "Authentication failed for %s operation",
                        operation_name,
                    )
                    raise DocumentAuthenticationError() from e

                logger.error(
                    "HTTP error during %s: status=%s",
                    operation_name,
                    e.response.status_code,
                )
                raise DocumentError(
                    detail=f"{operation_name.capitalize()} failed with status {e.response.status_code}"
                ) from e

            except Exception as e:
                logger.exception(
                    "Unexpected error during %s: %s",
                    operation_name,
                    str(e),
                )
                raise DocumentError(
                    detail=f"An unexpected error occurred during {operation_name}"
                ) from e

        return wrapper
    return decorator
