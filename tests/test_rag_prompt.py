from app.rag import build_prompt


def test_prompt_contains_context() -> None:
    prompt = build_prompt(context="retrieved context", question="質問")
    assert "retrieved context" in prompt


def test_prompt_contains_question() -> None:
    prompt = build_prompt(context="context", question="この手法は何ですか？")
    assert "この手法は何ですか？" in prompt


def test_prompt_contains_no_outside_knowledge_constraint() -> None:
    prompt = build_prompt(context="context", question="question")
    assert "Do not use outside knowledge." in prompt
    assert "ONLY the provided context" in prompt


def test_prompt_contains_citation_instruction() -> None:
    prompt = build_prompt(context="context", question="question")
    assert "Cite sources using [page: X, chunk: Y]." in prompt
