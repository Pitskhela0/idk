from pydantic import BaseModel, Field

from src.apps.documents.constants import MIN_DOCUMENT_ID_LENGTH


class PreviewIn(BaseModel):
    document_id: str = Field(
        ...,
        min_length=MIN_DOCUMENT_ID_LENGTH,
        description="Document ID to preview",
    )


class PreviewOut(BaseModel):
    content_base64: str = Field(..., description="Base64 encoded document content")
