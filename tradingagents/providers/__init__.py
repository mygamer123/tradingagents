"""
LLM Provider abstraction layer for TradingAgents.

This package provides a clean abstraction for different LLM providers
including OpenAI, Anthropic, Google, OpenRouter, and Ollama.
"""

from .factory import LLMProviderFactory, EmbeddingProviderFactory
from .base import LLMProvider, EmbeddingProvider

__all__ = [
    "LLMProviderFactory",
    "EmbeddingProviderFactory", 
    "LLMProvider",
    "EmbeddingProvider",
]