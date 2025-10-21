from functools import lru_cache

from src.apps.documents.client import DocumentClient
from src.apps.documents.service import DocumentService
from fastapi import Depends, Request


@lru_cache
def get_document_client(request: Request) -> DocumentClient:
    """Retrieve DocumentClient from FastAPI app state."""

    client = getattr(request.app.state, 'document_client', None)
    if client is None:
        raise RuntimeError("DocumentClient not initialized")
    return client


def get_document_service(client: DocumentClient = Depends(get_document_client)) -> DocumentService:
    return DocumentService(client=client)