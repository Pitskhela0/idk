from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from src.apps.documents.constants import MIN_PART_NUMBERS, MAX_PART_NUMBERS


class Document(BaseModel):
    """Document metadata. Multiple documents can share the same part_number with different revisions."""

    model_config = ConfigDict(from_attributes=True)

    id: str = Field(..., description="Internal document identifier (UUID or numeric)")
    part_number: int = Field(..., description="Part number identifying the document type")
    rev: str = Field(..., description="Document revision (e.g., 'A', '-B')")
    date_created: datetime = Field(..., description="Document creation timestamp")
    file_size_bytes: int = Field(..., description="File size in bytes")


class SearchRequest(BaseModel):
    """Internal service-layer model for search operations."""

    model_config = ConfigDict(from_attributes=True)

    part_numbers: list[int] = Field(
        ...,
        min_length=MIN_PART_NUMBERS,
        max_length=MAX_PART_NUMBERS,
        description="List of part numbers to search (minimum 1, maximum 10)",
    )


class NotFoundInfo(BaseModel):
    """Information about part numbers that were not found."""

    model_config = ConfigDict(from_attributes=True)

    part_numbers: list[int] = Field(
        default_factory=list,
        description="Part numbers that were not found in the system"
    )


class SearchResponse(BaseModel):
    """Response from document search operation."""

    model_config = ConfigDict(from_attributes=True, extra="ignore")

    data: list[Document] = Field(
        default_factory=list,
        description="List of found documents"
    )
    not_found: NotFoundInfo = Field(
        default_factory=NotFoundInfo,
        description="Information about documents not found"
    )


class DownloadRequest(BaseModel):
    """Request to download one or multiple documents."""

    model_config = ConfigDict(from_attributes=True)

    document_ids: list[str] = Field(
        ...,
        min_length=1,
        max_length=50,
        description="List of document IDs to download (1-50 documents)"
    )


class DownloadResponse(BaseModel):
    """Response containing downloaded file(s).

    Raw binary from API. Single file or ZIP.
    API layer transforms this into StreamingResponse.
    """

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    file_name: str = Field(
        ...,
        description="Name of the downloaded file (with extension)"
    )
    content: bytes = Field(
        ...,
        description="Raw binary file content"
    )
    content_type: str = Field(
        default="application/octet-stream",
        description="MIME type of the file"
    )


class PreviewRequest(BaseModel):
    """Request to preview a single document."""

    model_config = ConfigDict(from_attributes=True)

    document_id: str = Field(
        ...,
        min_length=1,
        description="Document ID to preview"
    )


class PreviewResponse(BaseModel):
    """Response containing document preview data."""

    model_config = ConfigDict(from_attributes=True)

    document_id: str = Field(
        ...,
        description="Document ID that was previewed"
    )
    file_name: str = Field(
        ...,
        description="Original file name"
    )
    content_base64: str = Field(
        ...,
        description="Base64 encoded file content for preview"
    )
    content_type: str = Field(
        default="application/pdf",
        description="MIME type of the document"
    )


class ErrorResponse(BaseModel):
    """Standard error response format."""

    model_config = ConfigDict(from_attributes=True)

    detail: str = Field(
        ...,
        description="Error message"
    )
    error_code: Optional[str] = Field(
        None,
        description="Application-specific error code"
    )
