"""
Finnhub data provider implementation.

This module implements the DataProvider interface for Finnhub data,
wrapping the existing Finnhub utilities to provide a consistent interface.
"""

import os
import json
from typing import Dict, Any, Optional

# Try absolute import first, fall back to relative import for package context
try:
    from tradingagents.dataflows.providers.base import DataProvider
except ImportError:
    from .base import DataProvider


def _get_finnhub_data_in_range(ticker, start_date, end_date, data_type, data_dir, period=None):
    """
    Gets finnhub data saved and processed on disk.
    This is a copy of the get_data_in_range function from finnhub_utils to avoid circular imports.
    """
    if period:
        data_path = os.path.join(
            data_dir,
            "finnhub_data",
            data_type,
            f"{ticker}_{period}_data_formatted.json",
        )
    else:
        data_path = os.path.join(
            data_dir, "finnhub_data", data_type, f"{ticker}_data_formatted.json"
        )

    try:
        with open(data_path, "r") as f:
            data = json.load(f)

        # filter keys (date, str in format YYYY-MM-DD) by the date range (str, str in format YYYY-MM-DD)
        filtered_data = {}
        for key, value in data.items():
            if start_date <= key <= end_date and len(value) > 0:
                filtered_data[key] = value
        return filtered_data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading Finnhub data from {data_path}: {e}")
        return {}


class FinnhubProvider(DataProvider):
    """
    Finnhub implementation of the DataProvider interface.
    
    This provider wraps the existing Finnhub utilities to provide data
    through the standardized DataProvider interface.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Finnhub provider.
        
        Args:
            config: Configuration dictionary containing data_dir and other settings
        """
        super().__init__(config)
        self.data_dir = self.config.get("data_dir", "")
        if not self.data_dir:
            raise ValueError("data_dir must be provided in config for FinnhubProvider")
    
    @property
    def provider_name(self) -> str:
        """Return the provider name."""
        return "finnhub"
    
    def get_news(self, ticker: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """
        Retrieve news data from Finnhub for a given ticker within a date range.
        
        Args:
            ticker: Ticker symbol for the company
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            Dict containing news data organized by date
        """
        try:
            return _get_finnhub_data_in_range(
                ticker=ticker,
                start_date=start_date,
                end_date=end_date,
                data_type="news_data",
                data_dir=self.data_dir
            )
        except Exception as e:
            print(f"Error retrieving news data from Finnhub: {e}")
            return {}
    
    def get_insider_sentiment(self, ticker: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """
        Retrieve insider sentiment data from Finnhub for a given ticker within a date range.
        
        Args:
            ticker: Ticker symbol for the company
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            Dict containing insider sentiment data organized by date
        """
        try:
            return _get_finnhub_data_in_range(
                ticker=ticker,
                start_date=start_date,
                end_date=end_date,
                data_type="insider_senti",
                data_dir=self.data_dir
            )
        except Exception as e:
            print(f"Error retrieving insider sentiment data from Finnhub: {e}")
            return {}
    
    def get_insider_transactions(self, ticker: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """
        Retrieve insider transaction data from Finnhub for a given ticker within a date range.
        
        Args:
            ticker: Ticker symbol for the company
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            Dict containing insider transaction data organized by date
        """
        try:
            return _get_finnhub_data_in_range(
                ticker=ticker,
                start_date=start_date,
                end_date=end_date,
                data_type="insider_trans",
                data_dir=self.data_dir
            )
        except Exception as e:
            print(f"Error retrieving insider transaction data from Finnhub: {e}")
            return {}
    
    def is_available(self) -> bool:
        """
        Check if Finnhub data is available by verifying the data directory exists.
        
        Returns:
            True if the Finnhub data directory exists, False otherwise
        """
        finnhub_data_path = os.path.join(self.data_dir, "finnhub_data")
        return os.path.exists(finnhub_data_path)
    
    def get_supported_data_types(self) -> list:
        """
        Return the data types supported by the Finnhub provider.
        
        Returns:
            List of supported data type strings
        """
        return ["news", "insider_sentiment", "insider_transactions"]