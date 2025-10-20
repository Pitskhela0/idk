from src.apps.document_app.client import DocumentClient
import logging
from typing import Any
import httpx
from src.apps.document_app.constants import APIEndpoints
from src.apps.document_app.decorators import handle_http_errors
from src.apps.document_app.dto import (
    SearchRequest,
    SearchResponse,
    DownloadRequest,
    DownloadResponse,
    PreviewRequest,
    PreviewResponse
)

from src.apps.document_app.exceptions import (
    DocumentConnectionError,
    DocumentTimeoutError,
    DocumentAuthenticationError,
    DocumentSearchError,
)

logger = logging.getLogger(__name__)


class DocumentService:
    def __init__(self, client: DocumentClient):
        self.client = client
        logger.info("DocumentService initialized")

    @handle_http_errors("search")
    async def search(self, request: SearchRequest) -> SearchResponse:
        part_numbers_str = ",".join(map(str, request.part_numbers))

        url = f"{self.client.base_url}{APIEndpoints.SEARCH}"

        params = {"part_numbers": part_numbers_str}

        response = await self.client.client.get(url, params=params)

        response.raise_for_status()

        response_data = response.json()

        search_response = self._parse_search_response(response_data)

        logger.info(
            "Search completed: found %d documents, %d part_numbers not found",
            len(search_response.data),
            len(search_response.not_found.part_numbers),
        )

        return search_response

    def _parse_search_response(self, response_data: dict[str, Any]) -> SearchResponse:
        try:
            return SearchResponse(**response_data)
        except Exception as e:
            logger.error("Failed to parse search response: %s", str(e))
            raise DocumentSearchError(
                detail="Invalid response format from document service"
            ) from e

    async def download(self, request: DownloadRequest) -> DownloadResponse:
        pass

    async def preview(self, request: PreviewRequest) -> PreviewResponse:
        pass
