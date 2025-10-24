from fastapi import APIRouter, Depends
from src.api.rest.v1.paths import SEND_EMAIL as SEND_EMAIL_PATH
from src.apps.documents.services.email_service import EmailDocumentAPIService
from src.apps.documents.dependency import get_email_service
from src.apps.documents.schemas.email import EmailIn, EmailOut
from src.apps.auth.dependency import require_groups
from src.apps.auth.policies import EMAIL_POLICY

email_router = APIRouter()


@email_router.post(SEND_EMAIL_PATH, response_model=EmailOut)
async def send_email(
        request: EmailIn,
        group_claims: dict = Depends(require_groups(*EMAIL_POLICY['groups'])),
        service: EmailDocumentAPIService = Depends(get_email_service)
):
    return await service.prepare_and_send(request.document_ids, request.email)
