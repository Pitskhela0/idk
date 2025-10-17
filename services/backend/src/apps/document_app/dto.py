import base64
from datetime import datetime

from pydantic import BaseModel, Field
from src.apps.document_app.constants import DTOConstants


class Document(BaseModel):
    """
    Document metadata model.

    Represents a document stored in the SPI system with its core attributes.
    Multiple documents can share the same part number but have different revisions.
    """

    id: str = Field(..., description=DTOConstants.DESC_DOCUMENT_ID)
    part_number: int = Field(..., description=DTOConstants.DESC_PART_NUMBER)
    rev: str = Field(..., description=DTOConstants.DESC_REVISION)
    date_created: datetime = Field(..., description=DTOConstants.DESC_DATE_CREATED)
    file_size_bytes: int = Field(..., description=DTOConstants.DESC_FILE_SIZE)


class SearchRequest(BaseModel):
    """
    Request model for searching documents by part numbers.

    Allows searching for up to 10 part numbers in a single request.
    Returns matching documents and lists any part numbers that were not found.
    """

    part_numbers: list[int] = Field(
        ...,
        min_length=DTOConstants.MIN_PART_NUMBERS,
        max_length=DTOConstants.MAX_PART_NUMBERS,
        description=DTOConstants.DESC_PART_NUMBERS_LIST,
    )


class NotFoundInfo(BaseModel):
    part_numbers: list[int]


class SearchResponse(BaseModel):
    """
    Response model for document search results.

    Contains found documents and tracks which part numbers had no matches.
    """

    data: list[Document] = Field(..., description=DTOConstants.DESC_FOUND_DOCUMENTS)
    not_found: NotFoundInfo


class DownloadRequest(BaseModel):
    """
    Request model for downloading a document.

    Uses the internal document ID (not the part number) to identify
    the specific document to download.
    """

    id: list[str] = Field(..., description=DTOConstants.DESC_DOWNLOAD_ID)


class DownloadResponse(BaseModel):
    """
    Response model for document download.

    Contains the document metadata and the file content encoded as base64.
    Use get_binary_content() to decode the content to binary bytes.
    """

    id: str = Field(..., description=DTOConstants.DESC_DOCUMENT_ID)
    part_number: int = Field(..., description=DTOConstants.DESC_PART_NUMBER)
    rev: str = Field(..., description=DTOConstants.DESC_REVISION)
    file_name: str = Field(..., description=DTOConstants.DESC_FILE_NAME)
    content_type: str = Field(..., description=DTOConstants.DESC_CONTENT_TYPE)
    file_size_bytes: int = Field(..., description=DTOConstants.DESC_FILE_SIZE)
    date_created: datetime = Field(..., description=DTOConstants.DESC_DATE_CREATED)
    content: str = Field(..., description=DTOConstants.DESC_BASE64_CONTENT)

    def get_binary_content(self) -> bytes:
        """
        Decode base64 content to binary bytes.

        Returns:
            bytes: Decoded binary file content ready for streaming or saving.
        """
        return base64.b64decode(self.content)


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
    content: str = Field(..., description=DTOConstants.DESC_BASE64_CONTENT)
