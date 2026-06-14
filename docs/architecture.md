# Architecture

Paper RAG with Gemini follows a minimal RAG pipeline:

1. FastAPI receives a PDF upload.
2. PyMuPDF extracts text page by page.
3. Text is split into overlapping chunks with page metadata.
4. Gemini embedding API converts chunks into vectors.
5. FAISS stores normalized vectors in memory.
6. A user question is embedded with Gemini.
7. FAISS retrieves the top-k chunks.
8. Retrieved chunks are inserted into a constrained prompt.
9. Gemini generates a concise Japanese answer with page and chunk citations.

The vector store is currently in memory. Persistence is intentionally left as future work.
