from fastapi import APIRouter
from models.schemas import HealthResponse
from core.config import get_settings

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    settings = get_settings()
    return HealthResponse(
        status="healthy",
        environment=settings.environment,
        vector_store=settings.vector_store_type
    )