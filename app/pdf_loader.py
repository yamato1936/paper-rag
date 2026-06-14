import re

import fitz


def _normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def load_pdf(file_path: str) -> list[dict]:
    pages: list[dict] = []
    with fitz.open(file_path) as document:
        for index, page in enumerate(document, start=1):
            text = _normalize_text(page.get_text("text"))
            if text:
                pages.append({"page": index, "text": text})
    return pages
