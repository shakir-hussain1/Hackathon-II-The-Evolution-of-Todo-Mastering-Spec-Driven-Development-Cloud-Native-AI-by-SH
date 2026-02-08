"""Health check routes"""

from fastapi import APIRouter

health_router = APIRouter()

@health_router.get("/health")
async def health():
    return {"status": "healthy"}

@health_router.get("/ready")
async def ready():
    return {"status": "ready"}
