"""
NextCraftTalk Self-Hosted Mode

Handles Nextcloud Talk integration with self-hosted AI stack (Ollama + ChromaDB + RAG).
"""

import logging

import uvicorn
from fastapi import FastAPI, HTTPException, Request

from ...core.config import get_config
from .rag.pipeline import get_rag_pipeline

logger = logging.getLogger(__name__)
app = FastAPI(title="NextCraftTalk Self-Hosted")


@app.on_event("startup")
async def startup_event():
    """Initialize the self-hosted mode"""
    logger.info("🚀 Initializing NextCraftTalk Self-Hosted mode")

    try:
        # Initialize RAG pipeline (this will set up Ollama and ChromaDB)
        get_rag_pipeline()
        logger.info("✅ RAG pipeline initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize RAG pipeline: {e}")
        logger.warning("Self-hosted mode may not function properly")


@app.post("/webhook")
async def nextcloud_webhook(request: Request):
    """
    Handle Nextcloud Talk webhooks with self-hosted AI
    """
    try:
        data = await request.json()
        logger.info(f"Received webhook: {data}")

        # Extract message
        message = data.get("message", "")
        if not message:
            return {"status": "ignored", "reason": "no message content"}

        # Get AI response using RAG pipeline
        rag_pipeline = get_rag_pipeline()
        ai_response = rag_pipeline.query(message)

        # TODO: Send response back to Nextcloud Talk
        # This will be implemented when we integrate the Nextcloud API

        return {
            "status": "processed",
            "message": message,
            "ai_response": ai_response,
            "mode": "self_hosted",
        }

    except Exception as e:
        logger.error(f"Webhook processing error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test RAG pipeline
        get_rag_pipeline()
        return {
            "status": "healthy",
            "mode": "self_hosted",
            "components": {
                "ollama": "available",
                "chromadb": "available",
                "rag_pipeline": "ready",
            },
        }
    except Exception as e:
        return {"status": "degraded", "mode": "self_hosted", "error": str(e)}


@app.post("/knowledge/add")
async def add_knowledge(request: Request):
    """Add new knowledge to the vector database"""
    try:
        data = await request.json()
        text = data.get("text", "")
        metadata = data.get("metadata", {})

        if not text:
            raise HTTPException(status_code=400, detail="Text content required")

        rag_pipeline = get_rag_pipeline()
        rag_pipeline.add_knowledge(text, metadata)

        return {"status": "added", "message": "Knowledge added to vector database"}

    except Exception as e:
        logger.error(f"Error adding knowledge: {e}")
        raise HTTPException(status_code=500, detail="Failed to add knowledge")


def run_self_hosted():
    """Run the self-hosted mode application"""
    config = get_config()

    logger.info("🚀 Starting NextCraftTalk in Self-Hosted mode")

    # Check if we have the required self-hosted configuration
    if not config.self_hosted:
        logger.error("Self-hosted mode requires DEPLOYMENT_MODE=self_hosted in .env")
        logger.error(
            "Please configure Ollama, ChromaDB, and other self-hosted settings"
        )
        return

    logger.info("📚 Self-hosted AI stack components:")
    logger.info(f"   - Ollama URL: {config.self_hosted.ollama_base_url}")
    logger.info(f"   - Ollama Model: {config.self_hosted.ollama_model}")
    logger.info(f"   - ChromaDB Path: {config.self_hosted.chroma_db_path}")
    logger.info(f"   - Wiki Base URL: {config.self_hosted.wiki_base_url}")

    logger.info("🤖 Starting self-hosted FastAPI server")
    uvicorn.run(
        "src.modes.self_hosted.main:app",
        host=config.webhook.host,
        port=8080,  # Fixed internal port for container
        reload=True,
    )


if __name__ == "__main__":
    run_self_hosted()
