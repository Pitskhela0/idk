import httpx
import logging

logger = logging.getLogger(__name__)


class SPIClient:
    """
    HTTP client for communicating with the SPI (SAP) API.

    Manages the HTTP connection, authentication, and basic configuration
    for making requests to the SPI service.

    Attributes:
        base_url (str): Base URL of the SPI API endpoint.
        client (httpx.AsyncClient): Configured async HTTP client instance.
    """

    def __init__(self,
                 base_url: str,
                 username: str,
                 password: str,
                 timeout: int
                 ):
        """
        Initialize the SPI client with connection parameters.

        Args:
            base_url (str): Base URL of the SPI API (e.g., 'https://spi-api.example.com').
            username (str): Username for basic authentication.
            password (str): Password for basic authentication.
            timeout (int): Request timeout in seconds.
        """

        self.base_url = base_url.rstrip("/")

        self.client = httpx.AsyncClient(
            auth=(username, password),
            timeout=httpx.Timeout(timeout),
            follow_redirects=True
        )

        logger.info(
            "SPIClient initialized with base_url=%s, timeout=%s",
            self.base_url,
            timeout
        )
