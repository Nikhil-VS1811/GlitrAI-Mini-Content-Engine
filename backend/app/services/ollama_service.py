"""Client for generating text with the local Ollama service."""

from typing import Any

import httpx


OLLAMA_GENERATE_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "gemma4:12b"
OLLAMA_TIMEOUT_SECONDS = 120.0


class OllamaServiceError(RuntimeError):
    """Raised when Ollama cannot produce a valid generation response."""


def generate_marketing_prompt(product_name: str, description: str) -> str:
    """Generate a concise marketing prompt for a product using Ollama."""
    instruction = (
        "Create one concise, high-quality marketing prompt for the product below. "
        "Focus on its value, audience appeal, and clear product details. "
        "Return only the marketing prompt, with no commentary or labels.\n\n"
        f"Product name: {product_name}\n"
        f"Description: {description}"
    )
    payload: dict[str, Any] = {
        "model": OLLAMA_MODEL,
        "prompt": instruction,
        "stream": False,
    }

    try:
        with httpx.Client(timeout=OLLAMA_TIMEOUT_SECONDS) as client:
            response = client.post(OLLAMA_GENERATE_URL, json=payload)
            response.raise_for_status()
            body = response.json()
    except (httpx.HTTPError, ValueError) as exc:
        raise OllamaServiceError("Ollama prompt generation failed.") from exc

    if not isinstance(body, dict):
        raise OllamaServiceError("Ollama returned an invalid response body.")

    generated_prompt = body.get("response")
    if not isinstance(generated_prompt, str) or not generated_prompt.strip():
        raise OllamaServiceError("Ollama returned an empty or invalid response.")

    return generated_prompt.strip()
