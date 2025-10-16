import logging
from typing import Literal

from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL


_AnyLogLevel = Literal["debug", "info", "warning", "error", "critical"]


logger = logging.getLogger(__name__)


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="")

    app_name: str
    app_host: AnyHttpUrl
    app_version: str = "0.0.1"

    debug: bool = True

    openapi_url: str = "/openapi.json"
    docs_url: str = "/docs"

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

    # Microsoft Graph API Configuration
    graph_client_id: str
    graph_client_secret: str
    graph_sender_mailbox: str = "drawinglocator@tennantco.com"

    # Application Limits
    max_email_size_mb: int = 50

    def get_config_copy_with_masked_passwords(self):
        new_config = {}
        for prop, value in dict(self).items():
            if isinstance(value, URL):
                value = value.with_password("***")
            elif prop in (
                "graph_client_secret",  # add other secrets if needed
            ):
                value = "***"

            new_config[prop] = value

        return type(self)(**new_config)
