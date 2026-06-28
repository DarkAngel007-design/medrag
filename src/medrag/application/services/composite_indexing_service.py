from __future__ import annotations

import asyncio

from medrag.application.ports.indexing_service import (
    IndexingService,
)
from medrag.domain.entities.chunk import Chunk
from medrag.domain.repositories.dense_search_repository import (
    DenseSearchRepository,
)
from medrag.domain.repositories.lexical_search_repository import (
    LexicalSearchRepository,
)


class CompositeIndexingService(IndexingService):
    """Coordinates indexing across multiple search backends."""

    def __init__(
        self,
        dense_search_repository: DenseSearchRepository,
        lexical_search_repository: LexicalSearchRepository,
    ) -> None:
        self._dense = dense_search_repository
        self._lexical = lexical_search_repository

    async def index(
        self,
        chunks: list[Chunk],
    ) -> None:
        """Index chunks into all configured search backends."""

        if not chunks:
            return

        await asyncio.gather(
            self._dense.index(chunks),
            self._lexical.index(chunks),
        )
