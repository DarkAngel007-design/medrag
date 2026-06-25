from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    """Search request payload."""

    query: str = Field(
        min_length=1,
        description="Search query.",
    )

    top_k: int = Field(
        default=10,
        gt=0,
        le=50,
        description="Maximum number of results.",
    )
