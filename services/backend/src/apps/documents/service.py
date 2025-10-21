import logging
import base64
from src.apps.documents.client import DocumentClient
from src.apps.documents.constants import APIEndpoints
from src.apps.documents.decorators import handle_http_errors
from src.apps.documents.dto import (
    SearchResponse,
    GetResponse,
    PreviewResponse,
)

logger = logging.getLogger(__name__)


class DocumentAPIService:
    """Business logic layer for SAP document operations."""

    def __init__(self, client: DocumentClient) -> None:
        self.document_client = client
        logger.info("DocumentAPIService initialized")


class SearchDocumentAPIService(DocumentAPIService):
    async def search(self, part_numbers: list[int]) -> SearchResponse:
        logger.info("Searching for %d part numbers", len(part_numbers))

        url = f"{self.document_client.base_url}{APIEndpoints.SEARCH}"

        params = {"part_numbers": "".join(map(str, part_numbers))}

        response = await self.document_client.http_client.get(url, params=params)

        response.raise_for_status()

        search_response = SearchResponse(**response.json())

        return search_response


class DownloadDocumentAPIService(DocumentAPIService):
    async def download(self, document_ids: list[str]) -> zip | None:
        # todo: send get requests to CPI SAP and with results construct zip
        pass


class PreviewDocumentAPIService(DocumentAPIService):
    async def preview(self, document_id: str) -> str | None:
        response = await self.document_client.get_document_content(document_id=document_id)

        if response is None:
            return None

        return base64.b64encode(response).decode('utf-8')
