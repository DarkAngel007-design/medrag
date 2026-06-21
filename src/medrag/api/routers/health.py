from fastapi import APIRouter

from medrag.api.schemas.health import HealthResponse
from medrag.shared.config.settings import settings

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get(
    "",
    response_model=HealthResponse,
    summary="Health Check",
)
async def health_check() -> HealthResponse:
    """
    Application health check.
    """

    return HealthResponse(
        status="healthy",
        application=settings.api.app_name,
        version=settings.api.version,
    )
