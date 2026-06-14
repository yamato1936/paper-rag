import argparse
import json
from pathlib import Path

from app.chunker import chunk_pages
from app.embeddings import EmbeddingClient
from app.pdf_loader import load_pdf
from app.vector_store import vector_store


def index_pdf(pdf_path: Path, document_id: str = "eval_doc") -> None:
    pages = load_pdf(str(pdf_path))
    chunks = chunk_pages(pages)
    embedding_client = EmbeddingClient()
    embeddings = embedding_client.embed_texts([chunk["text"] for chunk in chunks])
    vector_store.add_chunks(document_id=document_id, chunks=chunks, embeddings=embeddings)


def load_eval_data(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def evaluate(path: Path, top_k: int = 5) -> dict:
    rows = load_eval_data(path)
    if not rows:
        return {"questions": 0, "recall_at_5": 0.0, "page_hit_rate": 0.0, "keyword_hit_rate": 0.0}

    embedding_client = EmbeddingClient()
    recall_hits = 0
    page_hits = 0
    keyword_hits = 0

    for row in rows:
        query_embedding = embedding_client.embed_query(row["question"])
        sources = vector_store.search(query_embedding, top_k=top_k)
        pages = {source["page"] for source in sources}
        combined_text = " ".join(source["text"].lower() for source in sources)
        gold_pages = set(row.get("gold_pages", []))
        gold_keywords = [keyword.lower() for keyword in row.get("gold_keywords", [])]

        if pages & gold_pages:
            recall_hits += 1
            page_hits += 1
        if gold_keywords and any(keyword in combined_text for keyword in gold_keywords):
            keyword_hits += 1

    total = len(rows)
    return {
        "questions": total,
        "recall_at_5": recall_hits / total,
        "page_hit_rate": page_hits / total,
        "keyword_hit_rate": keyword_hits / total,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--eval-file", default="data/eval/qa_eval.jsonl")
    parser.add_argument("--pdf", help="Optional PDF to index before running evaluation.")
    parser.add_argument("--top-k", type=int, default=5)
    args = parser.parse_args()

    if args.pdf:
        index_pdf(Path(args.pdf))

    result = evaluate(Path(args.eval_file), top_k=args.top_k)
    print("Evaluation Result")
    print("-----------------")
    print(f"Questions: {result['questions']}")
    print(f"Recall@5: {result['recall_at_5']:.2f}")
    print(f"Page Hit Rate: {result['page_hit_rate']:.2f}")
    print(f"Keyword Hit Rate: {result['keyword_hit_rate']:.2f}")


if __name__ == "__main__":
    main()
