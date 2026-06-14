import os

import requests
import streamlit as st


API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

st.set_page_config(page_title="Paper RAG with Gemini", layout="wide")
st.title("Paper RAG with Gemini")

st.header("Upload PDF")
uploaded_file = st.file_uploader("PDF file", type=["pdf"])
if uploaded_file and st.button("Upload"):
    try:
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
        response = requests.post(f"{API_BASE_URL}/documents/upload", files=files, timeout=120)
        response.raise_for_status()
        st.success("Upload complete")
        st.json(response.json())
    except requests.RequestException as exc:
        detail = exc.response.text if getattr(exc, "response", None) is not None else str(exc)
        st.error(f"Upload failed: {detail}")

st.header("Ask a question")
question = st.text_input("Question")
top_k = st.number_input("top_k", min_value=1, max_value=20, value=5, step=1)

if st.button("Ask") and question:
    try:
        response = requests.post(
            f"{API_BASE_URL}/query",
            json={"question": question, "top_k": top_k},
            timeout=120,
        )
        response.raise_for_status()
        result = response.json()

        st.header("Answer")
        st.write(result["answer"])

        st.header("Sources")
        for source in result["sources"]:
            with st.expander(
                f"page {source['page']} / {source['chunk_id']} / score {source['score']:.3f}"
            ):
                st.write(source["text_preview"])
                st.caption(f"document_id: {source['document_id']}")
    except requests.RequestException as exc:
        detail = exc.response.text if getattr(exc, "response", None) is not None else str(exc)
        st.error(f"Question failed: {detail}")
