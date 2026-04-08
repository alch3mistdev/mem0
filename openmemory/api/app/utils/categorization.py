import json
import logging
from typing import List, Optional

from mem0.memory.utils import extract_json
from mem0.utils.factory import LlmFactory
from tenacity import retry, stop_after_attempt, wait_exponential

from app.utils.prompts import MEMORY_CATEGORIZATION_PROMPT

logger = logging.getLogger(__name__)

# Providers where the Mem0 client either ignores ``response_format`` or is unlikely to support
# OpenAI-style ``json_object`` mode reliably — use prompt-only JSON and parse from text.
_JSON_OBJECT_UNSUPPORTED = frozenset({"anthropic", "langchain", "sarvam", "aws_bedrock"})

_llm = None
_llm_cache_key: Optional[str] = None


def reset_categorization_llm() -> None:
    """Invalidate cached categorization LLM (e.g. after config/env changes)."""
    global _llm, _llm_cache_key
    _llm = None
    _llm_cache_key = None


def _bundle_cache_key(bundle: dict) -> str:
    return json.dumps(bundle, sort_keys=True)


def _get_llm_and_provider():
    from app.utils.memory import get_categorization_llm_config

    global _llm, _llm_cache_key
    bundle = get_categorization_llm_config()
    key = _bundle_cache_key(bundle)
    if _llm is None or _llm_cache_key != key:
        provider = bundle["provider"]
        supported = LlmFactory.get_supported_providers()
        if provider not in supported:
            raise ValueError(
                f"Categorization LLM provider '{provider}' is not supported. "
                f"Use one of: {', '.join(sorted(supported))}. "
                "If CATEGORIZATION_USE_EMBEDDER_CREDENTIALS is set, your EMBEDDER_PROVIDER must "
                "also be a Mem0 LLM provider (e.g. openai or ollama), or set CATEGORIZATION_PROVIDER."
            )
        cfg = bundle["config"]
        _llm = LlmFactory.create(provider, config=cfg)
        _llm_cache_key = key
    return _llm, bundle["provider"]


def _response_format_for_provider(provider: str):
    if provider in _JSON_OBJECT_UNSUPPORTED:
        return None
    return {"type": "json_object"}


def _normalize_llm_text(raw) -> str:
    if isinstance(raw, dict):
        if raw.get("content") is not None:
            raw = raw["content"]
        else:
            raw = json.dumps(raw)
    if not isinstance(raw, str):
        raw = str(raw)
    return raw


def _parse_categories_json(text: str) -> List[str]:
    json_str = extract_json(text)
    data = json.loads(json_str)
    cats = data.get("categories")
    if not isinstance(cats, list):
        return []
    return [str(cat).strip().lower() for cat in cats if cat]


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=15))
def get_categories_for_memory(memory: str) -> List[str]:
    llm, provider = _get_llm_and_provider()
    rf = _response_format_for_provider(provider)
    messages = [
        {"role": "system", "content": MEMORY_CATEGORIZATION_PROMPT},
        {"role": "user", "content": memory},
    ]

    try:
        raw = llm.generate_response(
            messages,
            response_format=rf,
            temperature=0,
        )
    except Exception as first_error:
        if rf is not None:
            logger.warning(
                "Categorization: JSON response mode failed (%s); retrying without response_format.",
                first_error,
            )
            raw = llm.generate_response(
                messages,
                response_format=None,
                temperature=0,
            )
        else:
            logger.error("[ERROR] Failed to get categories: %s", first_error)
            raise

    text = _normalize_llm_text(raw)
    try:
        return _parse_categories_json(text)
    except (json.JSONDecodeError, TypeError, ValueError) as e:
        logger.error("[ERROR] Failed to parse categorization JSON: %s — raw: %s", e, text[:500])
        raise

