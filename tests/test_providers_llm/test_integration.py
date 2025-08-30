"""
Integration tests for LLM provider system.

These tests verify that the provider abstraction works correctly
with different provider configurations and maintains backward compatibility.
"""

import unittest
from unittest.mock import Mock, patch
import os

from tradingagents.providers import LLMProviderFactory, EmbeddingProviderFactory
from tradingagents.providers.openai_provider import OpenAILLMProvider, OpenAIEmbeddingProvider
from tradingagents.providers.anthropic_provider import AnthropicLLMProvider, AnthropicEmbeddingProvider
from tradingagents.providers.google_provider import GoogleLLMProvider, GoogleEmbeddingProvider


class TestProviderIntegration(unittest.TestCase):
    """Integration tests for the LLM provider system."""
    
    def test_openai_provider_integration(self):
        """Test complete OpenAI provider integration."""
        config = {
            "llm_provider": "openai",
            "deep_think_llm": "gpt-4",
            "quick_think_llm": "gpt-3.5-turbo",
            "backend_url": "https://api.openai.com/v1"
        }
        
        # Test LLM provider
        llm_provider = LLMProviderFactory.get_provider(config)
        self.assertIsInstance(llm_provider, OpenAILLMProvider)
        self.assertEqual(llm_provider.get_provider_name(), "openaillm")
        
        # Test embedding provider
        embedding_provider = EmbeddingProviderFactory.get_provider(config)
        self.assertIsInstance(embedding_provider, OpenAIEmbeddingProvider)
        self.assertEqual(embedding_provider.get_provider_name(), "openai")
    
    def test_anthropic_provider_integration(self):
        """Test complete Anthropic provider integration."""
        config = {
            "llm_provider": "anthropic",
            "deep_think_llm": "claude-3-opus-20240229",
            "quick_think_llm": "claude-3-haiku-20240307",
            "backend_url": "https://api.anthropic.com/"
        }
        
        # Test LLM provider
        llm_provider = LLMProviderFactory.get_provider(config)
        self.assertIsInstance(llm_provider, AnthropicLLMProvider)
        self.assertEqual(llm_provider.get_provider_name(), "anthropicllm")
        
        # Test embedding provider (should fall back to OpenAI)
        embedding_provider = EmbeddingProviderFactory.get_provider(config)
        self.assertIsInstance(embedding_provider, AnthropicEmbeddingProvider)
        self.assertEqual(embedding_provider.get_provider_name(), "anthropic")
    
    def test_google_provider_integration(self):
        """Test complete Google provider integration."""
        config = {
            "llm_provider": "google",
            "deep_think_llm": "gemini-pro",
            "quick_think_llm": "gemini-pro",
            "backend_url": "https://generativelanguage.googleapis.com/v1"
        }
        
        # Test LLM provider
        llm_provider = LLMProviderFactory.get_provider(config)
        self.assertIsInstance(llm_provider, GoogleLLMProvider)
        self.assertEqual(llm_provider.get_provider_name(), "googlellm")
        
        # Test embedding provider (should fall back to OpenAI)
        embedding_provider = EmbeddingProviderFactory.get_provider(config)
        self.assertIsInstance(embedding_provider, GoogleEmbeddingProvider)
        self.assertEqual(embedding_provider.get_provider_name(), "google")
    
    def test_provider_switching(self):
        """Test switching between different providers."""
        # Test switching LLM providers
        openai_config = {"llm_provider": "openai", "backend_url": "https://api.openai.com/v1"}
        anthropic_config = {"llm_provider": "anthropic", "backend_url": "https://api.anthropic.com/"}
        
        openai_provider = LLMProviderFactory.get_provider(openai_config)
        anthropic_provider = LLMProviderFactory.get_provider(anthropic_config)
        
        self.assertIsInstance(openai_provider, OpenAILLMProvider)
        self.assertIsInstance(anthropic_provider, AnthropicLLMProvider)
        self.assertNotEqual(type(openai_provider), type(anthropic_provider))
    
    def test_case_insensitive_provider_names(self):
        """Test that provider names are case insensitive."""
        configs = [
            {"llm_provider": "openai"},
            {"llm_provider": "OPENAI"},
            {"llm_provider": "OpenAI"},
            {"llm_provider": "openAI"}
        ]
        
        for config in configs:
            provider = LLMProviderFactory.get_provider(config)
            self.assertIsInstance(provider, OpenAILLMProvider)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_embedding_fallback_mechanism(self):
        """Test that non-OpenAI providers fall back to OpenAI for embeddings."""
        anthropic_config = {
            "llm_provider": "anthropic",
            "backend_url": "https://api.anthropic.com/"
        }
        
        embedding_provider = EmbeddingProviderFactory.get_provider(anthropic_config)
        
        # Should be AnthropicEmbeddingProvider but use OpenAI internally
        self.assertIsInstance(embedding_provider, AnthropicEmbeddingProvider)
        
        # Should have OpenAI embedding provider internally
        self.assertIsInstance(embedding_provider._openai_embedding_provider, OpenAIEmbeddingProvider)
        
        # Model name should indicate fallback
        model_name = embedding_provider.get_embedding_model_name()
        self.assertIn("openai-fallback", model_name)
    
    def test_ollama_provider_special_handling(self):
        """Test that Ollama provider handles local models correctly."""
        ollama_config = {
            "llm_provider": "ollama",
            "backend_url": "http://localhost:11434/v1"
        }
        
        embedding_provider = EmbeddingProviderFactory.get_provider(ollama_config)
        
        # Should use nomic-embed-text for Ollama
        model_name = embedding_provider.get_embedding_model_name()
        self.assertEqual(model_name, "nomic-embed-text")
    
    def test_provider_factory_error_handling(self):
        """Test error handling in provider factories."""
        # Test unknown LLM provider
        with self.assertRaises(ValueError) as context:
            LLMProviderFactory.get_provider({"llm_provider": "unknown"})
        self.assertIn("Unknown LLM provider 'unknown'", str(context.exception))
        
        # Test unknown embedding provider
        with self.assertRaises(ValueError) as context:
            EmbeddingProviderFactory.get_provider({"llm_provider": "unknown"})
        self.assertIn("Unknown embedding provider 'unknown'", str(context.exception))
    
    def test_backward_compatibility(self):
        """Test that the new system maintains backward compatibility."""
        # Test with configs that would have worked with the old system
        legacy_configs = [
            {
                "llm_provider": "openai",
                "deep_think_llm": "gpt-4",
                "quick_think_llm": "gpt-3.5-turbo",
                "backend_url": "https://api.openai.com/v1"
            },
            {
                "llm_provider": "anthropic",
                "deep_think_llm": "claude-3-opus-20240229",
                "quick_think_llm": "claude-3-haiku-20240307",
                "backend_url": "https://api.anthropic.com/"
            },
            {
                "llm_provider": "google",
                "deep_think_llm": "gemini-pro",
                "quick_think_llm": "gemini-pro"
            }
        ]
        
        for config in legacy_configs:
            # Should be able to create providers without errors
            llm_provider = LLMProviderFactory.get_provider(config)
            embedding_provider = EmbeddingProviderFactory.get_provider(config)
            
            self.assertIsNotNone(llm_provider)
            self.assertIsNotNone(embedding_provider)
    
    def test_all_providers_available(self):
        """Test that all expected providers are available."""
        expected_llm_providers = ["openai", "anthropic", "google", "openrouter", "ollama"]
        expected_embedding_providers = ["openai", "anthropic", "google", "openrouter", "ollama"]
        
        llm_providers = LLMProviderFactory.list_providers()
        embedding_providers = EmbeddingProviderFactory.list_providers()
        
        for provider in expected_llm_providers:
            self.assertIn(provider, llm_providers)
        
        for provider in expected_embedding_providers:
            self.assertIn(provider, embedding_providers)


if __name__ == "__main__":
    unittest.main()