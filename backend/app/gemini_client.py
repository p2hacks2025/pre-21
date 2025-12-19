from google import genai  # google-genai パッケージを前提とする
from .config import settings
from .models import PrintDoc

class LLMError(Exception):
    """Raised for Gemini/LLM related failures."""

def _get_client():
    api_key = settings.gemini_api_key
    if not api_key:
        raise LLMError("GEMINI_API_KEY is not configured")
    # google.genai のクライアントを返す
    return genai.Client(api_key=api_key)

def gemini_transform(payload: str) -> PrintDoc:
    """
    Transform input payload via Gemini into a PrintDoc.

    NOTE: 未実装。実装時は google.generativeai の GenerativeModel を利用してください。
    今はジョブの失敗を適切に扱うため、明示的に LLMError を送出します。
    """
    raise LLMError("gemini_transform is not implemented yet; implement using google.genai")
