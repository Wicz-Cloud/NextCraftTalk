"""
Ollama LLM Client for Self-Hosted Mode

Handles communication with local Ollama instance for text generation.
"""

import logging
from typing import Any, Optional

import requests

from ....core.config import get_config

logger = logging.getLogger(__name__)


class OllamaClient:
    """Client for interacting with Ollama API"""

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama2"):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self._ensure_model_available()

    def _ensure_model_available(self) -> None:
        """Ensure the specified model is available in Ollama"""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_names = [m["name"] for m in models]
                if self.model not in model_names:
                    logger.warning(f"Model '{self.model}' not found in Ollama. Available: {model_names}")
                    logger.info(f"Pulling model '{self.model}'...")
                    self.pull_model(self.model)
                else:
                    logger.info(f"Model '{self.model}' is available")
            else:
                logger.error(f"Failed to connect to Ollama at {self.base_url}")
        except Exception as e:
            logger.error(f"Error checking Ollama models: {e}")

    def pull_model(self, model_name: str) -> bool:
        """Pull a model from the Ollama library"""
        try:
            response = requests.post(f"{self.base_url}/api/pull", json={"name": model_name})
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Error pulling model {model_name}: {e}")
            return False

    def generate(self, prompt: str, **kwargs: Any) -> Optional[str]:
        """Generate text using the Ollama model"""
        try:
            payload = {"model": self.model, "prompt": prompt, "stream": False, **kwargs}

            response = requests.post(f"{self.base_url}/api/generate", json=payload, timeout=60)

            if response.status_code == 200:
                result = response.json()
                return result.get("response", "")
            else:
                logger.error(f"Ollama API error: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            logger.error(f"Error generating text with Ollama: {e}")
            return None

    def chat(self, messages: list[dict[str, Any]], **kwargs: Any) -> Optional[str]:
        """Chat with the Ollama model using chat format"""
        try:
            payload = {
                "model": self.model,
                "messages": messages,
                "stream": False,
                **kwargs,
            }

            response = requests.post(f"{self.base_url}/api/chat", json=payload, timeout=60)

            if response.status_code == 200:
                result = response.json()
                return result.get("message", {}).get("content", "")
            else:
                logger.error(f"Ollama chat API error: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            logger.error(f"Error chatting with Ollama: {e}")
            return None


# Global instance
_ollama_client: Optional[OllamaClient] = None


def get_ollama_client() -> OllamaClient:
    """Get the global Ollama client instance"""
    global _ollama_client
    if _ollama_client is None:
        config = get_config()
        if config.self_hosted:
            _ollama_client = OllamaClient(
                base_url=config.self_hosted.ollama_base_url,
                model=config.self_hosted.ollama_model,
            )
        else:
            raise ValueError("Self-hosted mode not configured")
    return _ollama_client
