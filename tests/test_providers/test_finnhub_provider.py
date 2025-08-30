"""
Tests for the FinnhubProvider.
"""

import unittest
from unittest.mock import patch, MagicMock
from tradingagents.dataflows.providers.finnhub_provider import FinnhubProvider
from tradingagents.dataflows.providers.base import DataProvider


class TestFinnhubProvider(unittest.TestCase):
    """Test cases for the FinnhubProvider."""

    def setUp(self):
        """Set up test fixtures."""
        self.data_dir = "/tmp/test_data"
        self.provider = FinnhubProvider(self.data_dir)

    def test_inherits_from_data_provider(self):
        """Test that FinnhubProvider inherits from DataProvider."""
        self.assertIsInstance(self.provider, DataProvider)

    def test_initialization(self):
        """Test that FinnhubProvider initializes correctly."""
        self.assertEqual(self.provider.data_dir, self.data_dir)

    def test_get_provider_name(self):
        """Test the get_provider_name method."""
        self.assertEqual(self.provider.get_provider_name(), "finnhub")

    @patch('tradingagents.dataflows.providers.finnhub_provider.get_data_in_range')
    def test_get_news(self, mock_get_data):
        """Test the get_news method."""
        # Setup mock return value
        expected_data = {
            "2024-01-01": [{"headline": "Test news", "summary": "Test summary"}]
        }
        mock_get_data.return_value = expected_data

        # Call the method
        result = self.provider.get_news("AAPL", "2024-01-01", "2024-01-07")

        # Verify the call
        mock_get_data.assert_called_once_with(
            "AAPL", "2024-01-01", "2024-01-07", "news_data", self.data_dir
        )
        self.assertEqual(result, expected_data)

    @patch('tradingagents.dataflows.providers.finnhub_provider.get_data_in_range')
    def test_get_insider_sentiment(self, mock_get_data):
        """Test the get_insider_sentiment method."""
        # Setup mock return value
        expected_data = {
            "2024-01-01": [{"year": 2024, "month": 1, "change": 100, "mspr": 0.5}]
        }
        mock_get_data.return_value = expected_data

        # Call the method
        result = self.provider.get_insider_sentiment("AAPL", "2024-01-01", "2024-01-07")

        # Verify the call
        mock_get_data.assert_called_once_with(
            "AAPL", "2024-01-01", "2024-01-07", "insider_senti", self.data_dir
        )
        self.assertEqual(result, expected_data)

    @patch('tradingagents.dataflows.providers.finnhub_provider.get_data_in_range')
    def test_get_insider_transactions(self, mock_get_data):
        """Test the get_insider_transactions method."""
        # Setup mock return value
        expected_data = {
            "2024-01-01": [{"name": "John Doe", "share": 1000, "change": 500}]
        }
        mock_get_data.return_value = expected_data

        # Call the method
        result = self.provider.get_insider_transactions("AAPL", "2024-01-01", "2024-01-07")

        # Verify the call
        mock_get_data.assert_called_once_with(
            "AAPL", "2024-01-01", "2024-01-07", "insider_trans", self.data_dir
        )
        self.assertEqual(result, expected_data)

    @patch('tradingagents.dataflows.providers.finnhub_provider.get_data_in_range')
    def test_get_news_empty_result(self, mock_get_data):
        """Test get_news with empty result."""
        mock_get_data.return_value = {}
        
        result = self.provider.get_news("AAPL", "2024-01-01", "2024-01-07")
        
        self.assertEqual(result, {})
        mock_get_data.assert_called_once()

    @patch('tradingagents.dataflows.providers.finnhub_provider.get_data_in_range')
    def test_get_insider_sentiment_empty_result(self, mock_get_data):
        """Test get_insider_sentiment with empty result."""
        mock_get_data.return_value = {}
        
        result = self.provider.get_insider_sentiment("AAPL", "2024-01-01", "2024-01-07")
        
        self.assertEqual(result, {})
        mock_get_data.assert_called_once()

    @patch('tradingagents.dataflows.providers.finnhub_provider.get_data_in_range')
    def test_get_insider_transactions_empty_result(self, mock_get_data):
        """Test get_insider_transactions with empty result."""
        mock_get_data.return_value = {}
        
        result = self.provider.get_insider_transactions("AAPL", "2024-01-01", "2024-01-07")
        
        self.assertEqual(result, {})
        mock_get_data.assert_called_once()

    @patch('tradingagents.dataflows.providers.finnhub_provider.get_data_in_range')
    def test_method_parameters_passed_correctly(self, mock_get_data):
        """Test that all method parameters are passed correctly to underlying function."""
        mock_get_data.return_value = {}
        
        # Test various parameter combinations
        test_cases = [
            ("AAPL", "2024-01-01", "2024-01-07"),
            ("TSLA", "2023-12-01", "2023-12-31"),
            ("GOOGL", "2024-06-15", "2024-06-30"),
        ]
        
        for ticker, start_date, end_date in test_cases:
            # Reset mock
            mock_get_data.reset_mock()
            
            # Test news
            self.provider.get_news(ticker, start_date, end_date)
            mock_get_data.assert_called_with(ticker, start_date, end_date, "news_data", self.data_dir)
            
            # Reset mock
            mock_get_data.reset_mock()
            
            # Test insider sentiment
            self.provider.get_insider_sentiment(ticker, start_date, end_date)
            mock_get_data.assert_called_with(ticker, start_date, end_date, "insider_senti", self.data_dir)
            
            # Reset mock
            mock_get_data.reset_mock()
            
            # Test insider transactions
            self.provider.get_insider_transactions(ticker, start_date, end_date)
            mock_get_data.assert_called_with(ticker, start_date, end_date, "insider_trans", self.data_dir)

    @patch('tradingagents.dataflows.providers.finnhub_provider.get_data_in_range')
    def test_data_dir_passed_correctly(self, mock_get_data):
        """Test that data_dir is passed correctly to underlying function."""
        mock_get_data.return_value = {}
        
        # Test with different data directories
        test_data_dirs = ["/tmp/test1", "/tmp/test2", "/home/user/data"]
        
        for data_dir in test_data_dirs:
            provider = FinnhubProvider(data_dir)
            
            # Reset mock
            mock_get_data.reset_mock()
            
            provider.get_news("AAPL", "2024-01-01", "2024-01-07")
            mock_get_data.assert_called_with("AAPL", "2024-01-01", "2024-01-07", "news_data", data_dir)


if __name__ == '__main__':
    unittest.main()