import httpx
import logging
from typing import Optional

from src.apps.documents.constants import APIEndpoints

logger = logging.getLogger(__name__)


class DocumentClient:
    def __init__(
            self,
            base_url: str,
            username: str,
            password: str,
            timeout: int = 30
    ):
        self.base_url = base_url.rstrip("/")
        self.http_client = httpx.AsyncClient(
            auth=(username, password),
            timeout=httpx.Timeout(timeout),
            follow_redirects=True,
        )

        logger.debug(
            "DocumentClient initialized with base_url=%s, timeout=%s",
            self.base_url,
            timeout
        )

    async def get_document_content(self, document_id: str) -> Optional[bytes]:
        """Fetch document content by ID."""
        url = f"{self.base_url}{APIEndpoints.GET}"
        params = {"id": document_id}

        try:
            response = await self.http_client.get(url, params=params)
            response.raise_for_status()
            return response.content
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                logger.warning("Document not found: %s", document_id)
                return None
            raise

    async def get_document_metadata(self, params: dict) -> httpx.Response:
        """Execute search request for metadata(not content)."""
        url = f"{self.base_url}{APIEndpoints.SEARCH}"
        response = await self.http_client.get(url, params=params)
        response.raise_for_status()
        return response
