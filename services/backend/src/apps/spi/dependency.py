from functools import lru_cache
from fastapi import Depends

from src.apps.spi.client import SPIClient
from src.apps.spi.service import SPIService
from src.config import config


@lru_cache
def get_spi_client() -> SPIClient:
    """
    Create and return a singleton SPIClient instance.

    Uses lru_cache to ensure only one instance is created and reused
    throughout the application lifecycle. This is the recommended approach
    for dependency injection in FastAPI.

    Returns:
        SPIClient: Configured SPI client instance with connection parameters
                   from application configuration.
    """
    return SPIClient(
        base_url=config.spi_base_url,
        username=config.spi_username,
        password=config.spi_password,
        timeout=config.spi_timeout_seconds
    )


def get_spi_service(client: SPIClient = Depends(get_spi_client)) -> SPIService:
    """
    Create and return an SPIService instance with injected dependencies.

    This function is used as a FastAPI dependency to provide SPIService
    instances to route handlers. The SPIClient is automatically injected
    via FastAPI's dependency injection system.

    Args:
        client (SPIClient): Injected SPIClient instance (provided by get_spi_client).

    Returns:
        SPIService: Service instance ready to perform SPI operations.
    """
    return SPIService(client=client)
