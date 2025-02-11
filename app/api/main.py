from fastapi import APIRouter

from app.api.v1 import api

api_router = APIRouter(prefix="/api")

api_router.include_router(api.api_router)
