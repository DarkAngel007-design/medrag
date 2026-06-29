from abc import ABC, abstractmethod

from medrag.domain.value_objects.retrieved_chunk import RetrievedChunk


class FusionStrategy(ABC):
    """Defines how multiple ranked retrieval results are combined."""

    @abstractmethod
    async def fuse(
        self,
        dense_results: list[RetrievedChunk],
        lexical_results: list[RetrievedChunk],
    ) -> list[RetrievedChunk]:
        """Fuse multiple ranked retrieval results into a single ranked list."""
