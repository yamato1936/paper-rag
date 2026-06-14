import shutil
import uuid
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile

from app.chunker import chunk_pages
from app.config import get_settings
from app.embeddings import EmbeddingClient
from app.pdf_loader import load_pdf
from app.rag import answer_question
from app.schemas import QueryRequest, QueryResponse, UploadResponse
from app.vector_store import vector_store

app = FastAPI(title="paper-rag-gemini")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/documents/upload", response_model=UploadResponse)
def upload_document(file: UploadFile = File(...)) -> UploadResponse:
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Uploaded file must have a .pdf extension.")
    if file.content_type and file.content_type not in {"application/pdf", "application/octet-stream"}:
        raise HTTPException(status_code=400, detail="Only PDF uploads are supported.")

    settings = get_settings(require_api_key=False)
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)

    document_id = f"doc_{uuid.uuid4().hex[:12]}"
    file_path = upload_dir / f"{document_id}.pdf"
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        pages = load_pdf(str(file_path))
        chunks = chunk_pages(pages)
        embeddings = EmbeddingClient().embed_texts([chunk["text"] for chunk in chunks])
        vector_store.add_chunks(document_id=document_id, chunks=chunks, embeddings=embeddings)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {exc}") from exc

    return UploadResponse(
        document_id=document_id,
        filename=file.filename,
        pages=len(pages),
        chunks=len(chunks),
    )


@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest) -> QueryResponse:
    try:
        result = answer_question(request.question, top_k=request.top_k)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to answer question: {exc}") from exc
    return QueryResponse(**result)
