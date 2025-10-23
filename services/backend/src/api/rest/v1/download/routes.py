from fastapi import APIRouter, Depends

from src.apps.documents.service import DownloadDocumentAPIService
from src.apps.documents.dependency import get_download_service
from src.apps.documents.dto import DownloadRequest
from src.apps.auth.dependency import require_groups
from src.apps.auth.policies import DOWNLOAD_POLICY

download_router = APIRouter()

@download_router.post("/download")
async def download_documents(
    request: DownloadRequest,
    group_claims: dict = require_groups(*DOWNLOAD_POLICY['groups']),
    service: DownloadDocumentAPIService = Depends(get_download_service)
):

    return await service.download(request.document_ids)
