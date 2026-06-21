from pydantic import Field

from .base import BaseConfig


class VectorDBSettings(BaseConfig):
    """
    Qdrant configuration.
    """

    host: str = Field(default="localhost")

    port: int = Field(default=6333)

    collection_name: str = Field(default="medical_documents")

    grpc_port: int = Field(default=6334)

    prefer_grpc: bool = Field(default=True)
