MIN_CHUNK_CHARS = 100


def chunk_pages(
    pages: list[dict],
    chunk_size: int = 800,
    chunk_overlap: int = 120,
) -> list[dict]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0.")
    if chunk_overlap < 0:
        raise ValueError("chunk_overlap must be greater than or equal to 0.")
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size.")

    chunk_chars = chunk_size * 4
    overlap_chars = chunk_overlap * 4
    step = chunk_chars - overlap_chars
    chunks: list[dict] = []

    for page in pages:
        text = page["text"].strip()
        start = 0
        while start < len(text):
            piece = text[start : start + chunk_chars].strip()
            if len(piece) >= MIN_CHUNK_CHARS:
                chunks.append(
                    {
                        "chunk_id": f"chunk_{len(chunks) + 1:04d}",
                        "page": page["page"],
                        "text": piece,
                        "token_estimate": max(1, len(piece) // 4),
                    }
                )
            start += step

    return chunks
