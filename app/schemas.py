from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    document_id: str
    filename: str
    pages: int
    chunks: int


class QueryRequest(BaseModel):
    question: str = Field(min_length=1)
    top_k: int = Field(default=5, ge=1, le=20)


class Source(BaseModel):
    document_id: str
    chunk_id: str
    page: int
    score: float
    text_preview: str


class QueryResponse(BaseModel):
    answer: str
    sources: list[Source]
