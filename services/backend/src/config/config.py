import logging
from typing import Literal

from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL


_AnyLogLevel = Literal["debug", "info", "warning", "error", "critical"]


logger = logging.getLogger(__name__)


# Microsoft Azure AD Configuration
class AzureConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="AZURE_")

    client_id: str
    tenant_id: str

    @property
    def issuer(self) -> str:
        return f"https://login.microsoftonline.com/{self.tenant_id}/v2.0"

    @property
    def jwks_url(self) -> str:
        return f"{self.issuer}/discovery/v2.0/keys"


# Microsoft Graph API Configuration
class GraphConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="GRAPH_")
    
    client_id: str
    client_secret: str
    sender_mailbox: str = "drawinglocator@tennantco.com"


class SAPCPIConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SAP_CPI_")

    token_obtain_url: AnyHttpUrl
    client_id: str
    client_secret: str


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="")

    azure: AzureConfig = Field(default_factory=AzureConfig) # type: ignore[arg-type]
    graph: GraphConfig = Field(default_factory=GraphConfig) # type: ignore[arg-type]
    sap_cpi: SAPCPIConfig = Field(default_factory=SAPCPIConfig) # type: ignore[arg-type]

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

    # Application Limits
    max_email_size_mb: int = 50

    def get_config_copy_with_masked_passwords(self):
        new_config = {}
        for prop, value in dict(self).items():
            if isinstance(value, URL):
                value = value.with_password("***")
            #
            # if isinstance(value, BaseSettings):
            #     value = value.get_config_copy_with_masked_passwords()

            new_config[prop] = value

        return type(self)(**new_config)
