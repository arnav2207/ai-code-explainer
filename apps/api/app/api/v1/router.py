from fastapi import APIRouter

from app.routes.explain import router as explain_router

api_router = APIRouter()
api_router.include_router(explain_router)
