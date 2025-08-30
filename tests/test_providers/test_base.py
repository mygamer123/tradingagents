"""
Tests for the DataProvider abstract base class.
"""

import unittest
import sys
import os
from abc import ABC

# Add the project root to sys.path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from tradingagents.dataflows.providers.base import DataProvider


class TestDataProvider(unittest.TestCase):
    """Test cases for the DataProvider abstract base class."""

    def test_is_abstract_class(self):
        """Test that DataProvider is an abstract class."""
        self.assertTrue(issubclass(DataProvider, ABC))

    def test_cannot_instantiate_abstract_class(self):
        """Test that DataProvider cannot be instantiated directly."""
        with self.assertRaises(TypeError):
            DataProvider("/tmp/data")

    def test_abstract_methods_exist(self):
        """Test that all required abstract methods are defined."""
        abstract_methods = DataProvider.__abstractmethods__
        expected_methods = {
            'get_news',
            'get_insider_sentiment', 
            'get_insider_transactions'
        }
        self.assertEqual(abstract_methods, expected_methods)

    def test_concrete_implementation_works(self):
        """Test that a concrete implementation of DataProvider works."""
        
        class TestProvider(DataProvider):
            def get_news(self, ticker, start_date, end_date):
                return {"test": "news"}
            
            def get_insider_sentiment(self, ticker, start_date, end_date):
                return {"test": "sentiment"}
            
            def get_insider_transactions(self, ticker, start_date, end_date):
                return {"test": "transactions"}

        # Should be able to instantiate concrete implementation
        provider = TestProvider("/tmp/data")
        self.assertIsInstance(provider, DataProvider)
        self.assertEqual(provider.data_dir, "/tmp/data")

    def test_get_provider_name(self):
        """Test the get_provider_name method."""
        
        class MyCustomProvider(DataProvider):
            def get_news(self, ticker, start_date, end_date):
                return {}
            
            def get_insider_sentiment(self, ticker, start_date, end_date):
                return {}
            
            def get_insider_transactions(self, ticker, start_date, end_date):
                return {}

        provider = MyCustomProvider("/tmp/data")
        self.assertEqual(provider.get_provider_name(), "mycustom")

    def test_incomplete_implementation_fails(self):
        """Test that incomplete implementations cannot be instantiated."""
        
        class IncompleteProvider(DataProvider):
            def get_news(self, ticker, start_date, end_date):
                return {}
            # Missing get_insider_sentiment and get_insider_transactions

        with self.assertRaises(TypeError):
            IncompleteProvider("/tmp/data")


if __name__ == '__main__':
    unittest.main()