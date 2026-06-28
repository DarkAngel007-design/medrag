"""Application service orchestrating the complete RAG pipeline."""

from __future__ import annotations

from medrag.application.dto.generation import (
    GenerationRequest,
    GenerationResponse,
    RetrievedContext,
)
from medrag.application.services.generation_service import (
    GenerationService,
)
from medrag.application.services.hybrid_retrieval_service import (
    HybridRetrievalService,
)
from medrag.domain.value_objects.retrieved_chunk import (
    RetrievedChunk,
)
from medrag.domain.value_objects.search_query import (
    SearchQuery,
)


class RAGService:
    """Coordinates retrieval and answer generation."""

    def __init__(
        self,
        hybrid_retrieval_service: HybridRetrievalService,
        generation_service: GenerationService,
    ) -> None:
        """Initialize the RAG service."""

        if hybrid_retrieval_service is None:
            raise ValueError("retrieval_service cannot be None")

        if generation_service is None:
            raise ValueError("generation_service cannot be None")

        self._hybrid_retrieval_service = hybrid_retrieval_service
        self._generation_service = generation_service

    async def generate(
        self,
        question: str,
    ) -> GenerationResponse:
        """Generate a grounded answer using retrieval-augmented generation."""

        search_query = SearchQuery(
            query=question,
        )

        retrieved_chunks = await self._hybrid_retrieval_service.retrieve(
            search_query,
        )

        contexts = self._to_retrieved_contexts(
            retrieved_chunks,
        )

        generation_request = GenerationRequest(
            question=question,
            contexts=contexts,
        )

        return await self._generation_service.generate_answer(
            generation_request,
        )

    @staticmethod
    def _to_retrieved_contexts(
        retrieved_chunks: list[RetrievedChunk],
    ) -> list[RetrievedContext]:
        """Convert retrieved chunks into generation contexts."""

        return [
            RetrievedContext(
                chunk_id=item.chunk.id,
                document_id=item.chunk.document_id,
                content=item.chunk.text,
                score=item.score,
                metadata=item.chunk.metadata,
            )
            for item in retrieved_chunks
        ]
