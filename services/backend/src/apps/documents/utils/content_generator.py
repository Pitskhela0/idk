import asyncio
from typing import Optional
from datetime import datetime, UTC
from src.apps.documents.utils.zip_generator import ZipGenerator
from src.apps.documents.client import DocumentClient


class ContentGenerator:
    @staticmethod
    async def fetch_single_document(client, document_id: str) -> tuple[str, Optional[bytes]]:
        try:
            content = await client.get_document_content(document_id)
            return document_id, content
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error("Error fetching document %s: %s", document_id, str(e))
            return document_id, None

    @staticmethod
    async def content_response(client: DocumentClient, document_ids: list[str]):
        tasks = [ContentGenerator.fetch_single_document(client, doc_id) for doc_id in document_ids]
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
                doc_id, content = next(iter(found_files.items()))
                file_name = f"document_{doc_id}.pdf"  # todo: implement naming functionality
                file_content = content
            else:
                file_name = f"{timestamp}.zip"  # todo: implement naming functionality
                file_content = ZipGenerator.create_zip_archive(found_files)
            return (
                file_name, file_content, failed_ids
            )

        return None
