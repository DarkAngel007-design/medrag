"""Generation API endpoints."""

from dependency_injector.wiring import (
    Provide,
    inject,
)
from fastapi import (
    APIRouter,
    Depends,
)

from medrag.api.schemas.generation import GenerateRequest
from medrag.application.dto.generation import GenerationResponse
from medrag.application.services.rag_service import (
    RAGService,
)
from medrag.shared.di.containers import Container

router = APIRouter(
    prefix="/generate",
    tags=["Generation"],
)


@router.post(
    "",
    response_model=GenerationResponse,
    summary="Generate a grounded answer",
)
@inject
async def generate(
    request: GenerateRequest,
    rag_service: RAGService = Depends(
        Provide[Container.rag_service],
    ),
) -> GenerationResponse:
    """
    Generate a citation-aware answer using the complete
    Retrieval-Augmented Generation pipeline.
    """

    return await rag_service.generate(
        question=request.question,
    )
