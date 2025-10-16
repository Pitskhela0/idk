import httpx
import logging


logger = logging.getLogger(__name__)


class SPIClient:
    def __init__(self,
                 base_url: str,
                 username: str,
                 password: str,
                 timeout: int = 30,
                 max_retries: int = 30):

        self.base_url = base_url.rstrip("/")
        self.username = username
        self.password = password
        self.timeout = timeout
        self.max_retries = max_retries

        self.client = httpx.AsyncClient(
            auth=(username, password),
            timeout=httpx.Timeout(timeout),
            limits=httpx.Limits(
                max_keepalive_connections=10,
                max_connections=20,
            ),
            follow_redirects=True
        )

        logger.info(
            "SPIClient initialized with base_url=%s, timeout=%s, max_retries=%s",
            self.base_url,
            timeout,
            max_retries
        )





