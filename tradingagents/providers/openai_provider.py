"""
OpenAI provider implementation.

This module provides OpenAI-specific implementations for LLM and embedding services.
"""

from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.language_models.base import BaseLanguageModel
from openai import OpenAI

from .base import LLMProvider, EmbeddingProvider


class OpenAILLMProvider(LLMProvider):
    """OpenAI LLM provider implementation."""
    
    def get_deep_thinking_llm(self) -> BaseLanguageModel:
        """Get the deep thinking OpenAI LLM instance."""
        return ChatOpenAI(
            model=self.config["deep_think_llm"],
            base_url=self.config["backend_url"]
        )
    
    def get_quick_thinking_llm(self) -> BaseLanguageModel:
        """Get the quick thinking OpenAI LLM instance."""
        return ChatOpenAI(
            model=self.config["quick_think_llm"],
            base_url=self.config["backend_url"]
        )


class OpenAIEmbeddingProvider(EmbeddingProvider):
    """OpenAI embedding provider implementation."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        
        # Set a default API key if none is provided (for testing)
        import os
        api_key = os.getenv("OPENAI_API_KEY", "test-key")
        
        self.client = OpenAI(
            base_url=config["backend_url"],
            api_key=api_key
        )
        
        # Choose embedding model based on backend URL
        if config["backend_url"] == "http://localhost:11434/v1":
            self.embedding_model = "nomic-embed-text"
        else:
            self.embedding_model = "text-embedding-3-small"
    
    def get_embedding(self, text: str) -> List[float]:
        """Get OpenAI embedding for a text string."""
        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=text
        )
        return response.data[0].embedding
    
    def get_embedding_model_name(self) -> str:
        """Get the name of the embedding model being used."""
        return self.embedding_model