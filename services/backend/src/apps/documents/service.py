import logging
from typing import Optional
import asyncio

from src.apps.documents.client import DocumentClient
from src.apps.documents.dto import SearchResponse, DownloadResponse
from src.apps.documents.utils import create_zip_archive, encode_base64

logger = logging.getLogger(__name__)


class DocumentAPIService:
    def __init__(self, client: DocumentClient):
        self.document_client = client
        logger.info("DocumentService initialized")


class SearchDocumentAPIService(DocumentAPIService):
    async def search(self, part_numbers: list[int]) -> SearchResponse:
        logger.info("Searching for %d part numbers", len(part_numbers))
        params = {"part_numbers": "".join(map(str, part_numbers))}
        response = await self.document_client.get_documents_metadata(params)
        return SearchResponse(**response.json())


class DownloadDocumentAPIService(DocumentAPIService):
    async def download(self, document_ids: list[str]) -> DownloadResponse:
        logger.info("Downloading %d documents", len(document_ids))

        tasks = [
            self.document_client.get_document_content(doc_id)
            for doc_id in document_ids
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        found_files = {}
        not_found_ids = []

        for doc_id, result in zip(document_ids, results):
            if isinstance(result, Exception) or result is None:
                logger.warning("Document not found or failed: %s", doc_id)
                not_found_ids.append(doc_id)
            else:
                found_files[doc_id] = result

        if not found_files:
            logger.warning("No documents found for any of the requested IDs: %s", document_ids)
            return DownloadResponse(
                file_name="",
                content="",
                not_found_ids=not_found_ids
            )

        if len(found_files) == 1:
            doc_id, content = next(iter(found_files.items()))
            return DownloadResponse(
                file_name=f"document_{doc_id}.pdf",
                content=encode_base64(content),
                not_found_ids=not_found_ids
            )

        zip_content = create_zip_archive(found_files)
        return DownloadResponse(
            file_name="documents.zip",
            content=encode_base64(zip_content),
            not_found_ids=not_found_ids
        )


class PreviewDocumentAPIService(DocumentAPIService):
    async def preview(self, document_id: str) -> Optional[str]:
        response = await self.document_client.get_document_content(document_id)
        if response is None:
            return None
        return encode_base64(response)
