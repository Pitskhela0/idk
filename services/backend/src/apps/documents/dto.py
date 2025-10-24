from datetime import datetime
from pydantic import BaseModel


class DocumentDTO(BaseModel):
    id: str
    part_number: int
    rev: str
    date_created: datetime
    file_size_bytes: int


class SearchResultDTO(BaseModel):
    documents: list[DocumentDTO]
    not_found_part_numbers: list[int]


class DocumentContentDTO(BaseModel):
    content: bytes

    class Config:
        arbitrary_types_allowed = True


class DownloadResultDTO(BaseModel):
    file_name: str
    content_bytes: bytes
    is_single_file: bool

    class Config:
        arbitrary_types_allowed = True


class FailedDocumentsDTO(BaseModel):
    document_ids: list[str] = []


class EmailResultDTO(BaseModel):
    failed: FailedDocumentsDTO = FailedDocumentsDTO()
