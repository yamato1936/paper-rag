PROMPT_TEMPLATE = """You are a careful research assistant.
Answer the user's question using ONLY the provided context.
If the answer is not contained in the context, say:
"提供された文脈からは判断できません。"
Rules:
- Do not use outside knowledge.
- Cite sources using [page: X, chunk: Y].
- Keep the answer concise.
- If multiple sources support the answer, cite all relevant sources.
- Do not fabricate numbers, methods, results, or paper claims.
Context:
{context}
Question:
{question}
Answer in Japanese:"""


def build_context(results: list[dict]) -> str:
    blocks = []
    for result in results:
        blocks.append(
            f"[page: {result['page']}, chunk: {result['chunk_id']}]\n{result['text']}"
        )
    return "\n\n---\n\n".join(blocks)


def build_prompt(context: str, question: str) -> str:
    return PROMPT_TEMPLATE.format(context=context, question=question)


def answer_question(question: str, top_k: int = 5) -> dict:
    from app.embeddings import EmbeddingClient
    from app.gemini_client import GeminiClient
    from app.vector_store import vector_store

    embedding_client = EmbeddingClient()
    gemini_client = GeminiClient()

    query_embedding = embedding_client.embed_query(question)
    results = vector_store.search(query_embedding, top_k=top_k)
    context = build_context(results)
    prompt = build_prompt(context=context, question=question)
    answer = gemini_client.generate_answer(prompt)

    return {
        "answer": answer,
        "sources": [
            {
                "document_id": result["document_id"],
                "chunk_id": result["chunk_id"],
                "page": result["page"],
                "score": result["score"],
                "text_preview": result["text"][:240],
            }
            for result in results
        ],
    }
