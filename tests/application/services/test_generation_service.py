from uuid import uuid4

import pytest

from medrag.application.dto.generation import (
    Citation,
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
            citations=[
                Citation(
                    source_index=1,
                    document_id=uuid4(),
                    chunk_id=uuid4(),
                )
            ],
            model="test-model",
        )


@pytest.mark.asyncio
async def test_generation_service_returns_provider_response():
    service = GenerationService(
        llm_provider=FakeLLMProvider(),
        prompt_builder=FakePromptBuilder(),
    )

    request = GenerationRequest(
        question="What is hypertension?",
        contexts=[
            RetrievedContext(
                chunk_id=uuid4(),
                document_id=uuid4(),
                content="Hypertension is...",
                score=0.95,
            )
        ],
        config=GenerationConfig(),
    )

    response = await service.generate_answer(request)

    assert response.answer == "Test answer"
    assert response.model == "test-model"
