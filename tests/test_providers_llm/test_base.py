"""
Unit tests for LLM provider base classes.
"""

import unittest
from unittest.mock import Mock, patch
from typing import Dict, Any

from tradingagents.providers.base import LLMProvider, EmbeddingProvider
from langchain_core.language_models.base import BaseLanguageModel


class MockLLMProvider(LLMProvider):
    """Mock LLM provider for testing."""
    
    def get_deep_thinking_llm(self) -> BaseLanguageModel:
        return Mock(spec=BaseLanguageModel)
    
    def get_quick_thinking_llm(self) -> BaseLanguageModel:
        return Mock(spec=BaseLanguageModel)


class MockEmbeddingProvider(EmbeddingProvider):
    """Mock embedding provider for testing."""
    
    def get_embedding(self, text: str) -> list[float]:
        return [0.1, 0.2, 0.3]
    
    def get_embedding_model_name(self) -> str:
        return "mock-embedding-model"


class TestBaseLLMProvider(unittest.TestCase):
    """Test cases for LLMProvider base class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = {"llm_provider": "mock", "deep_think_llm": "mock-deep", "quick_think_llm": "mock-quick"}
        self.provider = MockLLMProvider(self.config)
    
    def test_init(self):
        """Test provider initialization."""
        self.assertEqual(self.provider.config, self.config)
    
    def test_get_provider_name(self):
        """Test provider name generation."""
        expected_name = "mockllm"
        self.assertEqual(self.provider.get_provider_name(), expected_name)
    
    def test_abstract_methods_implemented(self):
        """Test that abstract methods are properly implemented."""
        deep_llm = self.provider.get_deep_thinking_llm()
        quick_llm = self.provider.get_quick_thinking_llm()
        
        self.assertIsNotNone(deep_llm)
        self.assertIsNotNone(quick_llm)


class TestBaseEmbeddingProvider(unittest.TestCase):
    """Test cases for EmbeddingProvider base class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = {"llm_provider": "mock"}
        self.provider = MockEmbeddingProvider(self.config)
    
    def test_init(self):
        """Test provider initialization."""
        self.assertEqual(self.provider.config, self.config)
    
    def test_get_provider_name(self):
        """Test provider name generation."""
        expected_name = "mock"
        self.assertEqual(self.provider.get_provider_name(), expected_name)
    
    def test_get_embedding(self):
        """Test embedding generation."""
        text = "test text"
        embedding = self.provider.get_embedding(text)
        
        self.assertEqual(embedding, [0.1, 0.2, 0.3])
        self.assertIsInstance(embedding, list)
    
    def test_get_embedding_model_name(self):
        """Test embedding model name retrieval."""
        model_name = self.provider.get_embedding_model_name()
        self.assertEqual(model_name, "mock-embedding-model")


if __name__ == "__main__":
    unittest.main()