import json
import re
from typing import Iterable

from google import genai

from .config import settings
from .models import PrintDoc

class LLMError(Exception):
    """Raised for Gemini/LLM related failures."""

def _get_client() -> genai.Client:
    api_key = settings.gemini_api_key
    if not api_key:
        raise LLMError("GEMINI_API_KEY is not configured")
    return genai.Client(api_key=api_key)

def _parse_bits(payload: str) -> list[int]:
    raw = payload.strip()
    if not raw:
        raise LLMError("payload is empty")

    if raw.startswith("["):
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise LLMError("payload JSON parse failed") from exc
        if isinstance(data, list):
            bits = [int(v) for v in data]
        else:
            raise LLMError("payload JSON must be a list")
    else:
        bits = [int(v) for v in re.findall(r"[01]", raw)]

    if len(bits) != 5 or any(v not in (0, 1) for v in bits):
        raise LLMError("payload must contain exactly five 0/1 values")
    return bits

def _topic_index(bits: Iterable[int]) -> int:
    b2, b3 = list(bits)[2:4]
    return (b2 << 1) | b3

def _build_prompt(bits: list[int]) -> str:
    tone = "男" if bits[0] else "女"
    length = "和" if bits[1] else "現代"
    topics = [
        "ファンタジー",
        "外国語由来の言葉",
        "事象",
        "アニメ",
    ]
    topic = topics[_topic_index(bits)]
    include_bullets = bool(bits[4])

    bullets_rule = "漢字表記のキラキラネームを生成する" if include_bullets else "箇条書きは空配列にする"
    return (
        "あなたは赤子に名前をつける親です。次の条件でJSONのみを出力してください。\n"
        "出力フォーマットは {\"name\": string, \"ruby\": string} です。\n"
        "nameは漢字表記です。\n"
        "subnameはnameの読み仮名（ひらがな）です。\n"
        "コードフェンスや説明文は不要です。\n"
        f"トーン: {tone}\n"
        f"長さ: {length}\n"
        f"テーマ: {topic}\n"
        f"箇条書き: {bullets_rule}\n"
    )

def _extract_json(text: str) -> dict:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.S)
        if not match:
            raise
        return json.loads(match.group(0))

def gemini_transform(payload: str) -> tuple[PrintDoc, dict]:
    """
    Transform input payload via Gemini into a PrintDoc.
    """
    bits = _parse_bits(payload)
    prompt = _build_prompt(bits)
    client = _get_client()

    try:
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
        )
    except Exception as exc:
        raise LLMError(f"Gemini request failed: {exc}") from exc

    text = getattr(response, "text", None)
    if not text:
        raise LLMError("Gemini returned empty response")

    try:
        data = _extract_json(text)
    except json.JSONDecodeError as exc:
        raise LLMError("Gemini response is not valid JSON") from exc

    try:
        doc = PrintDoc.model_validate(data)
    except Exception as exc:
        raise LLMError(f"Gemini response validation failed: {exc}") from exc

    return doc, data
