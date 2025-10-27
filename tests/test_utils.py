"""
Tests for NextCraftTalk shared utilities.
"""

import logging
from pathlib import Path
from unittest.mock import patch

from src.core.config import Config, DeploymentMode
from src.shared.utils import ensure_directories, get_project_root, load_env_file, setup_logging


class TestSetupLogging:
    """Test logging setup functionality."""

    @patch("src.shared.utils.get_config")
    def test_setup_logging(self, mock_get_config):
        """Test that logging is configured correctly."""
        # Setup mock config
        mock_config = Config(
            nextcloud_url="https://test.com",
            nextcloud_username="user",
            nextcloud_password="pass",
            log_level="DEBUG",
            log_file="test.log",
        )
        mock_get_config.return_value = mock_config

        # Clear any existing handlers
        logger = logging.getLogger()
        logger.handlers.clear()

        # Setup logging
        setup_logging()

        # Check that handlers were added
        assert len(logger.handlers) >= 2  # FileHandler and StreamHandler

        # Check log level
        assert logger.level == logging.DEBUG

        # Clean up
        logger.handlers.clear()


class TestEnsureDirectories:
    """Test directory creation functionality."""

    def test_ensure_directories_external_ai(self, temp_dir):
        """Test directory creation for external AI mode."""
        with patch("src.shared.utils.get_config") as mock_get_config:
            mock_config = Config(
                deployment_mode=DeploymentMode.EXTERNAL_AI,
                nextcloud_url="https://test.com",
                nextcloud_username="user",
                nextcloud_password="pass",
            )
            mock_get_config.return_value = mock_config

            # Change to temp directory
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(temp_dir)

                ensure_directories()

                # Check that basic directories were created
                assert (temp_dir / "logs").exists()
                assert (temp_dir / "data").exists()

            finally:
                os.chdir(original_cwd)

    def test_ensure_directories_self_hosted(self, temp_dir):
        """Test directory creation for self-hosted mode."""
        with patch("src.shared.utils.get_config") as mock_get_config:
            mock_config = Config(
                deployment_mode=DeploymentMode.SELF_HOSTED,
                nextcloud_url="https://test.com",
                nextcloud_username="user",
                nextcloud_password="pass",
                chroma_db_path="./data/chroma_db",
            )
            mock_get_config.return_value = mock_config

            # Change to temp directory
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(temp_dir)

                ensure_directories()

                # Check that all directories were created
                assert (temp_dir / "logs").exists()
                assert (temp_dir / "data").exists()
                assert (temp_dir / "data").exists()  # Parent of chroma_db_path

            finally:
                os.chdir(original_cwd)


class TestGetProjectRoot:
    """Test project root detection."""

    def test_get_project_root(self):
        """Test that project root is detected correctly."""
        root = get_project_root()
        assert isinstance(root, Path)
        assert root.exists()
        assert root.is_dir()

        # Should contain src directory
        assert (root / "src").exists()


class TestLoadEnvFile:
    """Test environment file loading."""

    def test_load_env_file_exists(self, temp_dir):
        """Test loading existing env file."""
        env_file = temp_dir / ".env"
        env_content = "TEST_VAR=test_value\nANOTHER_VAR=another_value\n"
        env_file.write_text(env_content)

        # Mock get_project_root to return temp_dir
        with patch("src.shared.utils.get_project_root", return_value=temp_dir):
            load_env_file()

            # Check that environment variables were loaded
            import os as os_module

            assert os_module.getenv("TEST_VAR") == "test_value"
            assert os_module.getenv("ANOTHER_VAR") == "another_value"

    def test_load_env_file_not_exists(self, temp_dir):
        """Test loading non-existent env file."""
        # Change to temp directory
        original_cwd = Path.cwd()
        try:
            import os

            os.chdir(temp_dir)

            # Should not raise an exception
            load_env_file("nonexistent.env")

        finally:
            os.chdir(original_cwd)

    def test_load_env_file_custom_name(self, temp_dir):
        """Test loading custom env file name."""
        custom_env = temp_dir / "custom.env"
        custom_env.write_text("CUSTOM_VAR=custom_value\n")

        # Mock get_project_root to return temp_dir
        with patch("src.shared.utils.get_project_root", return_value=temp_dir):
            load_env_file("custom.env")

            # Check that environment variable was loaded
            import os as os_module

            assert os_module.getenv("CUSTOM_VAR") == "custom_value"
