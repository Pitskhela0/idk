from functools import lru_cache
from fastapi import Depends

from src.apps.document_app.client import DocumentClient
from src.apps.document_app.service import DocumentService
from src.config import config


@lru_cache
def get_document_client() -> DocumentClient:
    """
    Create and return a singleton DocumentClient instance.

    Uses lru_cache to ensure only one instance is created and reused
    throughout the application lifecycle.

    Returns:
        DocumentClient: Configured document client instance with connection parameters
                        from application configuration.
    """
    return DocumentClient(
        base_url=config.document_base_url,
        username=config.document_username,
        password=config.document_password,
        timeout=config.document_timeout_seconds
    )


def get_document_service(client: DocumentClient = Depends(get_document_client)) -> DocumentService:
    """
    Create and return a DocumentService instance with injected dependencies.

    This function is used as a FastAPI dependency to provide DocumentService
    instances to route handlers.

    Args:
        client (DocumentClient): Injected DocumentClient instance (provided by get_document_client).

    Returns:
        DocumentService: Service instance ready to perform document operations.
    """
    return DocumentService(client=client)
