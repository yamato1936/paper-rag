# Paper RAG with Gemini

## Overview
PDF論文・技術資料を対象にしたRAG検索チャットボットです。
PDFをアップロードすると、本文を抽出し、chunking、embedding、vector searchを行い、Gemini APIが根拠付きで回答します。

## Background
LLMは長文PDFをそのまま扱うと、根拠不明な回答やhallucinationが発生しやすいです。
本プロジェクトではRAG構成により、検索された文脈に基づく回答生成を実装しました。

## My Role
- 要件定義
- RAGアーキテクチャ設計
- PDF parser実装
- chunking実装
- embedding生成
- FAISS vector search実装
- Gemini API連携
- FastAPI backend実装
- Streamlit UI実装
- 評価スクリプト作成
- README・技術資料作成

## Architecture
PDF Upload
→ Text Extraction
→ Chunking
→ Embedding
→ FAISS Index
→ Query Embedding
→ Top-k Retrieval
→ Prompt Construction
→ Gemini API
→ Answer with Citations

## Tech Stack
- Python
- FastAPI
- Streamlit
- Google Gemini API
- FAISS
- PyMuPDF
- Pydantic
- pytest

## Environment Variables
This project does not use `.env`.
Set environment variables directly in your shell or deployment environment.

```bash
export GEMINI_API_KEY="your_api_key"
export GEMINI_MODEL="gemini-2.5-flash"
```

`GEMINI_MODEL` is optional. When it is not set, the app uses `gemini-2.5-flash`.
The Gemini API key is never printed by the app.

## How to Run
Install dependencies:

```bash
uv sync
```

Or, if you prefer pip:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Start the FastAPI backend in terminal 1:

```bash
export GEMINI_API_KEY="your_api_key"
export GEMINI_MODEL="gemini-2.5-flash"
bash scripts/run_api.sh
```

Open a second terminal and start the Streamlit UI:

```bash
cd ~/paper-rag
source .venv/bin/activate
export GEMINI_API_KEY="your_api_key"
export GEMINI_MODEL="gemini-2.5-flash"
bash scripts/run_ui.sh
```

Then open `http://localhost:8501` in your browser.
The API docs are available at `http://localhost:8000/docs`.

## API
### Upload PDF
`POST /documents/upload`

Multipart form field:

- `file`: PDF file

Example response:

```json
{
  "document_id": "doc_abc123",
  "filename": "sample.pdf",
  "pages": 12,
  "chunks": 48
}
```

### Ask Question
`POST /query`

```json
{
  "question": "この論文の提案手法は何ですか？",
  "top_k": 5
}
```

### Health Check
`GET /health`

## Evaluation
```bash
python scripts/evaluate.py
```

The evaluation data lives in `data/eval/qa_eval.jsonl`.
The script reports Recall@5, Page Hit Rate, and Keyword Hit Rate.
Because the current vector store is in memory, pass a PDF when running evaluation as a standalone command:

```bash
python scripts/evaluate.py --pdf path/to/sample.pdf
```

## Tests
```bash
pytest
```

Tests do not require a real Gemini API key.

## Challenges and Solutions
Challenge 1: PDF text extraction noise
PDFから抽出したテキストには改行崩れや不要な空白が含まれていました。
Solution: 連続改行、空白、空ページを除去する前処理を実装しました。

Challenge 2: Chunk boundary problem
固定長chunkでは文脈が途中で切れ、検索精度が下がる可能性がありました。
Solution: chunk overlapを導入し、前後の文脈を保持しました。

Challenge 3: Hallucination
LLMが検索結果に存在しない情報を補完する可能性がありました。
Solution: promptで「提供contextのみ使用」「不明なら判断不能と答える」「source citation必須」と制約しました。

## Current Limitations
- vector storeはオンメモリ実装
- PDFレイアウトの完全復元は未対応
- 表や図の理解は未対応
- rerankerは未実装

## Future Work
- FAISS index永続化
- hybrid search
- reranker追加
- section-aware chunking
- 複数PDF対応
- Docker対応
