from google import genai
from google.genai import types

from app.config import get_settings


class EmbeddingClient:
    def __init__(self, batch_size: int = 16, timeout_seconds: int = 60) -> None:
        self.settings = get_settings(require_api_key=True)
        self.client = genai.Client(
            api_key=self.settings.gemini_api_key,
            http_options=types.HttpOptions(timeout=timeout_seconds * 1000),
        )
        self.batch_size = batch_size

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        embeddings: list[list[float]] = []
        for start in range(0, len(texts), self.batch_size):
            batch = texts[start : start + self.batch_size]
            response = self.client.models.embed_content(
                model=self.settings.gemini_embedding_model,
                contents=batch,
                config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT"),
            )
            embeddings.extend([item.values for item in response.embeddings])
        return embeddings

    def embed_query(self, query: str) -> list[float]:
        response = self.client.models.embed_content(
            model=self.settings.gemini_embedding_model,
            contents=query,
            config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY"),
        )
        if not response.embeddings:
            raise RuntimeError("Gemini returned no query embedding.")
        return response.embeddings[0].values
