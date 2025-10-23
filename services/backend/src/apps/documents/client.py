import httpx
import logging

from src.apps.documents.constants import DEFAULT_TIMEOUT_SECONDS
from src.apps.documents.decorators import handle_http_errors
from src.apps.documents.constants import APIEndpoints


logger = logging.getLogger(__name__)


class DocumentClient:
    def __init__(
            self,
            base_url: str,
            username: str,
            password: str,
            timeout: int = DEFAULT_TIMEOUT_SECONDS
    ):
        self.base_url = base_url if base_url.endswith("/") else base_url + "/"

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
    async def get(self, url: str, params: dict | None = None):
        full_url = f"{self.base_url}{url}"

        # todo: transform request form into odata protocol

        response = await self.http_client.get(full_url, params=params or {})
        response.raise_for_status()
        return response.json()

    async def get_documents_list(self, part_numbers: list[int]):
        params = {"part_numbers": ",".join(map(str, part_numbers))}
        json_response = await self.get(APIEndpoints.DOCUMENTS_METADATA, params)

        return json_response

    async def get_document_content(self, document_id: str):
        url = APIEndpoints.SINGLE_FULL_DOCUMENT.format(document_id=document_id)
        json_response = await self.get(url)

        return json_response.get("content")
