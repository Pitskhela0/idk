from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict
from src.apps.documents.constants import DTOConstants


class Document(BaseModel):
    """Document metadata. Multiple documents can share the same part_number with different revisions."""

    id: str = Field(..., description=DTOConstants.DESC_DOCUMENT_ID)
    part_number: int = Field(..., description=DTOConstants.DESC_PART_NUMBER)
    rev: str = Field(..., description=DTOConstants.DESC_REVISION)
    date_created: datetime = Field(..., description=DTOConstants.DESC_DATE_CREATED)
    file_size_bytes: int = Field(..., description=DTOConstants.DESC_FILE_SIZE)


class SearchRequest(BaseModel):
    """Internal service-layer model. API layer receives part_numbers as query params."""

    part_numbers: list[int] = Field(
        ...,
        min_length=DTOConstants.MIN_PART_NUMBERS,
        max_length=DTOConstants.MAX_PART_NUMBERS,
        description=DTOConstants.DESC_PART_NUMBERS_LIST,
    )


class NotFoundInfo(BaseModel):
    part_numbers: list[int] = Field(
        default_factory=list,
        description=DTOConstants.DESC_NOT_FOUND_PART_NUMBERS
    )


class SearchResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    data: list[Document] = Field(..., description=DTOConstants.DESC_FOUND_DOCUMENTS)
    not_found: NotFoundInfo


class DownloadRequest(BaseModel):
    """
    Uses internal document IDs (not part numbers).
    Response: single file for one ID, ZIP for multiple IDs.
    """

    document_ids: list[str] = Field(
        ...,
        min_length=1,
        description=DTOConstants.DESC_DOWNLOAD_IDS
    )


class DownloadResponse(BaseModel):
    """
    Raw binary from CPI API. Single file or ZIP.
    API layer transforms this into StreamingResponse.
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
    id: str = Field(..., description=DTOConstants.DESC_DOCUMENT_ID)


class PreviewResponse(BaseModel):
    file_name: str = Field(..., description=DTOConstants.DESC_FILE_NAME)
    content: bytes = Field(..., description=DTOConstants.DESC_PREVIEW_CONTENT)

    class Config:
        arbitrary_types_allowed = True
