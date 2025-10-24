from pydantic import BaseModel, Field, field_validator

from src.apps.documents.constants import MIN_DOCUMENT_IDS, MAX_DOCUMENT_IDS


class EmailIn(BaseModel):
    document_ids: list[str] = Field(
        ...,
        min_length=MIN_DOCUMENT_IDS,
        max_length=MAX_DOCUMENT_IDS,
        description="List of document IDs to email",
    )
    email: str = Field(
        ...,
        description="Email address to send documents to (must be @tennantco.com)",
    )

    @field_validator("email")
    def validate_email_domain(cls, v: str) -> str:
        if not v.endswith("@tennantco.com"):
            raise ValueError("Email must be from tennantco.com domain")
        return v


class FailedDocuments(BaseModel):
    document_ids: list[str] = Field(default_factory=list)


class EmailOut(BaseModel):
    failed: FailedDocuments = Field(default_factory=FailedDocuments)