from datetime import datetime
from pydantic import BaseModel, Field

from src.apps.documents.constants import MIN_PART_NUMBERS, MAX_PART_NUMBERS


class SearchIn(BaseModel):
    part_numbers: list[int] = Field(
        ...,
        min_length=MIN_PART_NUMBERS,
        max_length=MAX_PART_NUMBERS,
        description="List of part numbers to search for",
    )


class DocumentSchema(BaseModel):
    id: str
    part_number: int
    rev: str
    date_created: datetime
    file_size_bytes: int


class NotFoundInfo(BaseModel):
    part_numbers: list[int] = Field(default_factory=list)


class SearchOut(BaseModel):
    data: list[DocumentSchema] = Field(default_factory=list)
    not_found: NotFoundInfo = Field(default_factory=NotFoundInfo)
