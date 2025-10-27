"""
NextCraftTalk External AI Mode

Integrates NextCraftTalk-EXT code with unified configuration system.
"""

import logging

import uvicorn

from src.core.config import get_config
from src.shared.utils import setup_logging


def run_external_ai() -> None:
    """Run the external AI mode application"""
    config = get_config()
    setup_logging()

    logger = logging.getLogger(__name__)
    logger.info("🚀 Starting NextCraftTalk in External AI mode")
    # Always bind to port 8080 inside the container
    # External port mapping is handled by docker-compose
    uvicorn.run(
        "src.modes.external_ai.bot.api:app",
        host=config.webhook_host,
        port=8080,  # Fixed internal port for container
        reload=True,
    )


if __name__ == "__main__":
    run_external_ai()
