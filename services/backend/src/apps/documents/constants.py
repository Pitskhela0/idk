MIN_PART_NUMBERS = 1
MAX_PART_NUMBERS = 10

DEFAULT_TIMEOUT_SECONDS = 30

MIN_DOCUMENT_IDS = 1
MAX_DOCUMENT_IDS = 10
MIN_DOCUMENT_ID_LENGTH = 1


class APIEndpoints:
    DOCUMENTS_METADATA = "api/v1/documents"
    SINGLE_FULL_DOCUMENT = "api/v1/documents/{document_id}"


ZIP_NAME = "documents.zip"
DOCUMENT_NAME = "document_{}.pdf"


class EmailServiceConsts:
    ZIP_CONTENT = "application/zip"
    PDF_CONTENT = "application/pdf"
    ODATA_FILE_TYPE = "#microsoft.graph.fileAttachment"
    MESSAGE_SUBJECT = "Documents from Drawing Locator"  # should be specified by user
    ATTACHMENT_CONTENT_DESC = "Please find attached: {file_name}"

