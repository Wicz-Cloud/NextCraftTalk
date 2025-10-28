# src/shared/safety_filter.py
import os
import re
from typing import Tuple

import requests

# Try to import profanity-check (optional, graceful fallback)
try:
    from profanity_check import predict  # type: ignore

    PROFANITY_CHECK_AVAILABLE = True
except ImportError:
    PROFANITY_CHECK_AVAILABLE = False
    predict = None  # Will be checked in _censor_profanity


PERSPECTIVE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def _get_config() -> dict:
    return {
        "enabled": os.getenv("ENABLE_SAFETY_FILTER", "true").lower() == "true",
        "profanity_threshold": float(os.getenv("PROFANITY_THRESHOLD", "0.6")),
        "toxicity_threshold": float(os.getenv("TOXICITY_THRESHOLD", "0.7")),
        "censor_word": os.getenv("CENSOR_REPLACEMENT", "[REDACTED]"),
        "perspective_key": os.getenv("PERSPECTIVE_API_KEY", ""),
    }


def _censor_profanity(text: str, config: dict) -> str:
    if not PROFANITY_CHECK_AVAILABLE or predict is None:
        return text
    words = text.split()
    return " ".join(
        config["censor_word"] if predict([re.sub(r"[^\w]", "", w.lower())])[0] > config["profanity_threshold"] else w
        for w in words
    )


def _analyze_perspective(text: str, config: dict) -> float:
    if not config["perspective_key"]:
        return 0.0
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "THREAT": {},
            "PROFANITY": {},
            "SEXUALLY_EXPLICIT": {},
        },
        "languages": ["en"],
    }
    try:
        r = requests.post(f"{PERSPECTIVE_URL}?key={config['perspective_key']}", json=payload, timeout=5)
        r.raise_for_status()
        scores = r.json()["attributeScores"]
        return max(scores.get(k, {}).get("summaryScore", {}).get("value", 0) for k in payload["requestedAttributes"])
    except Exception as e:
        print(f"[Perspective] Error: {e}")
        return 0.0


def apply_safety_filter(response: str) -> Tuple[str, bool]:
    """
    Returns (safe_text, is_safe)
    - is_safe = True → send as-is
    - is_safe = False → blocked, use fallback
    """
    config = _get_config()
    if not config["enabled"]:
        return response, True

    # 1. Censor profanity
    response = _censor_profanity(response, config)

    # 2. Check toxicity
    toxicity = _analyze_perspective(response, config)
    if toxicity > config["toxicity_threshold"]:
        return (
            "I'm sorry, I can't share that right now. "
            "Let's keep it fun and safe – ask me about building cool Minecraft stuff!",
            False,
        )

    return response, True
