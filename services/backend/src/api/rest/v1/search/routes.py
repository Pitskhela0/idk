from fastapi import APIRouter, Depends, Query
from src.apps.documents.service import DocumentService
from src.apps.documents.dto import SearchRequest, SearchResponse
from src.apps.auth.dependency import require_roles, require_scopes
from src.apps.auth.policies import SEARCH_POLICY

search_router = APIRouter()

@search_router.get("/search", response_model=SearchResponse)
async def search_documents(
    part_numbers: list[int] = Query(...),
    role_claims: dict = Depends(require_roles(*SEARCH_POLICY['roles'])),
    scope_claims: dict = Depends(require_scopes(*SEARCH_POLICY['scopes']))
    service: DocumentService = Depends(DocumentService)
):

    request = SearchRequest(part_numbers=part_numbers)
    return await service.search(request)
