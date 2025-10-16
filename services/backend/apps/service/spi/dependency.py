from functools import lru_cache
from apps.service.spi.client import SPIClient
from apps.config import config


@lru_cache
def get_spi_client() -> SPIClient:
    """
    Creating singleton, used for dependency injection
    """
    return SPIClient(
        base_url=config.spi_base_url,
        username=config.spi_username,
        password=config.spi_password,
        timeout=config.spi_timeout_seconds  # max waiting time for spi response
    )
