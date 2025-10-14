import logging
from typing import Literal

from pydantic import AnyHttpUrl, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL

from src.config.environment import Environment

logger = logging.getLogger(__name__)

# Define supported backend auth types
BackendAuthType = Literal["basic", "bearer", "oauth2", "api_key"]


class AppConfig(BaseSettings):
    """
    Application configuration loaded from environment variables.

    This config supports:
    - Generic backend service communication (SPI/SAP/etc.)
    - Azure AD authentication (SSO)
    - Microsoft Graph API (email sending)
    - CORS, logging, tracing, and other middleware settings
    """

    model_config = SettingsConfigDict(env_prefix="")

    app_name: str
    app_host: AnyHttpUrl
    app_version: str = "0.0.1"
    environment: Environment = Environment.LOCAL
    debug: bool = environment.is_debug

    openapi_url: str = "/openapi.json"
    docs_url: str = "/docs"

    log_level: str = "info"
    log_format: str = "%(asctime)s %(levelname)s %(trace_id)s: %(message)s"
    log_buffer_size: int = 1024
    log_flush_interval: float = 0.5

    cors_origins: list[AnyHttpUrl] = Field(default_factory=list)
    cors_methods: list[str] = Field(default_factory=lambda: ["*"])
    cors_headers: list[str] = Field(default_factory=lambda: ["*"])

    trace_header_name: str = "x-trace-id"

    sentry_dsn: URL | None = None
    sentry_debug_path: str | None = None

    @field_validator("sentry_dsn", mode="before")
    def coerce_sentry_dsn_to_yarl_url(cls, value: str | None) -> URL | None:
        return URL(value) if value else None

    backend_service_base_url: str
    backend_service_auth_type: BackendAuthType = "basic"

    # Common authentication fields
    backend_service_username: str | None = None
    backend_service_password: str | None = None

    # OAuth2 specific fields
    backend_service_token_url: str | None = None
    backend_service_client_id: str | None = None
    backend_service_client_secret: str | None = None

    # API Key specific fields
    backend_service_api_key: str | None = None
    backend_service_api_key_header: str = "X-API-Key"

    # Connection settings
    backend_service_timeout_seconds: int = 30
    backend_service_max_retries: int = 3

    @field_validator("backend_service_base_url", mode="before")
    def validate_backend_url(cls, value: str) -> str:
        """Ensure backend URL doesn't have trailing slash"""
        return value.rstrip('/') if value else value

    @field_validator("backend_service_auth_type")
    def validate_backend_auth_credentials(cls, value: str, info) -> str:
        """Ensure required credentials exist for chosen auth type"""
        values = info.data

        if value == "basic":
            if not values.get("backend_service_username") or not values.get("backend_service_password"):
                raise ValueError(
                    "basic auth requires backend_service_username and backend_service_password"
                )

        elif value == "oauth2":
            required = [
                "backend_service_token_url",
                "backend_service_client_id",
                "backend_service_client_secret"
            ]
            missing = [f for f in required if not values.get(f)]
            if missing:
                raise ValueError(f"oauth2 auth requires: {', '.join(missing)}")

        elif value == "api_key":
            if not values.get("backend_service_api_key"):
                raise ValueError("api_key auth requires backend_service_api_key")

        elif value == "bearer":
            if not values.get("backend_service_api_key"):
                raise ValueError("bearer auth requires backend_service_api_key")

        return value

    # azure entra
    azure_tenant_id: str
    azure_client_id: str
    azure_jwks_url: str

    graph_tenant_id: str
    graph_client_id: str
    graph_client_secret: str | None = None

    # Optional: Certificate-based authentication (more secure for production)
    graph_client_certificate_path: str | None = None
    graph_client_certificate_thumbprint: str | None = None

    # Email configuration
    graph_sender_mailbox: str = "drawinglocator@tennantco.com"
    graph_save_to_sent_items: bool = True
    graph_timeout_seconds: int = 30

    @property
    def graph_authority_url(self) -> str:
        """Microsoft login authority URL for Graph API"""
        return f"https://login.microsoftonline.com/{self.graph_tenant_id}"

    @property
    def graph_scope(self) -> list[str]:
        """Graph API scope for application permissions"""
        return ["https://graph.microsoft.com/.default"]

    @property
    def graph_api_base_url(self) -> str:
        """Microsoft Graph API base URL"""
        return "https://graph.microsoft.com/v1.0"

    @field_validator("graph_client_secret")
    def validate_graph_auth(cls, value: str | None, info) -> str | None:
        """Ensure either client secret or certificate is provided for Graph API"""
        values = info.data

        has_secret = bool(value)
        has_cert = bool(values.get("graph_client_certificate_path"))

        if not has_secret and not has_cert:
            raise ValueError(
                "Must provide either graph_client_secret or "
                "graph_client_certificate_path for Graph API authentication"
            )

        return value

    max_email_size_mb: int = 50
    max_files_per_email: int = 20
    max_materials_per_search: int = 50

    # smtp_host: str | None = None
    # smtp_port: int = 587
    # smtp_username: str | None = None
    # smtp_password: str | None = None
    # smtp_from_email: str | None = None
    # smtp_use_tls: bool = True

    def get_config_copy_with_masked_passwords(self) -> dict:
        """
        Return configuration dictionary with sensitive values masked.
        Safe for logging and debugging.
        """
        config_dict = self.model_dump()

        # List of sensitive fields to mask
        sensitive_fields = [
            'backend_service_password',
            'backend_service_client_secret',
            'backend_service_api_key',
            'graph_client_secret',
        ]

        # Mask sensitive values
        for field in sensitive_fields:
            if field in config_dict and config_dict[field]:
                config_dict[field] = '***'

        # Mask URLs with passwords (if using yarl.URL)
        if isinstance(config_dict.get('sentry_dsn'), URL):
            config_dict['sentry_dsn'] = str(config_dict['sentry_dsn'].with_password('***'))

        return config_dict

    def __repr__(self) -> str:
        """Safe string representation with masked passwords"""
        masked = self.get_config_copy_with_masked_passwords()
        return f"AppConfig({masked})"
