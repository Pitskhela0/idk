from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

from src.apps.documents.constants import (
    MIN_PART_NUMBERS,
    MAX_PART_NUMBERS,
    MIN_DOCUMENT_IDS,
    MAX_DOCUMENT_IDS,
    MIN_DOCUMENT_ID_LENGTH
)


class Document(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    part_number: int
    rev: str
    date_created: datetime
    file_size_bytes: int


class SearchRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    part_numbers: list[int] = Field(
        ...,
        min_length=MIN_PART_NUMBERS,
        max_length=MAX_PART_NUMBERS,
    )


class NotFoundInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    part_numbers: list[int] = Field(default_factory=list)


class SearchResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    data: list[Document] = Field(default_factory=list)
    not_found: NotFoundInfo = Field(default_factory=NotFoundInfo)


class DownloadRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    document_ids: list[str] = Field(
        ...,
        min_length=MIN_DOCUMENT_IDS,
        max_length=MAX_DOCUMENT_IDS
    )


class DownloadResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    file_name: str
    content: str
    not_found_ids: list[str] = Field(default_factory=list)


class PreviewRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    document_id: str = Field(..., min_length=MIN_DOCUMENT_ID_LENGTH)


class PreviewResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    content_base64: str
