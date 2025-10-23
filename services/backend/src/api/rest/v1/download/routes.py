from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from io import BytesIO

from src.apps.documents.service import DocumentService
from src.apps.documents.dto import DownloadRequest
from src.apps.auth.dependency import require_groups
from src.apps.auth.policies import DOWNLOAD_POLICY

download_router = APIRouter()

@download_router.post("/download")
async def download_documents(
    request: DownloadRequest,
    group_claims: dict = require_groups(*DOWNLOAD_POLICY['groups'])
    service: DocumentService = Depends(DocumentService)
):
    result = await service.download(request)

    return StreamingResponse(
        BytesIO(result.content),
        media_type="application/zip" if result.file_name.endswith(".zip") else "application/octet-stream",
        headers={
            "Content-Disposition": f'attachment; filename="{result.file_name}"'
        },
    )
