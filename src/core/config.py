"""
NextCraftTalk Configuration Module

Handles configuration loading and mode detection for dual deployment modes.
"""

from enum import Enum
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class DeploymentMode(str, Enum):
    SELF_HOSTED = "self_hosted"
    EXTERNAL_AI = "external_ai"


class NextcloudConfig(BaseSettings):
    """Nextcloud Talk configuration"""

    url: str = Field(env="NEXTCLOUD_URL")
    username: str = Field(env="NEXTCLOUD_USERNAME")
    password: str = Field(env="NEXTCLOUD_PASSWORD")
    room_token: str = Field(env="TALK_ROOM_TOKEN")

    class Config:
        env_file = ".env"
        extra = "ignore"


class ExternalAIConfig(BaseSettings):
    """External AI (x.ai) configuration"""

    api_key: str = Field(env="XAI_API_KEY")
    base_url: str = Field(default="https://api.x.ai/v1", env="XAI_BASE_URL")

    class Config:
        extra = "ignore"


class SelfHostedConfig(BaseSettings):
    """Self-hosted AI configuration"""

    ollama_base_url: str = Field(default="http://localhost:11434", env="OLLAMA_BASE_URL")
    ollama_model: str = Field(default="llama2", env="OLLAMA_MODEL")
    chroma_db_path: str = Field(default="./data/chroma_db", env="CHROMA_DB_PATH")
    chroma_db_host: str = Field(default="", env="CHROMA_DB_HOST")
    chroma_db_port: int = Field(default=8000, env="CHROMA_DB_PORT")
    wiki_base_url: str = Field(default="", env="WIKI_BASE_URL")
    scraping_interval_hours: int = Field(default=24, env="SCRAPING_INTERVAL_HOURS")

    class Config:
        extra = "ignore"


class LoggingConfig(BaseSettings):
    """Logging configuration"""

    level: str = Field(default="INFO", env="LOG_LEVEL")
    file: str = Field(default="logs/nextcraft.log", env="LOG_FILE")

    class Config:
        extra = "ignore"


class WebhookConfig(BaseSettings):
    """Webhook configuration"""

    port: int = Field(default=8080, env="WEBHOOK_PORT")
    host: str = Field(default="0.0.0.0", env="WEBHOOK_HOST")
    shared_secret: Optional[str] = Field(default=None, env="SHARED_SECRET")

    class Config:
        extra = "ignore"


class Config(BaseSettings):
    """Main configuration class"""

    deployment_mode: DeploymentMode = Field(default=DeploymentMode.EXTERNAL_AI, env="DEPLOYMENT_MODE")

    # Nextcloud configuration - make optional for testing
    nextcloud_url: str = Field(default="https://example.com", env="NEXTCLOUD_URL")
    nextcloud_username: str = Field(default="testuser", env="NEXTCLOUD_USERNAME")
    nextcloud_password: str = Field(default="testpass", env="NEXTCLOUD_PASSWORD")

    # External AI configuration
    xai_api_key: str = Field(default="", env="XAI_API_KEY")
    xai_base_url: str = Field(default="https://api.x.ai/v1", env="XAI_BASE_URL")

    # Self-hosted configuration
    ollama_base_url: str = Field(default="http://localhost:11434", env="OLLAMA_BASE_URL")
    ollama_model: str = Field(default="llama2", env="OLLAMA_MODEL")
    chroma_db_path: str = Field(default="./data/chroma_db", env="CHROMA_DB_PATH")
    chroma_db_host: str = Field(default="", env="CHROMA_DB_HOST")
    chroma_db_port: int = Field(default=8000, env="CHROMA_DB_PORT")
    wiki_base_url: str = Field(default="", env="WIKI_BASE_URL")
    scraping_interval_hours: int = Field(default=24, env="SCRAPING_INTERVAL_HOURS")

    # Logging configuration
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: str = Field(default="logs/nextcraft.log", env="LOG_FILE")

    # Webhook configuration
    webhook_port: int = Field(default=8080, env="WEBHOOK_PORT")
    webhook_host: str = Field(default="0.0.0.0", env="WEBHOOK_HOST")
    shared_secret: Optional[str] = Field(default=None, env="SHARED_SECRET")

    class Config:
        extra = "ignore"

    @property
    def self_hosted(self) -> bool:
        """Check if running in self-hosted mode"""
        return self.deployment_mode == DeploymentMode.SELF_HOSTED

    @property
    def external_ai(self) -> bool:
        """Check if running in external AI mode"""
        return self.deployment_mode == DeploymentMode.EXTERNAL_AI


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
