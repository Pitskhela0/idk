from fastapi import APIRouter, Depends, Path
from src.apps.documents.service import DocumentService
from src.apps.documents.dto import PreviewRequest, PreviewResponse
from src.apps.auth.dependency import require_groups
from src.apps.auth.policies import PREVIEW_POLICY

preview_router = APIRouter()

@preview_router.get("/preview/{id}", response_model=PreviewResponse)
async def preview_document(
    id: str = Path(..., description="Document ID to preview"),
    group_claims: dict = require_groups(*PREVIEW_POLICY['groups'])
    service: DocumentService = Depends(DocumentService)
):

    request = PreviewRequest(id=id)
    
    return await service.preview(request)
