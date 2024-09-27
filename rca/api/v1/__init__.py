from fastapi import APIRouter

from . import policy, proxy, token, endpoint

api_router = APIRouter()
api_router.include_router(tracing.router, tags=["Tracing"])
