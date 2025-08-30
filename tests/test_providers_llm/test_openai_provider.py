"""
Unit tests for OpenAI provider implementations.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import os

from tradingagents.providers.openai_provider import OpenAILLMProvider, OpenAIEmbeddingProvider


class TestOpenAILLMProvider(unittest.TestCase):
    """Test cases for OpenAILLMProvider."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = {
            "deep_think_llm": "gpt-4",
            "quick_think_llm": "gpt-3.5-turbo",
            "backend_url": "https://api.openai.com/v1"
        }
        self.provider = OpenAILLMProvider(self.config)
    
    @patch('tradingagents.providers.openai_provider.ChatOpenAI')
    def test_get_deep_thinking_llm(self, mock_chat_openai):
        """Test getting deep thinking LLM."""
        mock_llm = Mock()
        mock_chat_openai.return_value = mock_llm
        
        result = self.provider.get_deep_thinking_llm()
        
        mock_chat_openai.assert_called_with(
            model="gpt-4",
            base_url="https://api.openai.com/v1"
        )
        self.assertEqual(result, mock_llm)
    
    @patch('tradingagents.providers.openai_provider.ChatOpenAI')
    def test_get_quick_thinking_llm(self, mock_chat_openai):
        """Test getting quick thinking LLM."""
        mock_llm = Mock()
        mock_chat_openai.return_value = mock_llm
        
        result = self.provider.get_quick_thinking_llm()
        
        mock_chat_openai.assert_called_with(
            model="gpt-3.5-turbo",
            base_url="https://api.openai.com/v1"
        )
        self.assertEqual(result, mock_llm)
    
    def test_provider_name(self):
        """Test provider name."""
        self.assertEqual(self.provider.get_provider_name(), "openaillm")


class TestOpenAIEmbeddingProvider(unittest.TestCase):
    """Test cases for OpenAIEmbeddingProvider."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = {
            "backend_url": "https://api.openai.com/v1"
        }
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    @patch('tradingagents.providers.openai_provider.OpenAI')
    def test_init_with_openai_url(self, mock_openai):
        """Test initialization with OpenAI URL."""
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        provider = OpenAIEmbeddingProvider(self.config)
        
        mock_openai.assert_called_with(
            base_url="https://api.openai.com/v1",
            api_key="test-key"
        )
        self.assertEqual(provider.client, mock_client)
        self.assertEqual(provider.embedding_model, "text-embedding-3-small")
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    @patch('tradingagents.providers.openai_provider.OpenAI')
    def test_init_with_ollama_url(self, mock_openai):
        """Test initialization with Ollama URL."""
        config = {"backend_url": "http://localhost:11434/v1"}
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        provider = OpenAIEmbeddingProvider(config)
        
        mock_openai.assert_called_with(
            base_url="http://localhost:11434/v1",
            api_key="test-key"
        )
        self.assertEqual(provider.embedding_model, "nomic-embed-text")
    
    @patch.dict(os.environ, {}, clear=True)
    @patch('tradingagents.providers.openai_provider.OpenAI')
    def test_init_without_api_key(self, mock_openai):
        """Test initialization without API key uses default."""
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        provider = OpenAIEmbeddingProvider(self.config)
        
        mock_openai.assert_called_with(
            base_url="https://api.openai.com/v1",
            api_key="test-key"
        )
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    @patch('tradingagents.providers.openai_provider.OpenAI')
    def test_get_embedding(self, mock_openai):
        """Test getting embedding."""
        # Setup mock client and response
        mock_client = Mock()
        mock_response = Mock()
        mock_response.data = [Mock(embedding=[0.1, 0.2, 0.3])]
        mock_client.embeddings.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        provider = OpenAIEmbeddingProvider(self.config)
        
        result = provider.get_embedding("test text")
        
        mock_client.embeddings.create.assert_called_with(
            model="text-embedding-3-small",
            input="test text"
        )
        self.assertEqual(result, [0.1, 0.2, 0.3])
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    @patch('tradingagents.providers.openai_provider.OpenAI')
    def test_get_embedding_model_name(self, mock_openai):
        """Test getting embedding model name."""
        provider = OpenAIEmbeddingProvider(self.config)
        self.assertEqual(provider.get_embedding_model_name(), "text-embedding-3-small")
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    @patch('tradingagents.providers.openai_provider.OpenAI')
    def test_provider_name(self, mock_openai):
        """Test provider name."""
        provider = OpenAIEmbeddingProvider(self.config)
        self.assertEqual(provider.get_provider_name(), "openai")


if __name__ == "__main__":
    unittest.main()