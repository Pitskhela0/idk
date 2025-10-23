import logging

from src.apps.documents.dto import DocumentContentDTO
from src.apps.documents.exceptions import PreviewDocumentNotFound
from src.apps.documents.services.base_service import DocumentAPIService
from src.apps.documents.utils import encode_base64

logger = logging.getLogger(__name__)


class PreviewDocumentAPIService(DocumentAPIService):
    async def preview(self, document_id: str) -> DocumentContentDTO:
        raw_byte_content = await self.document_client.get_document_content(document_id)

        if raw_byte_content is None:
            raise PreviewDocumentNotFound()

        return DocumentContentDTO(
            content=encode_base64(raw_byte_content)
        )
