from uuid import uuid4

from medrag.application.dto.generation import (
    GenerationConfig,
    GenerationRequest,
    RetrievedContext,
)
from medrag.infrastructure.prompts.default_prompt_builder import (
    DefaultPromptBuilder,
)


def test_prompt_builder_formats_prompt():
    builder = DefaultPromptBuilder()

    request = GenerationRequest(
        question="What is hypertension?",
        contexts=[
            RetrievedContext(
                chunk_id=uuid4(),
                document_id=uuid4(),
                content="Hypertension is elevated blood pressure.",
                score=0.95,
            ),
            RetrievedContext(
                chunk_id=uuid4(),
                document_id=uuid4(),
                content="ACE inhibitors are antihypertensive drugs.",
                score=0.90,
            ),
        ],
        config=GenerationConfig(),
    )

    prompt = builder.build(request)

    assert "Context" in prompt
    assert "Question" in prompt
    assert "Answer" in prompt

    assert "Source [1]" in prompt
    assert "Source [2]" in prompt

    assert "What is hypertension?" in prompt

    assert "Hypertension is elevated blood pressure." in prompt

    assert "ACE inhibitors are antihypertensive drugs." in prompt
