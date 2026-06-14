from google import genai
from google.genai import types

from app.config import get_settings


class GeminiClient:
    def __init__(self, timeout_seconds: int = 60, temperature: float = 0.2) -> None:
        self.settings = get_settings(require_api_key=True)
        self.client = genai.Client(
            api_key=self.settings.gemini_api_key,
            http_options=types.HttpOptions(timeout=timeout_seconds * 1000),
        )
        self.temperature = temperature

    def generate_answer(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.settings.gemini_model,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=self.temperature),
        )
        if not response.text:
            raise RuntimeError("Gemini returned an empty response.")
        return response.text
