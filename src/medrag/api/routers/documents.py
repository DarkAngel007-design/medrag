from dependency_injector.wiring import (
    Provide,
    inject,
)
from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
)

from medrag.api.schemas.upload_response import (
    UploadResponse,
)
from medrag.application.services.ingestion_service import (
    IngestionService,
)
from medrag.shared.di.containers import Container
from medrag.shared.logging import get_logger

logger = get_logger(__name__)


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post(
    "/upload",
    response_model=UploadResponse,
    summary="Upload Document",
)
@inject
async def upload_document(
    file: UploadFile = File(...),
    ingestion_service: IngestionService = Depends(Provide[Container.ingestion_service]),
) -> UploadResponse:
    """Upload and index a document."""

    try:
        content = await file.read()

        result = await ingestion_service.ingest(
            content=content,
            source=file.filename or "uploaded-file",
        )

        return UploadResponse(
            document_id=result.document_id,
            chunk_count=result.chunk_count,
            already_indexed=result.already_indexed,
            message=(
                "Document already indexed."
                if result.already_indexed
                else "Document indexed successfully."
            ),
        )

    except HTTPException:
        raise

    except Exception as exc:
        logger.exception(
            "Failed to ingest document '%s'.",
            file.filename,
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to ingest document.",
        ) from exc
