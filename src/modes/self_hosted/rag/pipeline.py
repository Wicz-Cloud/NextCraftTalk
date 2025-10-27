"""
RAG Pipeline for Self-Hosted Mode

Combines vector database retrieval with Ollama generation for enhanced responses.
"""

import logging
from typing import Any, Dict, List, Optional

from ..data.vector_db import MinecraftVectorDB
from ..ollama.client import get_ollama_client

logger = logging.getLogger(__name__)


class SelfHostedRAGPipeline:
    """RAG pipeline combining vector search with local LLM generation"""

    def __init__(
        self,
        vector_db_path: str = "./data/chroma_db",
        chroma_host: str = None,
        chroma_port: int = 8000,
    ):
        from ....core.config import get_config

        config = get_config()

        # Use config values if not provided
        if chroma_host is None and config.self_hosted:
            chroma_host = config.self_hosted.chroma_db_host or None
            chroma_port = config.self_hosted.chroma_db_port

        self.vector_db = MinecraftVectorDB(
            persist_directory=vector_db_path,
            chroma_host=chroma_host,
            chroma_port=chroma_port,
        )
        self.ollama_client = get_ollama_client()

        # RAG prompt template
        self.rag_prompt_template = """
You are a helpful AI assistant with access to relevant knowledge from a knowledge base.
Use the following context information to help answer the user's question.
If the context doesn't contain relevant information, use your general knowledge.

Context:
{context}

Question: {question}

Answer:"""

    def retrieve_context(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Retrieve relevant context from vector database"""
        try:
            results = self.vector_db.search(query, n_results=top_k)
            return results
        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            return []

    def generate_rag_response(self, query: str, context_docs: List[str]) -> Optional[str]:
        """Generate response using retrieved context"""
        try:
            # Combine context documents
            context = "\n\n".join(context_docs) if context_docs else "No relevant context found."

            # Format prompt
            prompt = self.rag_prompt_template.format(context=context, question=query)

            # Generate response with Ollama
            response = self.ollama_client.generate(prompt=prompt, temperature=0.7, top_p=0.9)

            return response

        except Exception as e:
            logger.error(f"Error generating RAG response: {e}")
            return None

    def query(self, question: str, use_rag: bool = True) -> str:
        """Main query method with optional RAG"""
        if use_rag:
            # Retrieve context and generate RAG response
            context_docs = self.retrieve_context(question)
            if context_docs:
                response = self.generate_rag_response(question, context_docs)
                if response:
                    return response

        # Fallback to direct generation
        logger.info("Using direct LLM generation (no RAG context)")
        response = self.ollama_client.generate(prompt=question, temperature=0.7)

        return response or "I apologize, but I couldn't generate a response at this time."

    def add_knowledge(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Add new knowledge to the vector database"""
        try:
            self.vector_db.add_texts([text], metadatas=[metadata] if metadata else None)
            logger.info("Added new knowledge to vector database")
        except Exception as e:
            logger.error(f"Error adding knowledge: {e}")


# Global instance
_rag_pipeline: Optional[SelfHostedRAGPipeline] = None


def get_rag_pipeline() -> SelfHostedRAGPipeline:
    """Get the global RAG pipeline instance"""
    global _rag_pipeline
    if _rag_pipeline is None:
        from ....core.config import get_config

        config = get_config()
        if config.self_hosted:
            _rag_pipeline = SelfHostedRAGPipeline(
                vector_db_path=config.self_hosted.chroma_db_path,
                chroma_host=config.self_hosted.chroma_db_host or None,
                chroma_port=config.self_hosted.chroma_db_port,
            )
        else:
            raise ValueError("Self-hosted mode not configured")
    return _rag_pipeline
