from fastapi import APIRouter, Depends, Path
from src.api.rest.v1.paths import PREVIEW as PREVIEW_PATH
from src.apps.documents.service import PreviewDocumentAPIService
from src.apps.documents.dependency import get_preview_service
from src.apps.documents.dto import PreviewResponse
from src.apps.auth.dependency import require_groups
from src.apps.auth.policies import PREVIEW_POLICY

preview_router = APIRouter()

@preview_router.get(PREVIEW_PATH, response_model=PreviewResponse)
async def preview_document(
    id: str = Path(..., description="Document ID to preview"),
    group_claims: dict = require_groups(*PREVIEW_POLICY['groups']),
    service: PreviewDocumentAPIService = Depends(get_preview_service)
):
    
    return await service.preview(id)
