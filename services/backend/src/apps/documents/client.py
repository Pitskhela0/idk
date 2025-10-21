import httpx
import logging

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

        self.client = httpx.AsyncClient(
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

    async def close(self) -> None:
        await self.client.aclose()
        logger.info("DocumentClient closed")
