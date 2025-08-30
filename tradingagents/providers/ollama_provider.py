"""
Ollama provider implementation.

This module provides Ollama-specific implementations for LLM services.
Ollama uses OpenAI-compatible API, so we can reuse the OpenAI implementation
with local base URLs.
"""

from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.language_models.base import BaseLanguageModel

from .base import LLMProvider, EmbeddingProvider
from .openai_provider import OpenAIEmbeddingProvider


class OllamaLLMProvider(LLMProvider):
    """Ollama LLM provider implementation."""
    
    def get_deep_thinking_llm(self) -> BaseLanguageModel:
        """Get the deep thinking Ollama LLM instance."""
        return ChatOpenAI(
            model=self.config["deep_think_llm"],
            base_url=self.config["backend_url"]
        )
    
    def get_quick_thinking_llm(self) -> BaseLanguageModel:
        """Get the quick thinking Ollama LLM instance."""
        return ChatOpenAI(
            model=self.config["quick_think_llm"],
            base_url=self.config["backend_url"]
        )


class OllamaEmbeddingProvider(EmbeddingProvider):
    """
    Ollama embedding provider implementation.
    
    Uses the same OpenAI-compatible API as Ollama for embeddings,
    but with local models like nomic-embed-text.
    """
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        # Use OpenAI client but with Ollama-specific embedding model
        self._openai_embedding_provider = OpenAIEmbeddingProvider(config)
    
    def get_embedding(self, text: str) -> List[float]:
        """Get embedding for a text string using Ollama."""
        return self._openai_embedding_provider.get_embedding(text)
    
    def get_embedding_model_name(self) -> str:
        """Get the name of the embedding model being used."""
        return self._openai_embedding_provider.get_embedding_model_name()