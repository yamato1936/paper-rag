import faiss
import numpy as np


class VectorStore:
    def __init__(self) -> None:
        self.index: faiss.IndexFlatIP | None = None
        self.metadata: list[dict] = []

    def add_chunks(self, document_id: str, chunks: list[dict], embeddings: list[list[float]]) -> None:
        if len(chunks) != len(embeddings):
            raise ValueError("chunks and embeddings must have the same length.")
        if not chunks:
            return

        vectors = self._normalize(np.asarray(embeddings, dtype="float32"))
        if self.index is None:
            self.index = faiss.IndexFlatIP(vectors.shape[1])
        if vectors.shape[1] != self.index.d:
            raise ValueError("embedding dimension does not match existing FAISS index.")

        self.index.add(vectors)
        for chunk in chunks:
            self.metadata.append(
                {
                    "document_id": document_id,
                    "chunk_id": chunk["chunk_id"],
                    "page": chunk["page"],
                    "text": chunk["text"],
                }
            )

    def search(self, query_embedding: list[float], top_k: int = 5) -> list[dict]:
        if self.index is None or not self.metadata:
            return []

        query = self._normalize(np.asarray([query_embedding], dtype="float32"))
        scores, indices = self.index.search(query, min(top_k, len(self.metadata)))

        results: list[dict] = []
        for score, index in zip(scores[0], indices[0]):
            if index < 0:
                continue
            item = self.metadata[int(index)]
            results.append(
                {
                    **item,
                    "score": float(score),
                }
            )
        return results

    @staticmethod
    def _normalize(vectors: np.ndarray) -> np.ndarray:
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        return vectors / norms


vector_store = VectorStore()
