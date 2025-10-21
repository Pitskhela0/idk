from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from src.apps.documents.constants import MIN_PART_NUMBERS, MAX_PART_NUMBERS


class Document(BaseModel):
    """Document metadata. Multiple documents can share the same part_number with different revisions."""

    id: str = Field(..., description="Internal document identifier (UUID or numeric)")
    part_number: int = Field(..., description="Part number identifying the document type")
    rev: str = Field(..., description="Document revision (e.g., 'A', '-B')")
    date_created: datetime = Field(..., description="Document creation timestamp")
    file_size_bytes: int = Field(..., description="File size in bytes")


class SearchRequest(BaseModel):
    """Internal service-layer model. API layer receives part_numbers as query params."""

    part_numbers: list[int] = Field(
        ...,
        min_length=MIN_PART_NUMBERS,
        max_length=MAX_PART_NUMBERS,
        description="List of part numbers to search (minimum 1, maximum 10)",
    )


class NotFoundInfo(BaseModel):
    part_numbers: list[int] = Field(
        default_factory=list,
        description="Part numbers that were not found in the system"
    )


class SearchResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    data: list[Document] = Field(..., description="List of found documents")
    not_found: NotFoundInfo


class DownloadResponse(BaseModel):
    """
    Raw binary from CPI API. Single file or ZIP.
    API layer transforms this into StreamingResponse.
    """

    file_name: str = Field(
        ...,
        description="Name of the downloaded file"
    )
    content: bytes = Field(
        ...,
        description="Raw binary file content"
    )

    class Config:
        arbitrary_types_allowed = True


class GetResponse(BaseModel):
    file_name: str = Field(..., description="Original file name")
    content: bytes = Field(..., description="Raw binary file content for preview")

    class Config:
        arbitrary_types_allowed = True
