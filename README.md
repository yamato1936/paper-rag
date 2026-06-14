# Paper RAG with Gemini

## 概要
PDF論文・技術資料を対象にしたRAG検索チャットボットです。
PDFをアップロードすると、本文を抽出し、チャンク分割、埋め込み生成、ベクトル検索を行い、Gemini APIが根拠付きで回答します。

## 背景
LLMは長文PDFをそのまま扱うと、根拠不明な回答やハルシネーションが発生しやすいです。
本プロジェクトではRAG構成により、検索された文脈に基づく回答生成を実装しました。

## 担当範囲
- 要件定義
- RAGアーキテクチャ設計
- PDFパーサー実装
- チャンク分割実装
- 埋め込み生成
- FAISSベクトル検索実装
- Gemini API連携
- FastAPIバックエンド実装
- Streamlit UI実装
- 評価スクリプト作成
- README・技術資料作成

## アーキテクチャ
PDFアップロード
→ テキスト抽出
→ チャンク分割
→ 埋め込み生成
→ FAISSインデックス
→ クエリ埋め込み生成
→ Top-k検索
→ プロンプト構築
→ Gemini API
→ 引用付き回答

## 技術スタック
- Python
- FastAPI
- Streamlit
- Google Gemini API
- FAISS
- PyMuPDF
- Pydantic
- pytest

## 環境変数
このプロジェクトでは`.env`を使用しません。
環境変数はシェルまたはデプロイ環境で直接設定してください。

```bash
export GEMINI_API_KEY="your_api_key"
export GEMINI_MODEL="gemini-2.5-flash"
```

`GEMINI_MODEL`は任意です。未設定の場合、アプリは`gemini-2.5-flash`を使用します。
Gemini APIキーがアプリから出力されることはありません。

## 実行方法
依存関係をインストールします。

```bash
uv sync
```

pipを使う場合は、次の手順でインストールします。

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

ターミナル1でFastAPIバックエンドを起動します。

```bash
export GEMINI_API_KEY="your_api_key"
export GEMINI_MODEL="gemini-2.5-flash"
bash scripts/run_api.sh
```

ターミナル2でStreamlit UIを起動します。

```bash
cd ~/paper-rag
source .venv/bin/activate
export GEMINI_API_KEY="your_api_key"
export GEMINI_MODEL="gemini-2.5-flash"
bash scripts/run_ui.sh
```

ブラウザで`http://localhost:8501`を開きます。
APIドキュメントは`http://localhost:8000/docs`で確認できます。

## API
### PDFアップロード
`POST /documents/upload`

multipart/form-dataのフィールド:

- `file`: PDFファイル

レスポンス例:

```json
{
  "document_id": "doc_abc123",
  "filename": "sample.pdf",
  "pages": 12,
  "chunks": 48
}
```

### 質問
`POST /query`

```json
{
  "question": "この論文の提案手法は何ですか？",
  "top_k": 5
}
```

### ヘルスチェック
`GET /health`

## 評価
```bash
python scripts/evaluate.py
```

評価データは`data/eval/qa_eval.jsonl`にあります。
スクリプトはRecall@5、Page Hit Rate、Keyword Hit Rateを出力します。
現在のベクトルストアはオンメモリ実装のため、単独コマンドとして評価を実行する場合はPDFを指定してください。

```bash
python scripts/evaluate.py --pdf path/to/sample.pdf
```

## テスト
```bash
pytest
```

テストに実際のGemini APIキーは不要です。

## 課題と対応
課題1: PDFテキスト抽出時のノイズ
PDFから抽出したテキストには改行崩れや不要な空白が含まれていました。
対応: 連続改行、空白、空ページを除去する前処理を実装しました。

課題2: チャンク境界の問題
固定長チャンクでは文脈が途中で切れ、検索精度が下がる可能性がありました。
対応: チャンクのオーバーラップを導入し、前後の文脈を保持しました。

課題3: ハルシネーション
LLMが検索結果に存在しない情報を補完する可能性がありました。
対応: プロンプトで「提供されたコンテキストのみ使用」「不明なら判断不能と答える」「出典引用必須」と制約しました。

## 現在の制約
- ベクトルストアはオンメモリ実装
- PDFレイアウトの完全復元は未対応
- 表や図の理解は未対応
- リランカーは未実装

## 今後の予定
- FAISSインデックス永続化
- ハイブリッド検索
- リランカー追加
- セクションを考慮したチャンク分割
- 複数PDF対応
- Docker対応
