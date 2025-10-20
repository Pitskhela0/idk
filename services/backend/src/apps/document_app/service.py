# src/apps/document_app/service.py
"""
Service layer for document operations.

Handles business logic and communication with the CPI API.
"""
import logging

from src.apps.document_app.client import DocumentClient
from src.apps.document_app.constants import APIEndpoints
from src.apps.document_app.decorators import handle_http_errors
from src.apps.document_app.dto import (
    SearchRequest,
    SearchResponse,
    DownloadRequest,
    DownloadResponse,
    PreviewRequest,
    PreviewResponse,
)
from src.apps.document_app.exceptions import DocumentFileNotFoundError

logger = logging.getLogger(__name__)


class DocumentService:
    """
    Service layer for document operations.

    Handles business logic and communication with the CPI API.
    All HTTP errors are handled by the @handle_http_errors decorator.
    """

    def __init__(self, client: DocumentClient) -> None:
        """
        Initialize the service with a document client.

        Args:
            client: Configured DocumentClient instance for API communication.
        """
        self.client = client
        logger.info("DocumentService initialized")

    @handle_http_errors("search")
    async def search(self, request: SearchRequest) -> SearchResponse:
        """
        Search for documents by part numbers.

        Args:
            request: SearchRequest containing part numbers to search.

        Returns:
            SearchResponse: Found documents and list of not found part numbers.
        """
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
        """
        Download documents by their IDs.

        Args:
            request: DownloadRequest containing document IDs.

        Returns:
            DownloadResponse: Downloaded document(s) with content.
        """
        raise NotImplementedError("Download functionality coming soon")

    @handle_http_errors("preview")
    async def preview(self, request: PreviewRequest) -> PreviewResponse:
        """
        Preview a single document.

        Args:
            request: PreviewRequest containing document ID.

        Returns:
            PreviewResponse: Document preview with raw binary content.

        Raises:
            DocumentFileNotFoundError: If document ID doesn't exist.
        """
        logger.info("Previewing document with id=%s", request.id)

        url = f"{self.client.base_url}{APIEndpoints.PREVIEW.format(document_id=request.id)}"
        response = await self.client.client.get(url)

        # Handle 404 specifically before generic error handling
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
