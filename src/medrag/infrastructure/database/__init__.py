from sqlalchemy.ext.asyncio import AsyncEngine

from medrag.infrastructure.database.base import Base


async def create_database(
    engine: AsyncEngine,
) -> None:
    """Create database tables."""

    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.create_all,
        )
