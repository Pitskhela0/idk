class DTOConstants:
    MIN_PART_NUMBERS = 1
    MAX_PART_NUMBERS = 10

    DESC_DOCUMENT_ID = "Internal document identifier (UUID or numeric)"
    DESC_PART_NUMBER = "Part number identifying the document type"
    DESC_REVISION = "Document revision (e.g., 'A', '-B')"
    DESC_DATE_CREATED = "Document creation timestamp"
    DESC_FILE_SIZE = "File size in bytes"
    DESC_FILE_NAME = "Original file name"

    DESC_PART_NUMBERS_LIST = "List of part numbers to search (minimum 1, maximum 10)"
    DESC_FOUND_DOCUMENTS = "List of found documents"
    DESC_NOT_FOUND_PART_NUMBERS = "Part numbers that were not found in the system"

    DESC_DOWNLOAD_IDS = "Internal document identifiers to download"
    DESC_DOWNLOAD_FILE_NAME = "Name of the downloaded file"
    DESC_DOWNLOAD_CONTENT = "Raw binary file content"

    DESC_PREVIEW_CONTENT = "Raw binary file content for preview"


class APIEndpoints:
    """SAP CPI API paths."""
    
    SEARCH = "/api/v1/documents"
    DOWNLOAD = "/api/v1/documents/download"
    PREVIEW = "/api/v1/documents/preview/{document_id}"
