import logging

from src.apps.documents.client import DocumentClient
from src.apps.documents.constants import APIEndpoints
from src.apps.documents.decorators import handle_http_errors
from src.apps.documents.dto import (
    SearchResponse,
    GetResponse,
)

logger = logging.getLogger(__name__)


class DocumentService:
    """Business logic layer for SAP document operations."""

    def __init__(self, client: DocumentClient) -> None:
        self.client = client
        logger.info("DocumentService initialized")

    @handle_http_errors("search")
    async def search(self, part_numbers: list[int]) -> SearchResponse:
        logger.info("Searching for %d part numbers", len(part_numbers))

        url = f"{self.client.base_url}{APIEndpoints.SEARCH}"

        params = {"part_numbers": "".join(map(str, part_numbers))}

        response = await self.client.client.get(url, params=params)

        response.raise_for_status()

        search_response = SearchResponse(**response.json())

        logger.info(
            "Search completed: found %d documents, %d not found",
            len(search_response.data),
            len(search_response.not_found.part_numbers),
        )

        return search_response

    @handle_http_errors("get")
    async def get(self, ids: list[str]) -> GetResponse:
        url = f"{self.client.base_url}{APIEndpoints.GET}"
        response = await self.client.client.get(url, params={"ids": ids})

        response.raise_for_status()

        get_response = GetResponse(**response.json())

        logger.info(
            "Get completed: retrieved %d documents",
            len(get_response.data))

        return get_response
