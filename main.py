#!/usr/bin/env python3
"""
NextCraftTalk Main Application

Unified entry point that loads the appropriate mode based on configuration.
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = str(Path(__file__).parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from src.core.config import (  # noqa: E402
    get_config,
    is_external_ai_mode,
    is_self_hosted_mode,
)
from src.shared.utils import (  # noqa: E402
    ensure_directories,
    load_env_file,
    setup_logging,
)


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
