from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from io import BytesIO

from src.apps.documents.service import DocumentService
from src.apps.documents.dto import DownloadRequest
from src.apps.auth.dependency import require_roles, require_scopes
from src.apps.auth.policies import DOWNLOAD_POLICY

download_router = APIRouter()

@download_router.post("/download")
async def download_documents(
    request: DownloadRequest,
    role_claims: dict = Depends(require_roles(*DOWNLOAD_POLICY['roles'])),
    scope_claims: dict = Depends(require_scopes(*DOWNLOAD_POLICY['scopes'])),
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
