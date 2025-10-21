from fastapi import status

from src.infra.application.exception import AppError


class DocumentError(AppError):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR


class DocumentConnectionError(DocumentError):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    def __init__(self, detail: str = "Failed to connect to document service"):
        super().__init__(detail=detail)


class DocumentTimeoutError(DocumentError):
    status_code = status.HTTP_504_GATEWAY_TIMEOUT

    def __init__(self, detail: str = "Document request timed out"):
        super().__init__(detail=detail)


class DocumentAuthenticationError(DocumentError):
    status_code = status.HTTP_401_UNAUTHORIZED

    def __init__(self, detail: str = "Authentication failed to SPI service"):
        super().__init__(detail=detail)


class DocumentSearchError(DocumentError):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, detail: str = "Search operation failed"):
        super().__init__(detail=detail)


class DocumentDownloadError(DocumentError):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, detail: str = "Download operation failed"):
        super().__init__(detail=detail)


class DocumentPreviewError(DocumentError):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, detail: str = "Preview operation failed"):
        super().__init__(detail=detail)


class DocumentFileNotFoundError(DocumentError):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, file_id: str):
        super().__init__(detail=f"Document not found: {file_id}")
