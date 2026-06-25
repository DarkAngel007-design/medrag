from dependency_injector import containers, providers
from qdrant_client import AsyncQdrantClient

from medrag.application.services.generation_service import (
    GenerationService,
)
from medrag.application.services.ingestion_service import (
    IngestionService,
)
from medrag.application.services.rag_service import (
    RAGService,
)
from medrag.application.services.retrieval_service import (
    RetrievalService,
)
from medrag.infrastructure.chunkers.recursive_text_chunker import (
    RecursiveTextChunker,
)
from medrag.infrastructure.embeddings.bge_m3_provider import (
    BGEM3EmbeddingProvider,
)
from medrag.infrastructure.llm.provider import LiteLLMProvider
from medrag.infrastructure.parsers.pymupdf_parser import (
    PyMuPDFDocumentParser,
)
from medrag.infrastructure.prompts.default_prompt_builder import (
    DefaultPromptBuilder,
)
from medrag.infrastructure.repositories.in_memory_document_repository import (
    InMemoryDocumentRepository,
)
from medrag.infrastructure.repositories.qdrant_search_repository import (
    QdrantSearchRepository,
)
from medrag.shared.config.settings import (
    settings as app_settings,
)


class Container(containers.DeclarativeContainer):
    """Dependency Injection container."""

    wiring_config = containers.WiringConfiguration(
        packages=[
            "medrag.api",
        ]
    )

    settings = providers.Object(app_settings)

    qdrant_client = providers.Singleton(
        AsyncQdrantClient,
        url="http://localhost:6333",
        check_compatibility=False,
    )

    embedding_provider = providers.Singleton(
        BGEM3EmbeddingProvider,
    )

    document_parser = providers.Singleton(
        PyMuPDFDocumentParser,
    )

    text_chunker = providers.Singleton(
        RecursiveTextChunker,
    )

    document_repository = providers.Singleton(
        InMemoryDocumentRepository,
    )

    search_repository = providers.Singleton(
        QdrantSearchRepository,
        client=qdrant_client,
        embedding_provider=embedding_provider,
        collection_name=app_settings.vector_db.collection_name,
    )

    indexing_service = search_repository

    ingestion_service = providers.Factory(
        IngestionService,
        document_repository=document_repository,
        document_parser=document_parser,
        text_chunker=text_chunker,
        indexing_service=indexing_service,
    )

    retrieval_service = providers.Factory(
        RetrievalService,
        search_repository=search_repository,
    )

    prompt_builder = providers.Singleton(
        DefaultPromptBuilder,
        template_name=app_settings.prompts.system_template,
    )

    print("Model:", app_settings.llm.model_name)
    print("API key loaded:", app_settings.llm.api_key is not None)

    llm_provider = providers.Singleton(
        LiteLLMProvider,
        settings=providers.Object(app_settings.llm),
    )

    generation_service = providers.Factory(
        GenerationService,
        llm_provider=llm_provider,
        prompt_builder=prompt_builder,
    )

    rag_service = providers.Factory(
        RAGService,
        retrieval_service=retrieval_service,
        generation_service=generation_service,
    )
