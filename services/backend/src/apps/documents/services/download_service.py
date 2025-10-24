import logging

from src.apps.documents.dto import DownloadResultDTO
from src.apps.documents.services.base_service import DocumentAPIService
from src.apps.documents.utils.content_generator import ContentGenerator

logger = logging.getLogger(__name__)


class DownloadDocumentAPIService(DocumentAPIService):

    async def download(self, document_ids: list[str]) -> DownloadResultDTO:
        logger.info("Downloading %d documents", len(document_ids))

        documents_content = await ContentGenerator.content_response(self.document_client, document_ids)

        if documents_content is None:
            logger.warning("All %d documents failed to download", len(document_ids))
            return DownloadResultDTO(
                file_name="",
                content_bytes=b"",
            )

        file_name, file_content, failed_ids = documents_content

        if failed_ids:
            logger.warning(
                "Partial download failure: %d/%d documents failed. Failed IDs: %s",
                len(failed_ids),
                len(document_ids),
                failed_ids
            )

        return DownloadResultDTO(
            file_name=file_name,
            content_bytes=file_content
        )
