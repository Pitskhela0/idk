from typing import AsyncGenerator

from fastapi import Depends

from src.apps.documents.client import DocumentClient
from src.apps.documents.services.download_service import DownloadDocumentAPIService

from src.apps.documents.services.search_service import SearchDocumentAPIService
from src.apps.documents.services.email_service import EmailDocumentAPIService

from src.apps.documents.services.preview_service import PreviewDocumentAPIService

from src.config import get_config, AppConfig


async def get_document_client(
        config: AppConfig = Depends(get_config)
) -> AsyncGenerator[DocumentClient, None]:

    client = DocumentClient(
        base_url=config.document_base_url,
        username=config.document_username,
        password=config.document_password,
        timeout=config.document_timeout_seconds
    )
    try:
        yield client
    finally:
        await client.http_client.aclose()


def get_search_service(
        client: DocumentClient = Depends(get_document_client)
) -> SearchDocumentAPIService:
    return SearchDocumentAPIService(client=client)


def get_download_service(
        client: DocumentClient = Depends(get_document_client)
) -> DownloadDocumentAPIService:
    return DownloadDocumentAPIService(client=client)


def get_preview_service(
        client: DocumentClient = Depends(get_document_client)
) -> PreviewDocumentAPIService:
    return PreviewDocumentAPIService(client=client)


def get_email_service(
        client: DocumentClient = Depends(get_document_client)
) -> EmailDocumentAPIService:
    return EmailDocumentAPIService(client=client)
