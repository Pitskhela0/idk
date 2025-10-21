import logging

from src.apps.documents.client import DocumentClient
from src.apps.documents.constants import APIEndpoints
from src.apps.documents.decorators import handle_http_errors
from src.apps.documents.dto import (
    SearchRequest,
    SearchResponse,
    DownloadRequest,
    DownloadResponse,
    PreviewRequest,
    PreviewResponse,
)
from src.apps.documents.exceptions import DocumentFileNotFoundError

logger = logging.getLogger(__name__)


class DocumentService:
    """Business logic layer for SAP document operations."""

    def __init__(self, client: DocumentClient) -> None:
        self.client = client
        logger.info("DocumentService initialized")

    @handle_http_errors("search")
    async def search(self, request: SearchRequest) -> SearchResponse:
        logger.info("Searching for %d part numbers", len(request.part_numbers))

        part_numbers_str = ",".join(map(str, request.part_numbers))
        url = f"{self.client.base_url}{APIEndpoints.SEARCH}"
        params = {"part_numbers": part_numbers_str}

        response = await self.client.client.get(url, params=params)
        response.raise_for_status()

        search_response = SearchResponse(**response.json())

        logger.info(
            "Search completed: found %d documents, %d not found",
            len(search_response.data),
            len(search_response.not_found.part_numbers),
        )

        return search_response

    @handle_http_errors("download")
    async def download(self, request: DownloadRequest) -> DownloadResponse:
        raise NotImplementedError("Download functionality coming soon")

    @handle_http_errors("preview")
    async def preview(self, request: PreviewRequest) -> PreviewResponse:
        logger.info("Previewing document with id=%s", request.id)

        url = f"{self.client.base_url}{APIEndpoints.PREVIEW.format(document_id=request.id)}"
        response = await self.client.client.get(url)

        if response.status_code == 404:
            logger.warning("Document not found: id=%s", request.id)
            raise DocumentFileNotFoundError(file_id=request.id)

        response.raise_for_status()

        preview_response = PreviewResponse(**response.json())

        logger.info(
            "Preview completed: file_name=%s, size=%d bytes",
            preview_response.file_name,
            len(preview_response.content),
        )

        return preview_response
