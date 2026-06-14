# Evaluation

The evaluation script reads `data/eval/qa_eval.jsonl`.

Each JSONL row contains:

- `question`
- `gold_pages`
- `gold_keywords`

Metrics:

- `Recall@5`: 1 when any retrieved top-5 page appears in `gold_pages`.
- `Page Hit Rate`: same page-level hit averaged over all questions.
- `Keyword Hit Rate`: 1 when retrieved source text contains any gold keyword.

Run:

```bash
python scripts/evaluate.py
```

The current vector store is in memory, so evaluation should be run in the same process after loading documents, or extended later to load a persisted FAISS index.
