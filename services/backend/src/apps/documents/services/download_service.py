import logging
from typing import Optional
import asyncio

from src.apps.documents.dto import (
    DownloadRequest,
    DownloadResponse,
)
from src.apps.documents.services.base_service import DocumentAPIService
from src.apps.documents.utils import create_zip_archive, encode_base64

logger = logging.getLogger(__name__)


class DownloadDocumentAPIService(DocumentAPIService):
    async def _fetch_single_document(self, document_id: str) -> tuple[str, Optional[bytes]]:
        response = await self.document_client.get_document_content(document_id)

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
                content=""
            )

        if len(found_files) == 1:
            doc_id, content = next(iter(found_files.items()))
            return DownloadResponse(
                file_name="idk.pdf",
                content=encode_base64(content)
            )

        zip_content = create_zip_archive(found_files)
        return DownloadResponse(
            file_name="idk.zip",
            content=encode_base64(zip_content)
        )
