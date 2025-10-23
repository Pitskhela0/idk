import httpx
import logging

from src.apps.documents.constants import DEFAULT_TIMEOUT_SECONDS
from src.apps.documents.decorators import handle_http_errors

logger = logging.getLogger(__name__)


class DocumentClient:
    def __init__(
            self,
            base_url: str,
            username: str,
            password: str,
            timeout: int = DEFAULT_TIMEOUT_SECONDS
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

    @handle_http_errors("get")
    async def get(self, url: str, params: dict):
        full_url = f"{self.base_url}{url}"
        response = await self.http_client.get(full_url, params=params)
        response.raise_for_status()
        return response
