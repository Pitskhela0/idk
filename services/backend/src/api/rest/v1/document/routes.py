from fastapi import APIRouter, Depends, Path, Query
from src.api.rest.v1.paths import (
    DOWNLOAD as DOWNLOAD_PATH,
    SEND_EMAIL as SEND_EMAIL_PATH,
    PREVIEW as PREVIEW_PATH,
    SEARCH as SEARCH_PATH
)
from src.apps.documents.services.download_service import DownloadDocumentAPIService
from src.apps.documents.services.email_service import EmailDocumentAPIService
from src.apps.documents.services.preview_service import PreviewDocumentAPIService
from src.apps.documents.services.search_service import SearchDocumentAPIService
from src.apps.documents.dependency import (
    get_download_service,
    get_email_service,
    get_preview_service,
    get_search_service
)
from src.apps.documents.schemas import DownloadIn, DownloadOut, PreviewOut, SearchOut
from src.apps.documents.schemas.email import EmailIn, EmailOut
from src.apps.auth.dependency import require_groups
from src.apps.auth.policies import (
    DOWNLOAD_POLICY,
    EMAIL_POLICY,
    PREVIEW_POLICY,
    SEARCH_POLICY
)

download_router = APIRouter()
email_router = APIRouter()
preview_router = APIRouter()
search_router = APIRouter()


@download_router.post(DOWNLOAD_PATH, response_model=DownloadOut)
async def download_documents(
        request: DownloadIn,
        group_claims: dict = require_groups(*DOWNLOAD_POLICY['groups']),
        service: DownloadDocumentAPIService = Depends(get_download_service)
):
    return await service.download(request.document_ids)


@email_router.post(SEND_EMAIL_PATH, response_model=EmailOut)
async def send_email(
        request: EmailIn,
        group_claims: dict = Depends(require_groups(*EMAIL_POLICY['groups'])),
        service: EmailDocumentAPIService = Depends(get_email_service)
):
    return await service.prepare_and_send(request.document_ids, request.email)


@preview_router.get(PREVIEW_PATH, response_model=PreviewOut)
async def preview_document(
        id: str = Path(..., description="Document ID to preview"),
        group_claims: dict = require_groups(*PREVIEW_POLICY['groups']),
        service: PreviewDocumentAPIService = Depends(get_preview_service)
):
    return await service.preview(id)


@search_router.get(SEARCH_PATH, response_model=SearchOut)
async def search_documents(
        part_numbers: list[int] = Query(...),
        group_claims: dict = require_groups(*SEARCH_POLICY['groups']),
        service: SearchDocumentAPIService = Depends(get_search_service)
):
    return await service.search(part_numbers)
