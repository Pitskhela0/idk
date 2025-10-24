import logging

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
from src.apps.documents.utils.content_generator import ContentGenerator
from src.config import get_config

logger = logging.getLogger(__name__)


class EmailDocumentAPIService(DocumentAPIService):
    async def prepare_and_send(self, document_ids: list[str], email: str) -> EmailResultDTO:
        logger.info("Preparing %d documents for email to %s", len(document_ids), email)

        documents_content = await ContentGenerator.content_response(self.document_client, document_ids)

        if documents_content is not None:
            file_name, file_content, failed_ids = documents_content
            await self.send_email(email, file_name, file_content)
        else:
            failed_ids = document_ids

        return EmailResultDTO(
            failed=FailedDocumentsDTO(document_ids=failed_ids)
        )

    async def send_email(self, email: str, file_name: str, content: bytes) -> None:
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

