import logging
from typing import Optional
from datetime import datetime, UTC
import base64
import asyncio

from msgraph import GraphServiceClient
from msgraph.generated.users.item.send_mail.send_mail_post_request_body import SendMailPostRequestBody
from msgraph.generated.models.message import Message
from msgraph.generated.models.item_body import ItemBody
from msgraph.generated.models.body_type import BodyType
from msgraph.generated.models.recipient import Recipient
from msgraph.generated.models.email_address import EmailAddress
from msgraph.generated.models.file_attachment import FileAttachment
from azure.identity.aio import ClientSecretCredential

from src.apps.documents.dto import EmailResultDTO, FailedDocumentsDTO
from src.apps.documents.services.base_service import DocumentAPIService
from src.apps.documents.utils import create_zip_archive
from src.config import get_config

logger = logging.getLogger(__name__)


class EmailDocumentAPIService(DocumentAPIService):
    async def _fetch_single_document(self, document_id: str) -> tuple[str, Optional[bytes]]:
        try:
            content = await self.document_client.get_document_content(document_id)
            return document_id, content
        except Exception as e:
            logger.error("Error fetching document %s: %s", document_id, str(e))
            return document_id, None

    async def prepare_and_send(self, document_ids: list[str], email: str) -> EmailResultDTO:
        logger.info("Preparing %d documents for email to %s", len(document_ids), email)

        tasks = [self._fetch_single_document(doc_id) for doc_id in document_ids]
        results = await asyncio.gather(*tasks)

        found_files: dict[str, bytes] = {}
        failed_ids = []

        for doc_id, content in results:
            if content is None:
                failed_ids.append(doc_id)
            else:
                found_files[doc_id] = content

        if found_files:
            timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")

            if len(found_files) == 1:
                doc_id, content = next(iter(found_files.items()))  # convert into iterator and get first element
                file_name = f"document_{doc_id}.pdf"
                file_content = content
            else:
                file_name = f"documents_{timestamp}.zip"
                file_content = create_zip_archive(found_files)

            await self.send_email(email, file_name, file_content)

        return EmailResultDTO(
            failed=FailedDocumentsDTO(document_ids=failed_ids)
        )

    async def send_email(self, email: str, file_name: str, content: bytes) -> None:
        """Send email using Microsoft Graph SDK."""
        config = get_config()

        # todo: add handlers
        credential = ClientSecretCredential(
            tenant_id=config.graph.azure_tenant_id,
            client_id=config.graph.client_id,
            client_secret=config.graph.client_secret
        )

        graph_client = GraphServiceClient(credential)

        content_type = "application/zip" if file_name.endswith(".zip") else "application/pdf"

        request_body = SendMailPostRequestBody(
            message=Message(
                subject="Documents from Drawing Locator",
                body=ItemBody(
                    content_type=BodyType.Text,
                    content=f"Please find attached: {file_name}",
                ),
                to_recipients=[
                    Recipient(
                        email_address=EmailAddress(
                            address=email,
                        ),
                    ),
                ],
                attachments=[
                    FileAttachment(
                        odata_type="#microsoft.graph.fileAttachment",
                        name=file_name,
                        content_type=content_type,
                        content_bytes=content,
                    ),
                ],
            ),
            save_to_sent_items=False,
        )

        await graph_client.users.by_user_id(config.graph.sender_mailbox).send_mail.post(request_body)

        logger.info("Email sent to %s with file %s", email, file_name)

