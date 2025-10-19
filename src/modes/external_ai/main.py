"""
NextCraftTalk External AI Mode

Integrates NextCraftTalk-EXT code with unified configuration system.
"""

import logging
import uvicorn

from ...core.config import get_config
from ...shared.utils import setup_logging


def run_external_ai():
    """Run the external AI mode application"""
    config = get_config()

    logger = logging.getLogger(__name__)
    logger.info("🚀 Starting NextCraftTalk in External AI mode")
    uvicorn.run(
        "src.modes.external_ai.bot.api:app",
        host=config.webhook.host,
        port=config.webhook.port,
        reload=True
    )


if __name__ == "__main__":
    run_external_ai()