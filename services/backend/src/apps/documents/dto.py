from datetime import datetime, UTC
from pydantic import BaseModel, Field

from src.apps.documents.constants import (
    MIN_PART_NUMBERS,
    MAX_PART_NUMBERS,
    MIN_DOCUMENT_IDS,
    MAX_DOCUMENT_IDS,
    MIN_DOCUMENT_ID_LENGTH
)


class Document(BaseModel):
    id: str
    part_number: int
    rev: str
    date_created: datetime
    file_size_bytes: int


class SearchRequest(BaseModel):
    part_numbers: list[int] = Field(
        ...,
        min_length=MIN_PART_NUMBERS,
        max_length=MAX_PART_NUMBERS,
    )


class NotFoundInfo(BaseModel):
    part_numbers: list[int] = Field(default_factory=list)


class SearchResponse(BaseModel):
    data: list[Document] = Field(default_factory=list)
    not_found: NotFoundInfo = Field(default_factory=NotFoundInfo)


class DownloadRequest(BaseModel):
    document_ids: list[str] = Field(
        ...,
        min_length=MIN_DOCUMENT_IDS,
        max_length=MAX_DOCUMENT_IDS
    )


class DownloadResponse(BaseModel):
    file_name: str
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class PreviewRequest(BaseModel):
    document_id: str = Field(..., min_length=MIN_DOCUMENT_ID_LENGTH)


class PreviewResponse(BaseModel):
    content_base64: str
