"""
Tests for NextCraftTalk main entry point.
"""

from unittest.mock import MagicMock, patch

import pytest

from src.core.config import DeploymentMode
from src.main import main


class TestMain:
    """Test main application entry point."""

    @patch("src.main.setup_logging")
    @patch("src.main.load_env_file")
    @patch("src.main.ensure_directories")
    @patch("src.main.get_config")
    @patch("src.main.is_external_ai_mode", return_value=True)
    @patch("modes.external_ai.main.run_external_ai")
    def test_main_external_ai_mode(
        self, mock_run_external, mock_is_external, mock_get_config, mock_ensure_dirs, mock_load_env, mock_setup_logging
    ):
        """Test main function in external AI mode."""
        # Setup mock config
        mock_config = mock_get_config.return_value
        mock_config.deployment_mode = DeploymentMode.EXTERNAL_AI

        # Run main
        main()

        # Verify calls
        mock_load_env.assert_called_once()
        mock_ensure_dirs.assert_called_once()
        mock_setup_logging.assert_called_once()
        mock_get_config.assert_called_once()
        mock_is_external.assert_called_once()
        mock_run_external.assert_called_once()

    @pytest.mark.skip(reason="Dynamic import in main() makes mocking difficult")
    @patch("src.main.setup_logging")
    @patch("src.main.load_env_file")
    @patch("src.main.ensure_directories")
    @patch("src.main.get_config")
    @patch("src.main.is_external_ai_mode", return_value=False)
    @patch("src.main.is_self_hosted_mode", return_value=True)
    @patch("modes.self_hosted.main.run_self_hosted")  # Patch the imported function in main
    def test_main_self_hosted_mode(
        self,
        mock_run_self_hosted,
        mock_is_self_hosted,
        mock_is_external,
        mock_get_config,
        mock_ensure_dirs,
        mock_load_env,
        mock_setup_logging,
    ):
        """Test main function in self-hosted mode."""
        # Setup mock config
        mock_config = mock_get_config.return_value
        mock_config.deployment_mode = DeploymentMode.SELF_HOSTED
        # Mock the self_hosted property to return a truthy value
        mock_config.self_hosted = MagicMock()

        # Run main
        main()

        # Verify calls
        mock_load_env.assert_called_once()
        mock_ensure_dirs.assert_called_once()
        mock_setup_logging.assert_called_once()
        mock_get_config.assert_called_once()
        mock_is_external.assert_called_once()
        mock_is_self_hosted.assert_called_once()
        mock_run_self_hosted.assert_called_once()

    @patch("src.main.setup_logging")
    @patch("src.main.load_env_file")
    @patch("src.main.ensure_directories")
    @patch("src.main.get_config")
    @patch("src.main.is_external_ai_mode", return_value=False)
    @patch("src.main.is_self_hosted_mode", return_value=False)
    def test_main_unknown_mode(
        self,
        mock_is_self_hosted,
        mock_is_external,
        mock_get_config,
        mock_ensure_dirs,
        mock_load_env,
        mock_setup_logging,
    ):
        """Test main function with unknown deployment mode."""
        # Setup mock config
        mock_config = mock_get_config.return_value
        # Create a mock deployment mode with unknown value
        mock_deployment_mode = MagicMock()
        mock_deployment_mode.value = "unknown"
        mock_config.deployment_mode = mock_deployment_mode

        # Run main and expect ValueError
        with pytest.raises(ValueError, match="Unknown deployment mode"):
            main()

        # Verify setup calls still happened
        mock_load_env.assert_called_once()
        mock_ensure_dirs.assert_called_once()
        mock_setup_logging.assert_called_once()
        mock_get_config.assert_called_once()
