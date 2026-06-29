from pydantic import Field

from .base import BaseConfig


class RetrievalSettings(BaseConfig):
    """
    Retrieval pipeline configuration.
    """

    top_k: int = Field(
        default=10,
        ge=1,
    )

    rerank_top_k: int = Field(
        default=5,
        ge=1,
    )

    hybrid_alpha: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
    )

    fusion_k: int = Field(
        default=60,
        ge=1,
    )

    reranker_model: str = Field(
        default="BAAI/bge-reranker-v2-m3",
    )
