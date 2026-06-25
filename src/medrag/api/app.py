from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from medrag.api.routers import (
    documents_router,
    health_router,
    search_router,
)
from medrag.shared.config.settings import settings
from medrag.shared.di import Container
from medrag.shared.logging import configure_logging, get_logger


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Application lifespan.
    """

    logger = get_logger(__name__)

    logger.info("Starting MedRAG...")

    container = app.state.container

    logger.info("Initializing Qdrant collection...")

    search_repository = container.search_repository()

    print(container.settings().vector_db.host)
    print(container.settings().vector_db.port)

    await search_repository.initialize()

    logger.info("Qdrant initialization complete.")

    yield

    logger.info("Shutting down MedRAG...")


def create_app() -> FastAPI:
    """
    Application factory.
    """

    # Configure logging first.
    configure_logging()

    logger = get_logger(__name__)

    logger.info("Creating FastAPI application.")

    container = Container()

    container.wire(
        packages=[
            "medrag.api",
        ]
    )

    app = FastAPI(
        title=settings.api.app_name,
        version=settings.api.version,
        debug=settings.api.debug,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    app.include_router(health_router)
    app.include_router(documents_router)
    app.include_router(search_router)

    app.state.container = container

    logger.info("Application created successfully.")

    return app
