"""
Configuration compatibility layer for NextCraftTalk-EXT code

Adapts the unified NextCraftTalk configuration to work with existing NextCraftTalk-EXT code.
"""

import os
from pathlib import Path
from typing import Optional

from src.core.config import get_config


class Settings:
    """Compatibility wrapper for NextCraftTalk-EXT settings"""

    def __init__(self):
        self._config = get_config()

    @property
    def bot_port(self) -> int:
        """Bot port from unified config"""
        return self._config.webhook_port

    @property
    def bot_name(self) -> str:
        """Bot name (placeholder)"""
        return "NextCraftTalkBot"

    @property
    def bot_display_name(self) -> str:
        """Bot display name (placeholder)"""
        return "NextCraftTalk Assistant"

    @property
    def network_name(self) -> str:
        """Docker network name (placeholder)"""
        return "nextcraft-network"

    @property
    def nextcloud_url(self) -> Optional[str]:
        """Nextcloud URL from unified config"""
        return self._config.nextcloud_url

    @property
    def nextcloud_bot_token(self) -> Optional[str]:
        """Nextcloud bot token (use password if available, otherwise room token)"""
        # Try password first (for bot token auth), then room token
        return self._config.nextcloud_password

    @property
    def shared_secret(self) -> Optional[str]:
        """Shared secret for webhook verification"""
        return self._config.shared_secret

    @property
    def xai_api_key(self) -> Optional[str]:
        """x.ai API key from unified config"""
        return self._config.xai_api_key

    @property
    def xai_url(self) -> str:
        """x.ai API URL from unified config"""
        return self._config.xai_base_url

    @property
    def model_name(self) -> str:
        """x.ai model name (from .env or default)"""
        return os.getenv("MODEL_NAME", "grok-4-fast-non-reasoning")

    @property
    def prompt_template_path(self) -> str:
        """Prompt template path"""
        return "prompt_template.txt"

    @property
    def max_workers(self) -> int:
        """Max workers (placeholder)"""
        return 2

    @property
    def batch_size(self) -> int:
        """Batch size (placeholder)"""
        return 50

    @property
    def log_level(self) -> str:
        """Log level from unified config"""
        return self._config.log_level

    @property
    def log_file(self) -> str:
        """Log file from unified config"""
        return self._config.log_file

    @property
    def verbose_logging(self) -> bool:
        """Verbose logging (placeholder)"""
        return False

    @property
    def log_path(self) -> Path:
        """Get the log file path"""
        return Path(self.log_file)

    def ensure_log_directory(self) -> None:
        """Ensure log directory exists"""
        self.log_path.parent.mkdir(parents=True, exist_ok=True)


# Global settings instance for compatibility
settings = Settings()
