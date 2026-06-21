from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from medrag.api.routers import health_router
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

    app.state.container = container

    logger.info("Application created successfully.")

    return app
