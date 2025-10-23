from src.infra.application.exception import AppError


class DocumentError(AppError):
    default_detail = "An unexpected document error occurred"


class DocumentConnectionError(DocumentError):
    default_detail = "Failed to connect to document service"


class DocumentTimeoutError(DocumentError):
    default_detail = "Document request timed out"


class DocumentAuthenticationError(DocumentError):
    default_detail = "Authentication failed to document service"

