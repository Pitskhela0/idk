from datetime import datetime, UTC
from pydantic import BaseModel, Field

from src.apps.documents.constants import MIN_DOCUMENT_IDS, MAX_DOCUMENT_IDS


class DownloadIn(BaseModel):
    document_ids: list[str] = Field(
        ...,
        min_length=MIN_DOCUMENT_IDS,
        max_length=MAX_DOCUMENT_IDS,
        description="List of document IDs to download",
    )


class DownloadOut(BaseModel):
    file_name: str = Field(..., description="Name of the downloaded file")
    content: str = Field(..., description="Base64 encoded file content")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Timestamp when the download happened",
    )
