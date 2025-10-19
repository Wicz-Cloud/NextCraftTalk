"""
NextCraftTalk Self-Hosted Mode

Handles Nextcloud Talk integration with self-hosted AI stack.
Placeholder for Phase 2 implementation.
"""

import logging
from fastapi import FastAPI

logger = logging.getLogger(__name__)
app = FastAPI(title="NextCraftTalk Self-Hosted")


def run_self_hosted():
    """Run the self-hosted mode application"""
    logger.info("🚀 Self-hosted mode not yet implemented (Phase 2)")
    logger.info("This will include Ollama, ChromaDB, and RAG pipeline")
    print("Self-hosted mode: Coming in Phase 2!")
    print("For now, only external AI mode is available.")


if __name__ == "__main__":
    run_self_hosted()