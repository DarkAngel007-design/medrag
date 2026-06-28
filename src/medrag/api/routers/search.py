from dependency_injector.wiring import (
    Provide,
    inject,
)
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from medrag.api.schemas.search_request import (
    SearchRequest,
)
from medrag.api.schemas.search_response import (
    SearchResponse,
    SearchResult,
)
from medrag.application.services.hybrid_retrieval_service import (
    HybridRetrievalService,
)
from medrag.domain.value_objects.search_query import (
    SearchQuery,
)
from medrag.shared.di.containers import Container
from medrag.shared.logging import get_logger

logger = get_logger(__name__)


router = APIRouter(
    prefix="/search",
    tags=["Search"],
)


@router.post(
    "",
    response_model=SearchResponse,
    summary="Search Documents",
)
@inject
async def search_documents(
    request: SearchRequest,
    hybrid_retrieval_service: HybridRetrievalService = Depends(
        Provide[Container.hybrid_retrieval_service]
    ),
) -> SearchResponse:
    """Search indexed documents."""

    try:
        query = SearchQuery(
            query=request.query,
            top_k=request.top_k,
        )

        results = await hybrid_retrieval_service.retrieve(
            query,
        )

        return SearchResponse(
            results=[
                SearchResult(
                    chunk_id=result.chunk.id,
                    document_id=result.chunk.document_id,
                    text=result.chunk.text,
                    score=result.score,
                    rank=result.rank,
                )
                for result in results
            ]
        )

    except HTTPException:
        raise

    except Exception as exc:
        logger.exception(
            "Search request failed for query: %s",
            request.query,
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to search documents.",
        ) from exc
