"""
Tests for the DataProviderFactory.
"""

import unittest
from unittest.mock import patch, MagicMock
from tradingagents.dataflows.providers.factory import DataProviderFactory
from tradingagents.dataflows.providers.base import DataProvider
from tradingagents.dataflows.providers.finnhub_provider import FinnhubProvider
from tradingagents.dataflows.providers.twelvedata_provider import TwelveDataProvider


class TestDataProviderFactory(unittest.TestCase):
    """Test cases for the DataProviderFactory."""

    def setUp(self):
        """Set up test fixtures."""
        # Reset the factory's registry to default state
        DataProviderFactory._providers = {
            "finnhub": FinnhubProvider,
            "twelvedata": TwelveDataProvider,
        }

    @patch('tradingagents.dataflows.config.get_config')
    def test_get_provider_default_finnhub(self, mock_get_config):
        """Test getting the default provider (Finnhub)."""
        mock_get_config.return_value = {
            "data_provider": "finnhub",
            "data_dir": "/tmp/test_data"
        }
        
        provider = DataProviderFactory.get_provider()
        self.assertIsInstance(provider, FinnhubProvider)
        self.assertEqual(provider.data_dir, "/tmp/test_data")

    @patch('tradingagents.dataflows.config.get_config')
    def test_get_provider_explicit_name(self, mock_get_config):
        """Test getting a provider by explicit name."""
        mock_get_config.return_value = {
            "data_provider": "finnhub",
            "data_dir": "/tmp/test_data"
        }
        
        provider = DataProviderFactory.get_provider("twelvedata")
        self.assertIsInstance(provider, TwelveDataProvider)
        self.assertEqual(provider.data_dir, "/tmp/test_data")

    @patch('tradingagents.dataflows.config.get_config')
    def test_get_provider_with_explicit_data_dir(self, mock_get_config):
        """Test getting a provider with explicit data directory."""
        mock_get_config.return_value = {
            "data_provider": "finnhub",
            "data_dir": "/tmp/default"
        }
        
        provider = DataProviderFactory.get_provider("finnhub", "/tmp/custom")
        self.assertIsInstance(provider, FinnhubProvider)
        self.assertEqual(provider.data_dir, "/tmp/custom")

    @patch('tradingagents.dataflows.config.get_config')
    def test_get_provider_config_fallback(self, mock_get_config):
        """Test provider selection falls back to config when no provider specified."""
        mock_get_config.return_value = {
            "data_provider": "twelvedata",
            "data_dir": "/tmp/test"
        }
        
        provider = DataProviderFactory.get_provider()
        self.assertIsInstance(provider, TwelveDataProvider)

    @patch('tradingagents.dataflows.config.get_config')
    def test_get_provider_missing_config_uses_finnhub_default(self, mock_get_config):
        """Test that missing data_provider config defaults to Finnhub."""
        mock_get_config.return_value = {
            "data_dir": "/tmp/test"
            # No data_provider key
        }
        
        provider = DataProviderFactory.get_provider()
        self.assertIsInstance(provider, FinnhubProvider)

    @patch('tradingagents.dataflows.config.get_config')
    def test_get_provider_missing_data_dir_config(self, mock_get_config):
        """Test that missing data_dir config defaults to empty string."""
        mock_get_config.return_value = {
            "data_provider": "finnhub"
            # No data_dir key
        }
        
        provider = DataProviderFactory.get_provider()
        self.assertIsInstance(provider, FinnhubProvider)
        self.assertEqual(provider.data_dir, "")

    def test_get_provider_unknown_provider(self):
        """Test that requesting an unknown provider raises ValueError."""
        with self.assertRaises(ValueError) as context:
            DataProviderFactory.get_provider("unknown_provider", "/tmp/data")
        
        self.assertIn("Unknown data provider 'unknown_provider'", str(context.exception))
        self.assertIn("Available providers:", str(context.exception))

    @patch('tradingagents.dataflows.config.get_config')
    def test_get_provider_case_insensitive(self, mock_get_config):
        """Test that provider names are case-insensitive."""
        mock_get_config.return_value = {"data_dir": "/tmp/test"}
        
        provider1 = DataProviderFactory.get_provider("FINNHUB")
        provider2 = DataProviderFactory.get_provider("Finnhub")
        provider3 = DataProviderFactory.get_provider("finnhub")
        
        self.assertIsInstance(provider1, FinnhubProvider)
        self.assertIsInstance(provider2, FinnhubProvider)
        self.assertIsInstance(provider3, FinnhubProvider)

    @patch('tradingagents.dataflows.config.get_config')
    def test_get_provider_whitespace_normalization(self, mock_get_config):
        """Test that provider names are normalized (whitespace removed)."""
        mock_get_config.return_value = {"data_dir": "/tmp/test"}
        
        provider = DataProviderFactory.get_provider("  finnhub  ")
        self.assertIsInstance(provider, FinnhubProvider)

    def test_list_providers(self):
        """Test listing available providers."""
        providers = DataProviderFactory.list_providers()
        expected_providers = ["finnhub", "twelvedata"]
        self.assertEqual(set(providers), set(expected_providers))

    @patch('tradingagents.dataflows.config.get_config')
    def test_register_provider(self, mock_get_config):
        """Test registering a new provider."""
        mock_get_config.return_value = {"data_dir": "/tmp/test"}
        
        class CustomProvider(DataProvider):
            def get_news(self, ticker, start_date, end_date):
                return {}
            
            def get_insider_sentiment(self, ticker, start_date, end_date):
                return {}
            
            def get_insider_transactions(self, ticker, start_date, end_date):
                return {}

        # Register the new provider
        DataProviderFactory.register_provider("custom", CustomProvider)
        
        # Verify it's in the list
        providers = DataProviderFactory.list_providers()
        self.assertIn("custom", providers)
        
        # Verify we can get it
        provider = DataProviderFactory.get_provider("custom")
        self.assertIsInstance(provider, CustomProvider)

    def test_register_provider_invalid_class(self):
        """Test that registering an invalid provider class raises ValueError."""
        
        class NotAProvider:
            pass

        with self.assertRaises(ValueError) as context:
            DataProviderFactory.register_provider("invalid", NotAProvider)
        
        self.assertIn("Provider class must inherit from DataProvider", str(context.exception))

    @patch('tradingagents.dataflows.config.get_config')
    def test_register_provider_name_normalization(self, mock_get_config):
        """Test that provider registration normalizes names."""
        mock_get_config.return_value = {"data_dir": "/tmp/test"}
        
        class AnotherProvider(DataProvider):
            def get_news(self, ticker, start_date, end_date):
                return {}
            
            def get_insider_sentiment(self, ticker, start_date, end_date):
                return {}
            
            def get_insider_transactions(self, ticker, start_date, end_date):
                return {}

        # Register with uppercase and whitespace
        DataProviderFactory.register_provider("  ANOTHER  ", AnotherProvider)
        
        # Should be accessible with normalized name
        providers = DataProviderFactory.list_providers()
        self.assertIn("another", providers)
        
        provider = DataProviderFactory.get_provider("another")
        self.assertIsInstance(provider, AnotherProvider)


if __name__ == '__main__':
    unittest.main()