from fastapi import APIRouter, Depends, Query
from src.apps.documents.service import SearchDocumentAPIService
from src.apps.documents.dependency import get_search_service
from src.apps.documents.dto import SearchResponse
from src.apps.auth.dependency import require_groups
from src.apps.auth.policies import SEARCH_POLICY

search_router = APIRouter()

@search_router.get("/search", response_model=SearchResponse)
async def search_documents(
    part_numbers: list[int] = Query(...),
    group_claims: dict = require_groups(*SEARCH_POLICY['groups']),
    service: SearchDocumentAPIService = Depends(get_search_service)
):

    return await service.search(part_numbers)
