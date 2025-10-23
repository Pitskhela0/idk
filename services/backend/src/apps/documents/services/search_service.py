import logging

from src.apps.documents.dto import (
    SearchRequest,
    SearchResponse,
)
from src.apps.documents.services.base_service import DocumentAPIService

logger = logging.getLogger(__name__)


class SearchDocumentAPIService(DocumentAPIService):
    async def search(self, request: SearchRequest) -> SearchResponse:
        logger.info("Searching for %d part numbers", len(request.part_numbers))

        params = {"part_numbers": ",".join(map(str, request.part_numbers))}

        response = await self.document_client.get_documents_list(params)

        # todo: map xml response to dto

        cpi_docs = response.get("data", [])
        found_part_numbers = [doc.get("part_number") for doc in cpi_docs]
        not_found = list(filter(lambda part_number: part_number not in found_part_numbers, request.part_numbers))



        return SearchResponse(
            data=response,
            not_found=not_found
        )
