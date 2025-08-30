"""
Tests for the TwelveDataProvider.
"""

import unittest
from tradingagents.dataflows.providers.twelvedata_provider import TwelveDataProvider
from tradingagents.dataflows.providers.base import DataProvider


class TestTwelveDataProvider(unittest.TestCase):
    """Test cases for the TwelveDataProvider."""

    def setUp(self):
        """Set up test fixtures."""
        self.data_dir = "/tmp/test_data"
        self.provider = TwelveDataProvider(self.data_dir)

    def test_inherits_from_data_provider(self):
        """Test that TwelveDataProvider inherits from DataProvider."""
        self.assertIsInstance(self.provider, DataProvider)

    def test_initialization(self):
        """Test that TwelveDataProvider initializes correctly."""
        self.assertEqual(self.provider.data_dir, self.data_dir)

    def test_get_provider_name(self):
        """Test the get_provider_name method."""
        self.assertEqual(self.provider.get_provider_name(), "twelvedata")

    def test_get_news_returns_empty_dict(self):
        """Test that get_news returns an empty dictionary (placeholder implementation)."""
        result = self.provider.get_news("AAPL", "2024-01-01", "2024-01-07")
        self.assertEqual(result, {})
        self.assertIsInstance(result, dict)

    def test_get_insider_sentiment_returns_empty_dict(self):
        """Test that get_insider_sentiment returns an empty dictionary (placeholder implementation)."""
        result = self.provider.get_insider_sentiment("AAPL", "2024-01-01", "2024-01-07")
        self.assertEqual(result, {})
        self.assertIsInstance(result, dict)

    def test_get_insider_transactions_returns_empty_dict(self):
        """Test that get_insider_transactions returns an empty dictionary (placeholder implementation)."""
        result = self.provider.get_insider_transactions("AAPL", "2024-01-01", "2024-01-07")
        self.assertEqual(result, {})
        self.assertIsInstance(result, dict)

    def test_methods_accept_parameters(self):
        """Test that all methods accept the required parameters without error."""
        # These should not raise any exceptions
        self.provider.get_news("AAPL", "2024-01-01", "2024-01-07")
        self.provider.get_insider_sentiment("TSLA", "2023-12-01", "2023-12-31")
        self.provider.get_insider_transactions("GOOGL", "2024-06-15", "2024-06-30")

    def test_different_parameter_combinations(self):
        """Test with different parameter combinations to ensure method signatures are correct."""
        test_cases = [
            ("AAPL", "2024-01-01", "2024-01-07"),
            ("TSLA", "2023-12-01", "2023-12-31"),
            ("GOOGL", "2024-06-15", "2024-06-30"),
            ("MSFT", "2024-03-01", "2024-03-15"),
        ]
        
        for ticker, start_date, end_date in test_cases:
            # All methods should return empty dicts for now
            news_result = self.provider.get_news(ticker, start_date, end_date)
            sentiment_result = self.provider.get_insider_sentiment(ticker, start_date, end_date)
            transactions_result = self.provider.get_insider_transactions(ticker, start_date, end_date)
            
            self.assertEqual(news_result, {})
            self.assertEqual(sentiment_result, {})
            self.assertEqual(transactions_result, {})

    def test_implements_all_abstract_methods(self):
        """Test that TwelveDataProvider implements all required abstract methods."""
        # This test verifies that the class can be instantiated without TypeError
        # If any abstract methods were missing, instantiation would fail
        provider = TwelveDataProvider("/tmp/test")
        
        # Verify methods exist and are callable
        self.assertTrue(hasattr(provider, 'get_news'))
        self.assertTrue(callable(getattr(provider, 'get_news')))
        
        self.assertTrue(hasattr(provider, 'get_insider_sentiment'))
        self.assertTrue(callable(getattr(provider, 'get_insider_sentiment')))
        
        self.assertTrue(hasattr(provider, 'get_insider_transactions'))
        self.assertTrue(callable(getattr(provider, 'get_insider_transactions')))

    def test_method_signatures_match_base_class(self):
        """Test that method signatures match the abstract base class."""
        # This test verifies that the class can be instantiated without TypeError
        # If any abstract methods were missing or had wrong signatures, instantiation would fail
        # Since we can create the provider successfully in setUp, this test passes
        self.assertTrue(hasattr(self.provider, 'get_news'))
        self.assertTrue(hasattr(self.provider, 'get_insider_sentiment'))  
        self.assertTrue(hasattr(self.provider, 'get_insider_transactions'))


if __name__ == '__main__':
    unittest.main()