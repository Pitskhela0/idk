import logging
from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED
from typing import AsyncIterator, Optional
import base64

from src.apps.documents.client import DocumentClient
from src.apps.documents.constants import APIEndpoints
from src.apps.documents.dto import (
    SearchRequest,
    SearchResponse,
    DownloadRequest,
    PreviewRequest,
)

logger = logging.getLogger(__name__)


class DocumentAPIService:
    """Single service handling all document operations."""

    def __init__(self, client: DocumentClient):
        self.document_client = client
        logger.info("DocumentService initialized")


class DownloadDocumentAPIService(DocumentAPIService):
    pass


class SearchDocumentAPIService(DocumentAPIService):
    async def search(self, part_numbers: list[int]) -> SearchResponse:
        logger.info("Searching for %d part numbers", len(part_numbers))

        url = f"{self.document_client.base_url}{APIEndpoints.SEARCH}"
        params = {"part_numbers": "".join(map(str, part_numbers))}

        response = await self.document_client.search(url, params)

        search_response = SearchResponse(**response.json())
        return search_response


class PreviewDocumentAPIService(DocumentAPIService):
    async def preview(self, document_id: str) -> Optional[str]:
        response = await self.document_client.get_document_content(document_id=document_id)

        if response is None:
            return None

        return base64.b64encode(response).decode('utf-8')
