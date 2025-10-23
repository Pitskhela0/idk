import logging

from src.apps.documents.dto import SearchResultDTO
from src.apps.documents.services.base_service import DocumentAPIService

logger = logging.getLogger(__name__)


class SearchDocumentAPIService(DocumentAPIService):
    async def search(self, part_numbers: list[int]) -> SearchResultDTO:
        response = await self.document_client.get_documents_list(part_numbers)

        # todo: map xml response to dto

        cpi_docs = response.get("data", [])
        found_part_numbers = [doc.get("part_number") for doc in cpi_docs]
        not_found = list(filter(lambda part_number: part_number not in found_part_numbers, part_numbers))

        return SearchResultDTO(
            data=response,
            not_found=not_found
        )
