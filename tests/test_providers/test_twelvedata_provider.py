"""
Tests for the TwelveDataProvider.
"""

import unittest
from unittest.mock import patch, Mock, MagicMock
from tradingagents.dataflows.providers.twelvedata_provider import TwelveDataProvider
from tradingagents.dataflows.providers.base import DataProvider
import time


class TestTwelveDataProvider(unittest.TestCase):
    """Test cases for the TwelveDataProvider."""

    def setUp(self):
        """Set up test fixtures."""
        self.data_dir = "/tmp/test_data"
        
        # Mock the config to avoid requiring actual API key
        with patch('tradingagents.dataflows.providers.twelvedata_provider.get_config') as mock_config:
            mock_config.return_value = {
                "twelvedata_api_key": "test_api_key_123"
            }
            self.provider = TwelveDataProvider(self.data_dir)

    def test_inherits_from_data_provider(self):
        """Test that TwelveDataProvider inherits from DataProvider."""
        self.assertIsInstance(self.provider, DataProvider)

    def test_initialization(self):
        """Test that TwelveDataProvider initializes correctly."""
        self.assertEqual(self.provider.data_dir, self.data_dir)
        self.assertEqual(self.provider.api_key, "test_api_key_123")
        self.assertEqual(self.provider.base_url, "https://api.twelvedata.com")

    def test_initialization_without_api_key(self):
        """Test initialization without API key."""
        with patch('tradingagents.dataflows.providers.twelvedata_provider.get_config') as mock_config:
            mock_config.return_value = {}
            provider = TwelveDataProvider(self.data_dir)
            self.assertEqual(provider.api_key, "")

    def test_get_provider_name(self):
        """Test the get_provider_name method."""
        self.assertEqual(self.provider.get_provider_name(), "twelvedata")

    def test_rate_limiting(self):
        """Test that rate limiting works correctly."""
        start_time = time.time()
        self.provider._rate_limit()
        first_call_time = time.time()
        
        self.provider._rate_limit()
        second_call_time = time.time()
        
        # Second call should be delayed
        time_diff = second_call_time - first_call_time
        self.assertGreaterEqual(time_diff, self.provider.rate_limit_delay * 0.9)  # Allow some tolerance

    @patch('tradingagents.dataflows.providers.twelvedata_provider.requests.Session.get')
    def test_make_request_success(self, mock_get):
        """Test successful API request."""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"status": "ok", "data": []}
        mock_get.return_value = mock_response
        
        result = self.provider._make_request("test_endpoint", {"param": "value"})
        
        self.assertEqual(result, {"status": "ok", "data": []})
        mock_get.assert_called_once()

    @patch('tradingagents.dataflows.providers.twelvedata_provider.requests.Session.get')
    def test_make_request_api_error(self, mock_get):
        """Test API error response."""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"status": "error", "message": "API limit exceeded"}
        mock_get.return_value = mock_response
        
        result = self.provider._make_request("test_endpoint", {"param": "value"})
        
        self.assertIsNone(result)

    @patch('tradingagents.dataflows.providers.twelvedata_provider.requests.Session.get')
    def test_make_request_network_error(self, mock_get):
        """Test network error handling."""
        mock_get.side_effect = Exception("Network error")
        
        result = self.provider._make_request("test_endpoint", {"param": "value"})
        
        self.assertIsNone(result)

    def test_make_request_without_api_key(self):
        """Test API request without API key."""
        self.provider.api_key = ""
        
        result = self.provider._make_request("test_endpoint", {"param": "value"})
        
        self.assertIsNone(result)

    @patch('tradingagents.dataflows.providers.twelvedata_provider.TwelveDataProvider._make_request')
    def test_get_news_success(self, mock_request):
        """Test successful news retrieval."""
        mock_request.return_value = {
            "data": [
                {
                    "title": "Test News Title",
                    "content": "Test news content",
                    "source": "Test Source",
                    "url": "https://example.com",
                    "datetime": "2024-01-15T10:30:00Z"
                }
            ]
        }
        
        result = self.provider.get_news("AAPL", "2024-01-01", "2024-01-31")
        
        self.assertIn("2024-01-15", result)
        self.assertEqual(len(result["2024-01-15"]), 1)
        self.assertEqual(result["2024-01-15"][0]["headline"], "Test News Title")

    @patch('tradingagents.dataflows.providers.twelvedata_provider.TwelveDataProvider._make_request')
    def test_get_news_empty_response(self, mock_request):
        """Test news retrieval with empty response."""
        mock_request.return_value = None
        
        result = self.provider.get_news("AAPL", "2024-01-01", "2024-01-31")
        
        self.assertEqual(result, {})

    @patch('tradingagents.dataflows.providers.twelvedata_provider.TwelveDataProvider._make_request')
    def test_get_news_invalid_date_format(self, mock_request):
        """Test news retrieval with invalid date format."""
        with self.assertRaises(ValueError):
            self.provider.get_news("AAPL", "invalid-date", "2024-01-31")

    @patch('tradingagents.dataflows.providers.twelvedata_provider.TwelveDataProvider._make_request')
    def test_get_insider_sentiment_success(self, mock_request):
        """Test successful insider sentiment retrieval."""
        mock_request.return_value = {
            "data": [
                {
                    "date": "2024-01-15",
                    "rating": "Strong Buy",
                }
            ]
        }
        
        result = self.provider.get_insider_sentiment("AAPL", "2024-01-01", "2024-01-31")
        
        self.assertIn("2024-01-15", result)
        self.assertIn("mspr", result["2024-01-15"])

    @patch('tradingagents.dataflows.providers.twelvedata_provider.TwelveDataProvider._make_request')
    def test_get_insider_sentiment_empty_response(self, mock_request):
        """Test insider sentiment retrieval with empty response."""
        mock_request.return_value = None
        
        result = self.provider.get_insider_sentiment("AAPL", "2024-01-01", "2024-01-31")
        
        self.assertEqual(result, {})

    def test_get_insider_transactions(self):
        """Test insider transactions retrieval."""
        # TwelveData doesn't provide insider transactions, should return empty
        result = self.provider.get_insider_transactions("AAPL", "2024-01-01", "2024-01-31")
        
        self.assertEqual(result, {})

    @patch('tradingagents.dataflows.providers.twelvedata_provider.TwelveDataProvider._make_request')
    def test_get_company_profile_success(self, mock_request):
        """Test successful company profile retrieval."""
        mock_request.return_value = {
            "name": "Apple Inc.",
            "country": "United States",
            "sector": "Technology"
        }
        
        result = self.provider.get_company_profile("AAPL")
        
        self.assertEqual(result["name"], "Apple Inc.")
        self.assertEqual(result["country"], "United States")

    @patch('tradingagents.dataflows.providers.twelvedata_provider.TwelveDataProvider._make_request')
    def test_get_company_profile_empty_response(self, mock_request):
        """Test company profile retrieval with empty response."""
        mock_request.return_value = None
        
        result = self.provider.get_company_profile("AAPL")
        
        self.assertEqual(result, {})

    def test_parse_date_range_valid(self):
        """Test parsing valid date range."""
        start_dt, end_dt = self.provider._parse_date_range("2024-01-01", "2024-01-31")
        
        self.assertEqual(start_dt.strftime("%Y-%m-%d"), "2024-01-01")
        self.assertEqual(end_dt.strftime("%Y-%m-%d"), "2024-01-31")

    def test_parse_date_range_invalid(self):
        """Test parsing invalid date range."""
        with self.assertRaises(ValueError):
            self.provider._parse_date_range("invalid-date", "2024-01-31")

    def test_methods_accept_parameters(self):
        """Test that all methods accept the required parameters without error."""
        # These should not raise any exceptions (though they may return empty results)
        with patch('tradingagents.dataflows.providers.twelvedata_provider.TwelveDataProvider._make_request') as mock_request:
            mock_request.return_value = None
            
            self.provider.get_news("AAPL", "2024-01-01", "2024-01-07")
            self.provider.get_insider_sentiment("TSLA", "2023-12-01", "2023-12-31")
            self.provider.get_insider_transactions("GOOGL", "2024-06-15", "2024-06-30")

    def test_implements_all_abstract_methods(self):
        """Test that TwelveDataProvider implements all required abstract methods."""
        # This test verifies that the class can be instantiated without TypeError
        # If any abstract methods were missing, instantiation would fail
        with patch('tradingagents.dataflows.providers.twelvedata_provider.get_config') as mock_config:
            mock_config.return_value = {"twelvedata_api_key": "test_key"}
            provider = TwelveDataProvider("/tmp/test")
        
        # Verify methods exist and are callable
        self.assertTrue(hasattr(provider, 'get_news'))
        self.assertTrue(callable(getattr(provider, 'get_news')))
        
        self.assertTrue(hasattr(provider, 'get_insider_sentiment'))
        self.assertTrue(callable(getattr(provider, 'get_insider_sentiment')))
        
        self.assertTrue(hasattr(provider, 'get_insider_transactions'))
        self.assertTrue(callable(getattr(provider, 'get_insider_transactions')))


if __name__ == '__main__':
    unittest.main()