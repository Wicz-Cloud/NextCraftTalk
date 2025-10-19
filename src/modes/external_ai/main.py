"""
NextCraftTalk External AI Mode

Handles Nextcloud Talk integration with external AI services (x.ai).
"""

import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import uvicorn

from ...core.config import get_config
from ...shared.utils import setup_logging

logger = logging.getLogger(__name__)
app = FastAPI(title="NextCraftTalk External AI")


@app.on_event("startup")
async def startup_event():
    """Initialize the external AI mode"""
    logger.info("Starting NextCraftTalk in External AI mode")


@app.post("/webhook")
async def nextcloud_webhook(request: Request):
    """
    Handle Nextcloud Talk webhooks
    """
    try:
        data = await request.json()
        logger.info(f"Received webhook: {data}")

        # TODO: Process the message and respond with AI
        # This will be implemented when we migrate NextCraftTalk-EXT code

        return {"status": "received", "message": "Processing with external AI"}

    except Exception as e:
        logger.error(f"Webhook processing error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "mode": "external_ai"}


def run_external_ai():
    """Run the external AI mode application"""
    config = get_config()

    logger.info("🚀 Starting External AI mode server")
    uvicorn.run(
        "src.modes.external_ai.main:app",
        host=config.webhook.host,
        port=config.webhook.port,
        reload=True
    )


if __name__ == "__main__":
    run_external_ai()