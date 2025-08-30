"""
Integration tests for the data provider system.

These tests verify that the abstract data layer integrates correctly
with the existing interface functions and maintains backward compatibility.
"""

import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta


class TestDataProviderIntegration(unittest.TestCase):
    """Integration tests for the data provider system."""

    @patch('tradingagents.dataflows.interface.DataProviderFactory.get_provider')
    def test_get_finnhub_news_uses_provider(self, mock_get_provider):
        """Test that get_finnhub_news function uses the data provider."""
        from tradingagents.dataflows.interface import get_finnhub_news
        
        # Setup mock provider
        mock_provider = MagicMock()
        mock_provider.get_news.return_value = {
            "2024-01-01": [{"headline": "Test news", "summary": "Test summary"}]
        }
        mock_get_provider.return_value = mock_provider
        
        # Call the function
        result = get_finnhub_news("AAPL", "2024-01-07", 7)
        
        # Verify provider was called (date calculation: 2024-01-07 minus 7 days = 2023-12-31)
        mock_get_provider.assert_called_once()
        mock_provider.get_news.assert_called_once_with("AAPL", "2023-12-31", "2024-01-07")
        
        # Should return non-empty result
        self.assertNotEqual(result, "")

    @patch('tradingagents.dataflows.interface.DataProviderFactory.get_provider')
    def test_get_finnhub_news_empty_result(self, mock_get_provider):
        """Test get_finnhub_news with empty provider result."""
        from tradingagents.dataflows.interface import get_finnhub_news
        
        # Setup mock provider with empty result
        mock_provider = MagicMock()
        mock_provider.get_news.return_value = {}
        mock_get_provider.return_value = mock_provider
        
        # Call the function
        result = get_finnhub_news("AAPL", "2024-01-07", 7)
        
        # Should return empty string for empty result
        self.assertEqual(result, "")

    @patch('tradingagents.dataflows.interface.DataProviderFactory.get_provider')
    def test_get_finnhub_company_insider_sentiment_uses_provider(self, mock_get_provider):
        """Test that get_finnhub_company_insider_sentiment function uses the data provider."""
        from tradingagents.dataflows.interface import get_finnhub_company_insider_sentiment
        
        # Setup mock provider
        mock_provider = MagicMock()
        mock_provider.get_insider_sentiment.return_value = {
            "2024-01-01": [{"year": 2024, "month": 1, "change": 100, "mspr": 0.5}]
        }
        mock_get_provider.return_value = mock_provider
        
        # Call the function
        result = get_finnhub_company_insider_sentiment("AAPL", "2024-01-07", 7)
        
        # Verify provider was called (date calculation: 2024-01-07 minus 7 days = 2023-12-31)
        mock_get_provider.assert_called_once()
        mock_provider.get_insider_sentiment.assert_called_once_with("AAPL", "2023-12-31", "2024-01-07")
        
        # Should return non-empty result
        self.assertNotEqual(result, "")

    @patch('tradingagents.dataflows.interface.DataProviderFactory.get_provider')
    def test_get_finnhub_company_insider_sentiment_empty_result(self, mock_get_provider):
        """Test get_finnhub_company_insider_sentiment with empty provider result."""
        from tradingagents.dataflows.interface import get_finnhub_company_insider_sentiment
        
        # Setup mock provider with empty result
        mock_provider = MagicMock()
        mock_provider.get_insider_sentiment.return_value = {}
        mock_get_provider.return_value = mock_provider
        
        # Call the function
        result = get_finnhub_company_insider_sentiment("AAPL", "2024-01-07", 7)
        
        # Should return empty string for empty result
        self.assertEqual(result, "")

    @patch('tradingagents.dataflows.interface.DataProviderFactory.get_provider')
    def test_get_finnhub_company_insider_transactions_uses_provider(self, mock_get_provider):
        """Test that get_finnhub_company_insider_transactions function uses the data provider."""
        from tradingagents.dataflows.interface import get_finnhub_company_insider_transactions
        
        # Setup mock provider
        mock_provider = MagicMock()
        mock_provider.get_insider_transactions.return_value = {
            "2024-01-01": [{"name": "John Doe", "share": 1000, "change": 500, "filingDate": "2024-01-01", "transactionPrice": 150.0, "transactionCode": "P"}]
        }
        mock_get_provider.return_value = mock_provider
        
        # Call the function
        result = get_finnhub_company_insider_transactions("AAPL", "2024-01-07", 7)
        
        # Verify provider was called (date calculation: 2024-01-07 minus 7 days = 2023-12-31)
        mock_get_provider.assert_called_once()
        mock_provider.get_insider_transactions.assert_called_once_with("AAPL", "2023-12-31", "2024-01-07")
        
        # Should return non-empty result
        self.assertNotEqual(result, "")

    @patch('tradingagents.dataflows.interface.DataProviderFactory.get_provider')
    def test_get_finnhub_company_insider_transactions_empty_result(self, mock_get_provider):
        """Test get_finnhub_company_insider_transactions with empty provider result."""
        from tradingagents.dataflows.interface import get_finnhub_company_insider_transactions
        
        # Setup mock provider with empty result
        mock_provider = MagicMock()
        mock_provider.get_insider_transactions.return_value = {}
        mock_get_provider.return_value = mock_provider
        
        # Call the function
        result = get_finnhub_company_insider_transactions("AAPL", "2024-01-07", 7)
        
        # Should return empty string for empty result
        self.assertEqual(result, "")

    def test_date_calculation_accuracy(self):
        """Test that date calculations in interface functions are accurate."""
        from tradingagents.dataflows.interface import get_finnhub_news
        
        with patch('tradingagents.dataflows.interface.DataProviderFactory.get_provider') as mock_get_provider:
            mock_provider = MagicMock()
            mock_provider.get_news.return_value = {}
            mock_get_provider.return_value = mock_provider
            
            # Test with specific date and lookback period
            current_date = "2024-01-15"
            lookback_days = 10
            
            get_finnhub_news("AAPL", current_date, lookback_days)
            
            # Verify the start date calculation
            expected_start_date = "2024-01-05"  # 2024-01-15 minus 10 days
            mock_provider.get_news.assert_called_once_with("AAPL", expected_start_date, current_date)

    @patch('tradingagents.dataflows.interface.DataProviderFactory.get_provider')
    def test_function_signatures_unchanged(self, mock_get_provider):
        """Test that the modified interface functions maintain their original signatures."""
        from tradingagents.dataflows.interface import (
            get_finnhub_news,
            get_finnhub_company_insider_sentiment,
            get_finnhub_company_insider_transactions
        )
        import inspect
        
        # Setup mock
        mock_provider = MagicMock()
        mock_provider.get_news.return_value = {}
        mock_provider.get_insider_sentiment.return_value = {}
        mock_provider.get_insider_transactions.return_value = {}
        mock_get_provider.return_value = mock_provider
        
        # Test that functions can be called with original parameters
        try:
            get_finnhub_news("AAPL", "2024-01-07", 7)
            get_finnhub_company_insider_sentiment("AAPL", "2024-01-07", 7)
            get_finnhub_company_insider_transactions("AAPL", "2024-01-07", 7)
        except TypeError as e:
            self.fail(f"Function signature changed: {e}")

    @patch('tradingagents.dataflows.interface.DataProviderFactory.get_provider')
    def test_provider_selection_from_config(self, mock_get_provider):
        """Test that the correct provider is selected based on configuration."""
        from tradingagents.dataflows.interface import get_finnhub_news
        
        mock_provider = MagicMock()
        mock_provider.get_news.return_value = {}
        mock_get_provider.return_value = mock_provider
        
        # Call function
        get_finnhub_news("AAPL", "2024-01-07", 7)
        
        # Verify factory was called without explicit provider name
        # (should use configuration)
        mock_get_provider.assert_called_once_with()

    @patch('tradingagents.dataflows.interface.DataProviderFactory.get_provider')
    def test_multiple_calls_use_same_provider_pattern(self, mock_get_provider):
        """Test that multiple interface function calls use the same provider pattern."""
        from tradingagents.dataflows.interface import (
            get_finnhub_news,
            get_finnhub_company_insider_sentiment,
            get_finnhub_company_insider_transactions
        )
        
        mock_provider = MagicMock()
        mock_provider.get_news.return_value = {}
        mock_provider.get_insider_sentiment.return_value = {}
        mock_provider.get_insider_transactions.return_value = {}
        mock_get_provider.return_value = mock_provider
        
        # Call all three functions
        get_finnhub_news("AAPL", "2024-01-07", 7)
        get_finnhub_company_insider_sentiment("AAPL", "2024-01-07", 7)
        get_finnhub_company_insider_transactions("AAPL", "2024-01-07", 7)
        
        # Each call should get a provider instance
        self.assertEqual(mock_get_provider.call_count, 3)
        
        # Each provider method should be called once
        mock_provider.get_news.assert_called_once()
        mock_provider.get_insider_sentiment.assert_called_once()
        mock_provider.get_insider_transactions.assert_called_once()


if __name__ == '__main__':
    unittest.main()