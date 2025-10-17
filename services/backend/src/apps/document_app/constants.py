"""
Constants for document app.

Contains validation limits, field descriptions, and other reusable constants.
"""


class DTOConstants:
    """Constants used in document DTOs."""

    MIN_PART_NUMBERS = 1
    MAX_PART_NUMBERS = 10

    DESC_DOCUMENT_ID = "Internal document identifier (UUID or numeric)"
    DESC_PART_NUMBER = "Part number identifying the document type"
    DESC_REVISION = "Document revision (e.g., 'A', '-B')"
    DESC_DATE_CREATED = "Document creation timestamp"
    DESC_FILE_SIZE = "File size in bytes"

    DESC_PART_NUMBERS_LIST = "List of part numbers to search (minimum 1, maximum 10)"
    DESC_FOUND_DOCUMENTS = "List of found documents"
    DESC_NOT_FOUND_PART_NUMBERS = "Part numbers that were not found in the system"

    DESC_DOWNLOAD_ID = "Internal document identifier to download"
    DESC_FILE_NAME = "Original file name"
    DESC_CONTENT_TYPE = "MIME type (e.g., 'application/pdf')"
    DESC_BASE64_CONTENT = "Base64-encoded file content"
