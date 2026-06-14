from app.chunker import chunk_pages


def test_chunks_are_not_empty() -> None:
    pages = [{"page": 1, "text": "a" * 400}]
    chunks = chunk_pages(pages, chunk_size=50, chunk_overlap=10)
    assert chunks
    assert all(chunk["text"] for chunk in chunks)


def test_chunk_ids_are_unique() -> None:
    pages = [{"page": 1, "text": "a" * 1000}]
    chunks = chunk_pages(pages, chunk_size=50, chunk_overlap=10)
    ids = [chunk["chunk_id"] for chunk in chunks]
    assert len(ids) == len(set(ids))


def test_chunk_overlap_works() -> None:
    text = "".join(str(index % 10) for index in range(500))
    chunks = chunk_pages([{"page": 1, "text": text}], chunk_size=50, chunk_overlap=25)
    assert len(chunks) >= 2
    assert chunks[0]["text"][-100:] == chunks[1]["text"][:100]


def test_short_chunks_are_excluded() -> None:
    chunks = chunk_pages([{"page": 1, "text": "too short"}])
    assert chunks == []
