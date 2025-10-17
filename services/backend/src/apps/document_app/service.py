from src.apps.document_app.client import DocumentClient

from src.apps.document_app.dto import (
    SearchRequest,
    SearchResponse,
    DownloadRequest,
    DownloadResponse,
    PreviewRequest,
    PreviewResponse
    )


class DocumentService:
    def __init__(self, client: DocumentClient):
        self.client = client

    async def search(self, request: SearchRequest) -> SearchResponse:
        pass

    async def download(self, request: DownloadRequest) -> DownloadResponse:
        pass

    async def preview(self, request: PreviewRequest) -> PreviewResponse:
        pass