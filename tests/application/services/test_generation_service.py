from uuid import uuid4

import pytest

from medrag.application.dto.generation import (
    GenerationConfig,
    GenerationRequest,
    GenerationResponse,
    RetrievedContext,
)
from medrag.application.services.generation_service import (
    GenerationService,
)


class FakePromptBuilder:
    def build(self, request):
        return "PROMPT"


class FakeLLMProvider:
    async def generate(self, prompt, config):
        return GenerationResponse(
            answer="Test answer",
            citations=[],
            model="test-model",
        )


@pytest.mark.asyncio
async def test_generation_service_returns_provider_response():
    service = GenerationService(
        llm_provider=FakeLLMProvider(),
        prompt_builder=FakePromptBuilder(),
    )

    document_id = uuid4()
    chunk_id = uuid4()

    request = GenerationRequest(
        question="What is hypertension?",
        contexts=[
            RetrievedContext(
                chunk_id=chunk_id,
                document_id=document_id,
                content="Hypertension is...",
                score=0.95,
            )
        ],
        config=GenerationConfig(),
    )

    response = await service.generate_answer(request)

    assert response.answer == "Test answer"
    assert response.model == "test-model"

    assert len(response.citations) == 1

    citation = response.citations[0]

    assert citation.source_index == 1
    assert citation.document_id == document_id
    assert citation.chunk_id == chunk_id
