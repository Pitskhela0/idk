from enum import StrEnum


class Role(StrEnum):
    """User roles as defined by the business rules."""

    VIEWER = "Viewer"
    EDITOR = "Editor"
    ADMIN = "Admin"


class Scope(StrEnum):
    """OAuth scopes controlling fine-grained access."""

    DOCUMENT_SEARCH = "Document.Search"
    DOCUMENT_PREVIEW = "Document.Preview"
    DOCUMENT_DOWNLOAD = "Document.Download"
    DOCUMENT_MANAGE = "Document.Manage"
