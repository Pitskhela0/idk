import httpx
import logging

from src.apps.documents.constants import APIEndpoints

logger = logging.getLogger(__name__)


class DocumentClient:
    """HTTP client for SAP document API with Basic Auth."""

    def __init__(
            self,
            base_url: str,
            username: str,
            password: str,
            timeout: int
    ):
        self.base_url = base_url.rstrip("/")

        self.http_client = httpx.AsyncClient(
            auth=(username, password),
            timeout=httpx.Timeout(timeout),
            follow_redirects=True,
            limits=httpx.Limits(
                max_connections=300,
                max_keepalive_connections=60
            )
        )

        logger.info(
            "DocumentClient initialized with base_url=%s, timeout=%s",
            self.base_url,
            timeout
        )

    # todo: error handling logic for get method
    async def get_document_content(self, document_id: str) -> bytes | None:
        url = f"{self.base_url}{APIEndpoints.GET}"
        params = {"id": document_id}

        try:
            response = await self.http_client.get(url, params=params)
            response.raise_for_status()

            return response.content
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                logger.warning("document not found: %s", document_id)
                return None
            raise

    async def close(self) -> None:
        await self.http_client.aclose()
        logger.info("DocumentClient closed")
