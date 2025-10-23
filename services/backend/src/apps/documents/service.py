import logging
from typing import Optional
import asyncio

from src.apps.documents.client import DocumentClient
from src.apps.documents.dto import (
    SearchRequest,
    SearchResponse,
    DownloadRequest,
    DownloadResponse,
    PreviewRequest,
    PreviewResponse,
)
from src.apps.documents.utils import create_zip_archive, encode_base64
from src.apps.documents.constants import APIEndpoints, DownloadDocumentName, PreviewDocumentName

logger = logging.getLogger(__name__)


class DocumentAPIService:
    def __init__(self, client: DocumentClient):
        self.document_client = client
        logger.info("DocumentService initialized")


class SearchDocumentAPIService(DocumentAPIService):
    async def search(self, request: SearchRequest) -> SearchResponse:
        logger.info("Searching for %d part numbers", len(request.part_numbers))
        params = {"part_numbers": ",".join(map(str, request.part_numbers))}

        response = await self.document_client.get(url=APIEndpoints.SEARCH, params=params)
        return SearchResponse(**response.json())


class DownloadDocumentAPIService(DocumentAPIService):
    async def _fetch_single_document(self, document_id: str) -> tuple[str, Optional[bytes]]:
        params = {"id": document_id}
        response = await self.document_client.get(url=APIEndpoints.GET, params=params)

        if not response.content or response.status_code >= 400:
            return document_id, None

        return document_id, response.content

    async def download(self, request: DownloadRequest) -> DownloadResponse:
        logger.info("Downloading %d documents", len(request.document_ids))

        tasks = [self._fetch_single_document(doc_id) for doc_id in request.document_ids]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        found_files: dict[str, bytes] = {}
        not_found_ids: list[str] = []

        for result in results:
            if isinstance(result, Exception):
                logger.error("Unexpected error during document fetch: %s", str(result))
                continue

            doc_id, content = result
            if content is None:
                not_found_ids.append(doc_id)
            else:
                found_files[doc_id] = content

        if not found_files:
            logger.warning("No documents found for any of the requested IDs: %s", request.document_ids)
            return DownloadResponse(
                file_name="",
                content="",
                not_found_ids=not_found_ids,
            )

        if len(found_files) == 1:
            doc_id, content = next(iter(found_files.items()))
            return DownloadResponse(
                file_name=DownloadDocumentName.SINGLE_DOCUMENT_NAME.format(doc_id),
                content=encode_base64(content),
                not_found_ids=not_found_ids,
            )

        zip_content = create_zip_archive(found_files)
        return DownloadResponse(
            file_name=DownloadDocumentName.ZIP_NAME,
            content=encode_base64(zip_content),
            not_found_ids=not_found_ids,
        )


class PreviewDocumentAPIService(DocumentAPIService):
    async def preview(self, request: PreviewRequest) -> PreviewResponse:
        params = {"id": request.document_id}
        response = await self.document_client.get(url=APIEndpoints.GET, params=params)

        return PreviewResponse(
            file_name=PreviewDocumentName.DOCUMENT_NAME.format(request.document_id),
            content_base64=encode_base64(response.content),
        )
