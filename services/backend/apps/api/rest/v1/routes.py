from fastapi import APIRouter

# todo: uncomment when those options will be implemented
# from apps.api.rest.v1.search.routes import search_router
# from apps.api.rest.v1.download.routes import download_router
# from apps.api.rest.v1.email.routes import email_router

api_v1_router = APIRouter()

# todo: uncomment when those options will be implemented
# api_v1_router.include_router(search_router, tags=["Search"], prefix="/search")
# api_v1_router.include_router(download_router, tags=["Download"], prefix="/download")
# api_v1_router.include_router(email_router, tags=["Email"], prefix="/email")
