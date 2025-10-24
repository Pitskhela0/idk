import logging

from src.apps.documents.dto import DownloadResultDTO
from src.apps.documents.exceptions import DocumentNotFound
from src.apps.documents.services.base_service import DocumentAPIService
from src.apps.documents.utils.content_generator import ContentGenerator

logger = logging.getLogger(__name__)


class DownloadDocumentAPIService(DocumentAPIService):

    async def download(self, document_ids: list[str]) -> DownloadResultDTO:
        logger.info("Downloading %d documents", len(document_ids))

        documents_content = await ContentGenerator.content_response(self.document_client, document_ids)

        if documents_content is None:
            raise DocumentNotFound()

        file_name, file_content, _ = documents_content

        return DownloadResultDTO(
            file_name=file_name,
            content=file_content
        )
