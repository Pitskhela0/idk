from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict
from src.apps.document_app.constants import DTOConstants


class Document(BaseModel):
    """
    Document metadata model.

    Represents a document stored in the CPI system with its core attributes.
    Multiple documents can share the same part number but have different revisions.
    """

    id: str = Field(..., description=DTOConstants.DESC_DOCUMENT_ID)
    part_number: int = Field(..., description=DTOConstants.DESC_PART_NUMBER)
    rev: str = Field(..., description=DTOConstants.DESC_REVISION)
    date_created: datetime = Field(..., description=DTOConstants.DESC_DATE_CREATED)
    file_size_bytes: int = Field(..., description=DTOConstants.DESC_FILE_SIZE)


class SearchRequest(BaseModel):
    """
    Internal request model for searching documents by part numbers.

    Note: This is used internally by the service layer.
    The API layer accepts part_numbers as query parameters.
    """

    part_numbers: list[int] = Field(
        ...,
        min_length=DTOConstants.MIN_PART_NUMBERS,
        max_length=DTOConstants.MAX_PART_NUMBERS,
        description=DTOConstants.DESC_PART_NUMBERS_LIST,
    )


class NotFoundInfo(BaseModel):
    """Information about part numbers that were not found."""

    part_numbers: list[int] = Field(
        default_factory=list,
        description=DTOConstants.DESC_NOT_FOUND_PART_NUMBERS
    )


class SearchResponse(BaseModel):
    """
    Response model for document search results.

    Contains found documents and tracks which part numbers had no matches.
    """
    model_config = ConfigDict(extra="ignore")
    data: list[Document] = Field(..., description=DTOConstants.DESC_FOUND_DOCUMENTS)
    not_found: NotFoundInfo


class DownloadRequest(BaseModel):
    """
    Request model for downloading documents.

    Uses POST method with document IDs in request body.
    Uses internal document IDs (not part numbers) to identify specific documents.

    Response behavior:
    - Single document_id: Returns the file directly (PDF, DOCX, etc.)
    - Multiple document_ids: Returns a ZIP file containing all documents
    """

    document_ids: list[str] = Field(
        ...,
        min_length=1,
        description=DTOConstants.DESC_DOWNLOAD_IDS
    )


class DownloadResponse(BaseModel):
    """
    Response model for download operation.

    Document API returns raw binary content:
    - Single file: The actual file content (PDF, DOCX, etc.)
    - Multiple files: ZIP archive containing all requested documents

    This model represents the raw response from document API.
    The API layer transforms this into FastAPI StreamingResponse.
    """

    file_name: str = Field(
        ...,
        description=DTOConstants.DESC_DOWNLOAD_FILE_NAME
    )
    content: bytes = Field(
        ...,
        description=DTOConstants.DESC_DOWNLOAD_CONTENT
    )

    class Config:
        arbitrary_types_allowed = True


class PreviewRequest(BaseModel):
    """
    Request model for previewing a document.
    """

    id: str = Field(..., description=DTOConstants.DESC_DOCUMENT_ID)


class PreviewResponse(BaseModel):
    """
    Response model for previewing a document.
    """

    file_name: str = Field(..., description=DTOConstants.DESC_FILE_NAME)
    content: bytes = Field(..., description=DTOConstants.DESC_PREVIEW_CONTENT)

    class Config:
        arbitrary_types_allowed = True
