"""
Tests for NextCraftTalk configuration module.
"""

import os
from unittest.mock import patch

import pytest

from src.core.config import (
    Config,
    DeploymentMode,
    ExternalAIConfig,
    NextcloudConfig,
    SelfHostedConfig,
    WebhookConfig,
    get_config,
    is_external_ai_mode,
    is_self_hosted_mode,
)


class TestDeploymentMode:
    """Test DeploymentMode enum."""

    def test_deployment_mode_values(self):
        """Test that deployment modes have correct string values."""
        assert DeploymentMode.SELF_HOSTED.value == "self_hosted"
        assert DeploymentMode.EXTERNAL_AI.value == "external_ai"


class TestNextcloudConfig:
    """Test NextcloudConfig class."""

    def test_nextcloud_config_creation(self):
        """Test creating NextcloudConfig with required fields."""
        config = NextcloudConfig(
            url="https://nextcloud.example.com", username="testuser", password="testpass", room_token="testtoken"
        )
        assert config.url == "https://nextcloud.example.com"
        assert config.username == "testuser"
        assert config.password == "testpass"
        assert config.room_token == "testtoken"

    def test_nextcloud_config_missing_required(self):
        """Test that NextcloudConfig fails without required fields."""
        with pytest.raises(Exception):  # pydantic.ValidationError
            NextcloudConfig()


class TestExternalAIConfig:
    """Test ExternalAIConfig class."""

    def test_external_ai_config_creation(self):
        """Test creating ExternalAIConfig."""
        config = ExternalAIConfig(api_key="test_key")
        assert config.api_key == "test_key"
        assert config.base_url == "https://api.x.ai/v1"

    def test_external_ai_config_custom_url(self):
        """Test ExternalAIConfig with custom base URL."""
        config = ExternalAIConfig(api_key="test_key", base_url="https://custom.api.com/v1")
        assert config.base_url == "https://custom.api.com/v1"


class TestSelfHostedConfig:
    """Test SelfHostedConfig class."""

    def test_self_hosted_config_defaults(self):
        """Test SelfHostedConfig with default values."""
        config = SelfHostedConfig()
        assert config.ollama_base_url == "http://localhost:11434"
        assert config.ollama_model == "llama2"
        assert config.chroma_db_path == "./data/chroma_db"
        assert config.chroma_db_host == ""
        assert config.chroma_db_port == 8000
        assert config.wiki_base_url == ""
        assert config.scraping_interval_hours == 24


class TestWebhookConfig:
    """Test WebhookConfig class."""

    def test_webhook_config_defaults(self):
        """Test WebhookConfig with default values."""
        config = WebhookConfig()
        assert config.port == 8080
        assert config.host == "127.0.0.1"
        assert config.shared_secret is None


class TestConfig:
    """Test main Config class."""

    def test_config_external_ai_defaults(self):
        """Test Config defaults for external AI mode."""
        config = Config(nextcloud_url="https://test.com", nextcloud_username="user", nextcloud_password="pass")
        assert config.deployment_mode == DeploymentMode.EXTERNAL_AI
        assert config.webhook_port == 8080
        assert config.log_level == "INFO"

    def test_config_self_hosted_mode(self):
        """Test Config for self-hosted mode."""
        config = Config(
            deployment_mode=DeploymentMode.SELF_HOSTED,
            nextcloud_url="https://test.com",
            nextcloud_username="user",
            nextcloud_password="pass",
        )
        assert config.deployment_mode == DeploymentMode.SELF_HOSTED

    @patch.dict(
        os.environ,
        {
            "DEPLOYMENT_MODE": "self_hosted",
            "WEBHOOK_PORT": "8081",
            "LOG_LEVEL": "DEBUG",
            "NEXTCLOUD_URL": "https://env-test.com",
            "NEXTCLOUD_USERNAME": "env_user",
            "NEXTCLOUD_PASSWORD": "env_pass",
        },
    )
    def test_config_from_env(self):
        """Test Config loading from environment variables."""
        config = Config()
        assert config.deployment_mode == DeploymentMode.SELF_HOSTED
        assert config.webhook_port == 8081
        assert config.log_level == "DEBUG"
        assert config.nextcloud_url == "https://env-test.com"
        assert config.nextcloud_username == "env_user"
        assert config.nextcloud_password == "env_pass"


class TestConfigFunctions:
    """Test configuration utility functions."""

    @patch(
        "src.core.config.config",
        Config(
            deployment_mode=DeploymentMode.EXTERNAL_AI,
            nextcloud_url="https://test.com",
            nextcloud_username="user",
            nextcloud_password="pass",
        ),
    )
    def test_get_config(self):
        """Test get_config function."""
        config = get_config()
        assert isinstance(config, Config)
        assert config.deployment_mode == DeploymentMode.EXTERNAL_AI

    @patch(
        "src.core.config.config",
        Config(
            deployment_mode=DeploymentMode.EXTERNAL_AI,
            nextcloud_url="https://test.com",
            nextcloud_username="user",
            nextcloud_password="pass",
        ),
    )
    def test_is_external_ai_mode(self):
        """Test is_external_ai_mode function."""
        assert is_external_ai_mode() is True
        assert is_self_hosted_mode() is False

    @patch(
        "src.core.config.config",
        Config(
            deployment_mode=DeploymentMode.SELF_HOSTED,
            nextcloud_url="https://test.com",
            nextcloud_username="user",
            nextcloud_password="pass",
        ),
    )
    def test_is_self_hosted_mode(self):
        """Test is_self_hosted_mode function."""
        assert is_self_hosted_mode() is True
        assert is_external_ai_mode() is False
