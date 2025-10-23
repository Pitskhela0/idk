import logging
import httpx

from src.apps.documents.exceptions import (
    DocumentConnectionError,
    DocumentTimeoutError,
    DocumentError,
)

logger = logging.getLogger(__name__)


def handle_http_errors(operation_name: str):
    """
    Converts httpx errors into application-level exceptions.
    """

    def decorator(func):
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)

            except httpx.ConnectError as e:
                logger.error("Connection error during %s: %s", operation_name, e)
                raise DocumentConnectionError()

            except httpx.TimeoutException as e:
                logger.error("Timeout during %s: %s", operation_name, e)
                raise DocumentTimeoutError()

            except httpx.HTTPStatusError as e:
                logger.error(
                    "HTTP error during %s (status=%s)", operation_name, e.response.status_code
                )
                raise DocumentError(f"{operation_name} failed with status {e.response.status_code}")

            except Exception as e:
                logger.exception("Unexpected error during %s: %s", operation_name, e)
                raise DocumentError("Unexpected internal error")

        return wrapper

    return decorator
