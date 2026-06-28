from __future__ import annotations

from uuid import UUID

from qdrant_client import AsyncQdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
)

from medrag.application.ports.embedding_provider import (
    EmbeddingProvider,
)
from medrag.application.ports.indexing_service import (
    IndexingService,
)
from medrag.domain.entities.chunk import Chunk
from medrag.domain.repositories.dense_search_repository import (
    DenseSearchRepository,
)
from medrag.domain.value_objects.retrieved_chunk import (
    RetrievedChunk,
)
from medrag.domain.value_objects.search_query import (
    SearchQuery,
)

DEFAULT_COLLECTION_NAME = "medrag_chunks"


class QdrantSearchRepository(
    DenseSearchRepository,
    IndexingService,
):
    """Qdrant-backed search repository."""

    def __init__(
        self,
        client: AsyncQdrantClient,
        embedding_provider: EmbeddingProvider,
        collection_name: str = DEFAULT_COLLECTION_NAME,
    ) -> None:
        self._client = client
        self._embedding_provider = embedding_provider
        self._collection_name = collection_name

    async def initialize(
        self,
    ) -> None:
        """Initialize repository resources."""

        exists = await self._client.collection_exists(
            self._collection_name,
        )

        if exists:
            return

        await self._client.create_collection(
            collection_name=self._collection_name,
            vectors_config=VectorParams(
                size=self._embedding_provider.dimension,
                distance=Distance.COSINE,
            ),
        )

    async def index(
        self,
        chunks: list[Chunk],
    ) -> None:
        """Index chunks for retrieval."""

        if not chunks:
            return

        texts = [chunk.text for chunk in chunks]

        embeddings = await self._embedding_provider.embed(
            texts,
        )

        points: list[PointStruct] = []

        for chunk, embedding in zip(
            chunks,
            embeddings,
            strict=True,
        ):
            points.append(
                PointStruct(
                    id=str(chunk.id),
                    vector=embedding,
                    payload={
                        "chunk_id": str(chunk.id),
                        "document_id": str(
                            chunk.document_id,
                        ),
                        "text": chunk.text,
                        "chunk_index": chunk.chunk_index,
                        "metadata": chunk.metadata,
                    },
                )
            )

        await self._client.upsert(
            collection_name=self._collection_name,
            points=points,
        )

    async def search(
        self,
        query: SearchQuery,
    ) -> list[RetrievedChunk]:
        """Search indexed chunks."""

        query_embedding = (
            await self._embedding_provider.embed(
                [query.query],
            )
        )[0]

        response = await self._client.query_points(
            collection_name=self._collection_name,
            query=query_embedding,
            limit=query.top_k,
        )

        results: list[RetrievedChunk] = []

        for rank, point in enumerate(
            response.points,
            start=1,
        ):
            payload = point.payload

            if payload is None:
                continue

            chunk = Chunk(
                id=UUID(
                    str(payload["chunk_id"]),
                ),
                document_id=UUID(
                    str(payload["document_id"]),
                ),
                text=str(payload["text"]),
                chunk_index=int(
                    payload["chunk_index"],
                ),
                metadata=dict(
                    payload.get(
                        "metadata",
                        {},
                    )
                ),
            )

            results.append(
                RetrievedChunk(
                    chunk=chunk,
                    score=float(point.score),
                    rank=rank,
                )
            )

        return results
