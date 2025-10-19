"""
NextCraftTalk Configuration Module

Handles configuration loading and mode detection for dual deployment modes.
"""

import os
from pathlib import Path
from typing import Optional
from pydantic import BaseSettings, Field
from enum import Enum


class DeploymentMode(str, Enum):
    SELF_HOSTED = "self_hosted"
    EXTERNAL_AI = "external_ai"


class NextcloudConfig(BaseSettings):
    """Nextcloud Talk configuration"""
    url: str = Field(..., env="NEXTCLOUD_URL")
    username: str = Field(..., env="NEXTCLOUD_USERNAME")
    password: str = Field(..., env="NEXTCLOUD_PASSWORD")
    room_token: str = Field(..., env="TALK_ROOM_TOKEN")


class ExternalAIConfig(BaseSettings):
    """External AI (x.ai) configuration"""
    api_key: str = Field(..., env="XAI_API_KEY")
    base_url: str = Field(default="https://api.x.ai/v1", env="XAI_BASE_URL")


class SelfHostedConfig(BaseSettings):
    """Self-hosted AI configuration"""
    ollama_base_url: str = Field(default="http://localhost:11434", env="OLLAMA_BASE_URL")
    ollama_model: str = Field(default="llama2", env="OLLAMA_MODEL")
    chroma_db_path: str = Field(default="./data/chroma_db", env="CHROMA_DB_PATH")
    wiki_base_url: str = Field(default="", env="WIKI_BASE_URL")
    scraping_interval_hours: int = Field(default=24, env="SCRAPING_INTERVAL_HOURS")


class LoggingConfig(BaseSettings):
    """Logging configuration"""
    level: str = Field(default="INFO", env="LOG_LEVEL")
    file: str = Field(default="logs/nextcraft.log", env="LOG_FILE")


class WebhookConfig(BaseSettings):
    """Webhook configuration"""
    port: int = Field(default=8080, env="WEBHOOK_PORT")
    host: str = Field(default="0.0.0.0", env="WEBHOOK_HOST")


class Config(BaseSettings):
    """Main configuration class"""
    deployment_mode: DeploymentMode = Field(default=DeploymentMode.EXTERNAL_AI, env="DEPLOYMENT_MODE")

    nextcloud: NextcloudConfig
    logging: LoggingConfig
    webhook: WebhookConfig

    # Mode-specific configs (loaded conditionally)
    external_ai: Optional[ExternalAIConfig] = None
    self_hosted: Optional[SelfHostedConfig] = None

    class Config:
        env_file = ".env"
        case_sensitive = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Load mode-specific configuration
        if self.deployment_mode == DeploymentMode.EXTERNAL_AI:
            self.external_ai = ExternalAIConfig()
        elif self.deployment_mode == DeploymentMode.SELF_HOSTED:
            self.self_hosted = SelfHostedConfig()


# Global config instance
config = Config()


def get_config() -> Config:
    """Get the global configuration instance"""
    return config


def is_self_hosted_mode() -> bool:
    """Check if running in self-hosted mode"""
    return config.deployment_mode == DeploymentMode.SELF_HOSTED


def is_external_ai_mode() -> bool:
    """Check if running in external AI mode"""
    return config.deployment_mode == DeploymentMode.EXTERNAL_AI