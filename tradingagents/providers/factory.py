"""
LLM and Embedding provider factories.

This module provides factory patterns for creating LLM and embedding provider instances
based on configuration.
"""

from typing import Optional, Dict, Any
from .base import LLMProvider, EmbeddingProvider
from .openai_provider import OpenAILLMProvider, OpenAIEmbeddingProvider
from .anthropic_provider import AnthropicLLMProvider, AnthropicEmbeddingProvider
from .google_provider import GoogleLLMProvider, GoogleEmbeddingProvider
from .openrouter_provider import OpenRouterLLMProvider, OpenRouterEmbeddingProvider
from .ollama_provider import OllamaLLMProvider, OllamaEmbeddingProvider


class LLMProviderFactory:
    """
    Factory class for creating LLM provider instances.
    
    This factory allows for easy switching between different LLM providers
    based on configuration settings.
    """
    
    # Registry of available LLM providers
    _providers = {
        "openai": OpenAILLMProvider,
        "anthropic": AnthropicLLMProvider,
        "google": GoogleLLMProvider,
        "openrouter": OpenRouterLLMProvider,
        "ollama": OllamaLLMProvider,
    }
    
    @classmethod
    def get_provider(cls, config: Optional[Dict[str, Any]] = None) -> LLMProvider:
        """
        Get an LLM provider instance.
        
        Args:
            config (Optional[Dict[str, Any]]): Configuration dictionary.
                                             If None, uses default config.
            
        Returns:
            LLMProvider: An instance of the requested LLM provider
            
        Raises:
            ValueError: If the provider name is not recognized
        """
        # Import config here to avoid circular imports
        if config is None:
            from ..default_config import DEFAULT_CONFIG
            config = DEFAULT_CONFIG
        
        provider_name = config.get("llm_provider", "openai").lower().strip()
        
        # Get provider class
        if provider_name not in cls._providers:
            available = ", ".join(cls._providers.keys())
            raise ValueError(f"Unknown LLM provider '{provider_name}'. Available providers: {available}")
        
        provider_class = cls._providers[provider_name]
        return provider_class(config)
    
    @classmethod
    def list_providers(cls) -> list[str]:
        """
        Get a list of available LLM provider names.
        
        Returns:
            list[str]: List of provider names
        """
        return list(cls._providers.keys())
    
    @classmethod
    def register_provider(cls, name: str, provider_class: type) -> None:
        """
        Register a new LLM provider.
        
        Args:
            name (str): Name of the provider
            provider_class (type): Provider class that inherits from LLMProvider
        """
        if not issubclass(provider_class, LLMProvider):
            raise ValueError("Provider class must inherit from LLMProvider")
        
        cls._providers[name.lower().strip()] = provider_class


class EmbeddingProviderFactory:
    """
    Factory class for creating embedding provider instances.
    
    This factory allows for easy switching between different embedding providers
    based on configuration settings.
    """
    
    # Registry of available embedding providers
    _providers = {
        "openai": OpenAIEmbeddingProvider,
        "anthropic": AnthropicEmbeddingProvider,
        "google": GoogleEmbeddingProvider,
        "openrouter": OpenRouterEmbeddingProvider,
        "ollama": OllamaEmbeddingProvider,
    }
    
    @classmethod
    def get_provider(cls, config: Optional[Dict[str, Any]] = None) -> EmbeddingProvider:
        """
        Get an embedding provider instance.
        
        Args:
            config (Optional[Dict[str, Any]]): Configuration dictionary.
                                             If None, uses default config.
            
        Returns:
            EmbeddingProvider: An instance of the requested embedding provider
            
        Raises:
            ValueError: If the provider name is not recognized
        """
        # Import config here to avoid circular imports
        if config is None:
            from ..default_config import DEFAULT_CONFIG
            config = DEFAULT_CONFIG
        
        provider_name = config.get("llm_provider", "openai").lower().strip()
        
        # Get provider class
        if provider_name not in cls._providers:
            available = ", ".join(cls._providers.keys())
            raise ValueError(f"Unknown embedding provider '{provider_name}'. Available providers: {available}")
        
        provider_class = cls._providers[provider_name]
        return provider_class(config)
    
    @classmethod
    def list_providers(cls) -> list[str]:
        """
        Get a list of available embedding provider names.
        
        Returns:
            list[str]: List of provider names
        """
        return list(cls._providers.keys())
    
    @classmethod
    def register_provider(cls, name: str, provider_class: type) -> None:
        """
        Register a new embedding provider.
        
        Args:
            name (str): Name of the provider
            provider_class (type): Provider class that inherits from EmbeddingProvider
        """
        if not issubclass(provider_class, EmbeddingProvider):
            raise ValueError("Provider class must inherit from EmbeddingProvider")
        
        cls._providers[name.lower().strip()] = provider_class