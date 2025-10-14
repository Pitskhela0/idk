import logging
import secrets
from typing import Literal

from pydantic import AnyHttpUrl, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL

from src.config.environment import Environment


_AnyLogLevel = Literal["debug", "info", "warning", "error", "critical"]


logger = logging.getLogger(__name__)


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="")

    app_name: str
    app_host: AnyHttpUrl
    app_version: str = "0.0.1"

    environment: Environment = Environment.LOCAL
    debug: bool = environment.is_debug

    openapi_url: str = "/openapi.json"
    docs_url: str = "/docs"

    secret_key: str = secrets.token_urlsafe(32)

    log_buffer_size: int = 1024
    log_flush_interval: int | float = 0.1
    log_format: str = (
        "%(asctime)s %(levelname)s:%(funcName)s:%(lineno)d %(trace_id)s %(message)s"
    )
    log_level: _AnyLogLevel = "debug" if debug else "info"

    trace_header_name: str = "X-Trace-ID"

    cors_origins: list[AnyHttpUrl] = Field(default_factory=list)
    cors_methods: list[str]
    cors_headers: list[str]

    sentry_dsn: URL | None = None
    sentry_debug_path: str | None = None

    @field_validator("sentry_dsn", mode="before")
    def coerce_sentry_dsn_to_yarl_url(cls, value: str) -> URL | None:  # noqa: N805
        return URL(value) if value else None

    # JWT Configuration
    jwt_exp: int = 5
    jwt_algorithm: str = "HS256"
    jwt_secret: str = secret_key

    # SPI API Configuration
    spi_base_url: str
    spi_username: str
    spi_password: str
    spi_timeout_seconds: int = 30

    # Azure Entra ID Configuration
    azure_tenant_id: str
    azure_client_id: str
    azure_jwks_url: str

    # Microsoft Graph API Configuration
    graph_client_id: str
    graph_client_secret: str
    graph_sender_mailbox: str = "drawinglocator@tennantco.com"

    # Application Limits
    max_email_size_mb: int = 50
    max_files_per_email: int = 20
    max_materials_per_search: int = 50

    # OSS Token Service
    oss_token_service_url: str

    def get_config_copy_with_masked_passwords(self):
        new_config = {}
        for prop, value in dict(self).items():
            if isinstance(value, URL):
                value = value.with_password("***")
            elif prop in (
                "spi_password",
                "graph_client_secret",
                "jwt_secret",
                "secret_key",
            ):
                value = "***"

            new_config[prop] = value

        return type(self)(**new_config)
