"""
Unit tests for LLM provider factories.
"""

import unittest
from unittest.mock import Mock, patch
from typing import Dict, Any

from tradingagents.providers.factory import LLMProviderFactory, EmbeddingProviderFactory
from tradingagents.providers.base import LLMProvider, EmbeddingProvider
from tradingagents.providers.openai_provider import OpenAILLMProvider, OpenAIEmbeddingProvider


class TestLLMProviderFactory(unittest.TestCase):
    """Test cases for LLMProviderFactory."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_config = {
            "llm_provider": "openai",
            "deep_think_llm": "gpt-4",
            "quick_think_llm": "gpt-3.5-turbo",
            "backend_url": "https://api.openai.com/v1"
        }
    
    def test_get_openai_provider(self):
        """Test getting OpenAI provider."""
        provider = LLMProviderFactory.get_provider(self.test_config)
        
        self.assertIsInstance(provider, OpenAILLMProvider)
        self.assertEqual(provider.config, self.test_config)
    
    def test_list_providers(self):
        """Test listing available providers."""
        providers = LLMProviderFactory.list_providers()
        
        expected_providers = ["openai", "anthropic", "google", "openrouter", "ollama"]
        for provider in expected_providers:
            self.assertIn(provider, providers)
    
    def test_register_provider(self):
        """Test registering a new provider."""
        class TestProvider(LLMProvider):
            def get_deep_thinking_llm(self):
                return Mock()
            def get_quick_thinking_llm(self):
                return Mock()
        
        # Register the provider
        LLMProviderFactory.register_provider("test", TestProvider)
        
        # Check it's in the list
        self.assertIn("test", LLMProviderFactory.list_providers())
        
        # Test we can get it
        test_config = {"llm_provider": "test"}
        provider = LLMProviderFactory.get_provider(test_config)
        self.assertIsInstance(provider, TestProvider)
        
        # Clean up
        if "test" in LLMProviderFactory._providers:
            del LLMProviderFactory._providers["test"]
    
    def test_register_invalid_provider(self):
        """Test registering invalid provider raises error."""
        class NotAProvider:
            pass
        
        with self.assertRaises(ValueError):
            LLMProviderFactory.register_provider("invalid", NotAProvider)
    
    def test_unknown_provider_error(self):
        """Test error for unknown provider."""
        config = {"llm_provider": "unknown"}
        
        with self.assertRaises(ValueError) as context:
            LLMProviderFactory.get_provider(config)
        
        self.assertIn("Unknown LLM provider 'unknown'", str(context.exception))
        self.assertIn("Available providers:", str(context.exception))
    
    def test_get_provider_with_none_config(self):
        """Test getting provider with None config uses defaults."""
        # This will use the actual DEFAULT_CONFIG
        provider = LLMProviderFactory.get_provider(None)
        self.assertIsInstance(provider, LLMProvider)


class TestEmbeddingProviderFactory(unittest.TestCase):
    """Test cases for EmbeddingProviderFactory."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_config = {
            "llm_provider": "openai",
            "backend_url": "https://api.openai.com/v1"
        }
    
    def test_get_openai_embedding_provider(self):
        """Test getting OpenAI embedding provider."""
        provider = EmbeddingProviderFactory.get_provider(self.test_config)
        
        self.assertIsInstance(provider, OpenAIEmbeddingProvider)
        self.assertEqual(provider.config, self.test_config)
    
    def test_list_providers(self):
        """Test listing available embedding providers."""
        providers = EmbeddingProviderFactory.list_providers()
        
        expected_providers = ["openai", "anthropic", "google", "openrouter", "ollama"]
        for provider in expected_providers:
            self.assertIn(provider, providers)
    
    def test_register_provider(self):
        """Test registering a new embedding provider."""
        class TestEmbeddingProvider(EmbeddingProvider):
            def get_embedding(self, text: str):
                return [0.1, 0.2, 0.3]
            def get_embedding_model_name(self):
                return "test-model"
        
        # Register the provider
        EmbeddingProviderFactory.register_provider("test", TestEmbeddingProvider)
        
        # Check it's in the list
        self.assertIn("test", EmbeddingProviderFactory.list_providers())
        
        # Test we can get it
        test_config = {"llm_provider": "test"}
        provider = EmbeddingProviderFactory.get_provider(test_config)
        self.assertIsInstance(provider, TestEmbeddingProvider)
        
        # Clean up
        if "test" in EmbeddingProviderFactory._providers:
            del EmbeddingProviderFactory._providers["test"]
    
    def test_register_invalid_provider(self):
        """Test registering invalid embedding provider raises error."""
        class NotAnEmbeddingProvider:
            pass
        
        with self.assertRaises(ValueError):
            EmbeddingProviderFactory.register_provider("invalid", NotAnEmbeddingProvider)
    
    def test_unknown_provider_error(self):
        """Test error for unknown embedding provider."""
        config = {"llm_provider": "unknown"}
        
        with self.assertRaises(ValueError) as context:
            EmbeddingProviderFactory.get_provider(config)
        
        self.assertIn("Unknown embedding provider 'unknown'", str(context.exception))
        self.assertIn("Available providers:", str(context.exception))


if __name__ == "__main__":
    unittest.main()