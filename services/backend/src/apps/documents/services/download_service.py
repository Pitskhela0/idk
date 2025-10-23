import logging
from typing import Optional
from datetime import datetime, UTC

import asyncio

from src.apps.documents.dto import (
    DownloadRequest,
    DownloadResponse,
)
from src.apps.documents.exceptions import DownloadDocumentNotFound
from src.apps.documents.services.base_service import DocumentAPIService
from src.apps.documents.utils import create_zip_archive, encode_base64

logger = logging.getLogger(__name__)


class DownloadDocumentAPIService(DocumentAPIService):
    async def _fetch_single_document(self, document_id: str) -> tuple[str, Optional[bytes]]:
        content = await self.document_client.get_document_content(document_id)

        return document_id, content

    async def download(self, request: DownloadRequest) -> DownloadResponse:
        logger.info("Downloading %d documents", len(request.document_ids))

        tasks = [self._fetch_single_document(doc_id) for doc_id in request.document_ids]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        found_files: dict[str, bytes] = {}

        for result in results:
            if isinstance(result, Exception):
                logger.error("Unexpected error during document fetch: %s", str(result))
                continue

            doc_id, content = result
            found_files[doc_id] = content

        if not found_files:
            logger.warning("No documents found for any of the requested IDs: %s", request.document_ids)
            raise DownloadDocumentNotFound()

        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")  # can be used for name

        if len(found_files) == 1:
            doc_id, content = next(iter(found_files.items()))
            return DownloadResponse(
                file_name="idk.pdf",
                content=encode_base64(content),
                created_at=datetime.now(UTC),
            )

        zip_content = create_zip_archive(found_files)

        return DownloadResponse(
            file_name="idk.zip",
            content=encode_base64(zip_content),
            created_at=datetime.now(UTC),
        )
