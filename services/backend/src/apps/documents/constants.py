MIN_PART_NUMBERS = 1
MAX_PART_NUMBERS = 10

DEFAULT_TIMEOUT_SECONDS = 30

MIN_DOCUMENT_IDS = 1
MAX_DOCUMENT_IDS = 10
MIN_DOCUMENT_ID_LENGTH = 1


class APIEndpoints:
    SEARCH = "/api/v1/documents/search/"
    GET = "/api/v1/documents/get/"


class DownloadDocumentName:
    ZIP_NAME = "documents.zip"
    SINGLE_DOCUMENT_NAME = "document_{}.pdf"


class PreviewDocumentName:
    DOCUMENT_NAME = "preview_{}.pdf"
