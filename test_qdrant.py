import asyncio

from qdrant_client import AsyncQdrantClient


async def test() -> None:
    client = AsyncQdrantClient(
        host="localhost",
        port=6333,
    )

    print(await client.collection_exists("medrag_chunks"))


asyncio.run(test())
