import logging
from typing import Literal, Any

from pydantic import AnyHttpUrl, Field
from pydantic_core import Url
from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL


_AnyLogLevel = Literal["debug", "info", "warning", "error", "critical"]


logger = logging.getLogger(__name__)


class EmailConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="EMAIL_")

    sender_mailbox: str = "drawinglocator@tennantco.com"


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

    _email_config: EmailConfig | None = None

    @property
    def sender_mailbox(self) -> str:
        if self._email_config is None:
            self._email_config = EmailConfig() # type: ignore[arg-type]

        return self._email_config.sender_mailbox


class SAPCPIConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SAP_CPI_")

    document_base_url: AnyHttpUrl
    token_obtain_url: AnyHttpUrl
    client_id: str
    client_secret: str


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="")

    email: EmailConfig = Field(default_factory=EmailConfig) # type: ignore[arg-type]
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

    def get_config_copy_with_masked_passwords(self) -> dict[str, Any]:
        """
        Returns a nested dictionary copy of this config:
        - URL passwords are masked with '***'
        - Nested BaseSettings are recursively converted to dictionaries
        - Lists and dicts are also handled recursively
        """
        def mask_value(value: Any) -> Any:
            if isinstance(value, Url):
                if value.password is not None:
                    return URL(str(value)).with_password("***")

            elif isinstance(value, BaseSettings):
                # recursively process nested BaseSettings
                return {k: mask_value(v) for k, v in value.model_dump().items()}

            elif isinstance(value, list):
                return [mask_value(v) for v in value]

            elif isinstance(value, dict):
                return {k: mask_value(v) for k, v in value.items()}
            return value

        return {k: mask_value(v) for k, v in self.model_dump().items()}
