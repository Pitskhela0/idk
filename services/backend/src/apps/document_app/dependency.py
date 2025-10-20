from functools import lru_cache

from src.apps.document_app.client import DocumentClient
from src.apps.document_app.service import DocumentService
from fastapi import Depends, Request


@lru_cache
def get_document_client(request: Request) -> DocumentClient:
    """Get DocumentClient from application state."""

    client = getattr(request.app.state, 'document_client', None)
    if client is None:
        raise RuntimeError("DocumentClient not initialized")
    return client


def get_document_service(client: DocumentClient = Depends(get_document_client)) -> DocumentService:
    """Create and return a DocumentService instance."""
    return DocumentService(client=client)
