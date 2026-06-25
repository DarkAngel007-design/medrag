from medrag.infrastructure.prompts.loader import (
    PromptTemplateLoader,
)


def test_system_prompt_loads():
    prompt = PromptTemplateLoader.load(
        "system_prompt.txt",
    )

    assert prompt
    assert "MedRAG" in prompt
