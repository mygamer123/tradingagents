"""
Abstract base classes for LLM and Embedding providers.

This module defines the interfaces that all LLM and embedding providers must implement.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from langchain_core.language_models.base import BaseLanguageModel


class LLMProvider(ABC):
    """
    Abstract base class for LLM providers.
    
    All LLM providers must implement these methods to ensure compatibility
    across different LLM services.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the LLM provider.
        
        Args:
            config (Dict[str, Any]): Configuration dictionary containing
                                   provider-specific settings
        """
        self.config = config
    
    @abstractmethod
    def get_deep_thinking_llm(self) -> BaseLanguageModel:
        """
        Get the deep thinking LLM instance.
        
        Returns:
            BaseLanguageModel: LLM instance for complex reasoning tasks
        """
        pass
    
    @abstractmethod
    def get_quick_thinking_llm(self) -> BaseLanguageModel:
        """
        Get the quick thinking LLM instance.
        
        Returns:
            BaseLanguageModel: LLM instance for fast responses
        """
        pass
    
    def get_provider_name(self) -> str:
        """
        Get the name of this provider.
        
        Returns:
            str: Provider name
        """
        return self.__class__.__name__.replace("Provider", "").lower()


class EmbeddingProvider(ABC):
    """
    Abstract base class for embedding providers.
    
    All embedding providers must implement these methods to ensure compatibility
    across different embedding services.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the embedding provider.
        
        Args:
            config (Dict[str, Any]): Configuration dictionary containing
                                   provider-specific settings
        """
        self.config = config
    
    @abstractmethod
    def get_embedding(self, text: str) -> List[float]:
        """
        Get embedding for a text string.
        
        Args:
            text (str): Text to embed
            
        Returns:
            List[float]: Embedding vector
        """
        pass
    
    @abstractmethod
    def get_embedding_model_name(self) -> str:
        """
        Get the name of the embedding model being used.
        
        Returns:
            str: Model name
        """
        pass
    
    def get_provider_name(self) -> str:
        """
        Get the name of this provider.
        
        Returns:
            str: Provider name
        """
        return self.__class__.__name__.replace("EmbeddingProvider", "").lower()