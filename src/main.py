#!/usr/bin/env python3
"""
NextCraftTalk Main Application

Unified entry point that loads the appropriate mode based on configuration.
"""

import sys
from pathlib import Path

# Add current directory (src) to path for imports when run from project root
current_path = str(Path(__file__).parent)
if current_path not in sys.path:
    sys.path.insert(0, current_path)

from core.config import get_config, is_external_ai_mode, is_self_hosted_mode  # noqa: E402
from shared.utils import ensure_directories, load_env_file, setup_logging  # noqa: E402


def main() -> None:
    """Main application entry point"""
    # Load environment and setup
    load_env_file()
    ensure_directories()
    setup_logging()

    config = get_config()

    print(f"🚀 Starting NextCraftTalk in {config.deployment_mode.value} mode")

    # Import and run appropriate mode
    if is_external_ai_mode():
        from modes.external_ai.main import run_external_ai

        run_external_ai()
    elif is_self_hosted_mode():
        from modes.self_hosted.main import run_self_hosted

        run_self_hosted()
    else:
        raise ValueError(f"Unknown deployment mode: {config.deployment_mode}")


if __name__ == "__main__":
    main()
