"""
OpenRouter provider implementation.

This module provides OpenRouter-specific implementations for LLM services.
OpenRouter uses OpenAI-compatible API, so we can reuse the OpenAI implementation
with different base URLs.
"""

from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.language_models.base import BaseLanguageModel

from .base import LLMProvider, EmbeddingProvider
from .openai_provider import OpenAIEmbeddingProvider


class OpenRouterLLMProvider(LLMProvider):
    """OpenRouter LLM provider implementation."""
    
    def get_deep_thinking_llm(self) -> BaseLanguageModel:
        """Get the deep thinking OpenRouter LLM instance."""
        return ChatOpenAI(
            model=self.config["deep_think_llm"],
            base_url=self.config["backend_url"]
        )
    
    def get_quick_thinking_llm(self) -> BaseLanguageModel:
        """Get the quick thinking OpenRouter LLM instance."""
        return ChatOpenAI(
            model=self.config["quick_think_llm"],
            base_url=self.config["backend_url"]
        )


class OpenRouterEmbeddingProvider(EmbeddingProvider):
    """
    OpenRouter embedding provider implementation.
    
    Since OpenRouter doesn't provide embedding services,
    this class falls back to OpenAI for embeddings.
    """
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        # Use OpenAI for embeddings since OpenRouter doesn't provide them
        # Ensure backend_url is present for OpenAI fallback
        openai_config = dict(config)
        if "backend_url" not in openai_config:
            openai_config["backend_url"] = "https://api.openai.com/v1"
        self._openai_embedding_provider = OpenAIEmbeddingProvider(openai_config)
    
    def get_embedding(self, text: str) -> List[float]:
        """Get embedding for a text string using OpenAI fallback."""
        return self._openai_embedding_provider.get_embedding(text)
    
    def get_embedding_model_name(self) -> str:
        """Get the name of the embedding model being used."""
        return f"openai-fallback-{self._openai_embedding_provider.get_embedding_model_name()}"