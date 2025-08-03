from fastapi import APIRouter

from endpoints import file_upload, rag, chat, authentication

api_router = APIRouter()

api_router.include_router(rag.router, prefix="/rag", tags=["RAG"])
api_router.include_router(file_upload.router, prefix="/files", tags=["Files"])
api_router.include_router(chat.router, tags=["Chat"])
api_router.include_router(authentication.router, prefix="/auth", tags=["Auth"])