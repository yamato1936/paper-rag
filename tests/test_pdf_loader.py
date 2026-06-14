import fitz

from app.pdf_loader import load_pdf


def test_load_pdf_extracts_page_text(tmp_path) -> None:
    file_path = tmp_path / "sample.pdf"
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), "Hello PDF")
    document.save(file_path)
    document.close()

    pages = load_pdf(str(file_path))

    assert pages == [{"page": 1, "text": "Hello PDF"}]


def test_load_pdf_excludes_empty_pages(tmp_path) -> None:
    file_path = tmp_path / "sample.pdf"
    document = fitz.open()
    document.new_page()
    page = document.new_page()
    page.insert_text((72, 72), "Text page")
    document.save(file_path)
    document.close()

    pages = load_pdf(str(file_path))

    assert pages == [{"page": 2, "text": "Text page"}]
