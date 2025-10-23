import logging

from src.apps.documents.client import DocumentClient

logger = logging.getLogger(__name__)


class DocumentAPIService:
    def __init__(self, client: DocumentClient):
        self.document_client = client
        logger.info("DocumentService initialized")
