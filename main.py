#!/usr/bin/env python3
"""
NextCraftTalk Main Application

Unified entry point that loads the appropriate mode based on configuration.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.shared.utils import load_env_file, setup_logging, ensure_directories
from src.core.config import get_config, is_self_hosted_mode, is_external_ai_mode


def main():
    """Main application entry point"""
    # Load environment and setup
    load_env_file()
    ensure_directories()
    setup_logging()

    config = get_config()

    print(f"🚀 Starting NextCraftTalk in {config.deployment_mode.value} mode")

    # Import and run appropriate mode
    if is_external_ai_mode():
        from src.modes.external_ai.main import run_external_ai
        run_external_ai()
    elif is_self_hosted_mode():
        from src.modes.self_hosted.main import run_self_hosted
        run_self_hosted()
    else:
        raise ValueError(f"Unknown deployment mode: {config.deployment_mode}")


if __name__ == "__main__":
    main()