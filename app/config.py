import os
from dataclasses import dataclass


DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"
DEFAULT_EMBEDDING_MODEL = "gemini-embedding-001"


@dataclass(frozen=True)
class Settings:
    gemini_api_key: str
    gemini_model: str = DEFAULT_GEMINI_MODEL
    gemini_embedding_model: str = DEFAULT_EMBEDDING_MODEL
    upload_dir: str = "data/uploads"


def get_settings(require_api_key: bool = True) -> Settings:
    api_key = os.getenv("GEMINI_API_KEY", "")
    if require_api_key and not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set. Set it as an environment variable.")

    return Settings(
        gemini_api_key=api_key,
        gemini_model=os.getenv("GEMINI_MODEL", DEFAULT_GEMINI_MODEL),
        gemini_embedding_model=os.getenv("GEMINI_EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL),
        upload_dir=os.getenv("UPLOAD_DIR", "data/uploads"),
    )
