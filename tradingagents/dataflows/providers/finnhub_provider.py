"""Finnhub data provider implementation."""

import os
import json
from typing import Any, Dict
from .base import DataProvider


def _get_data_in_range(ticker, start_date, end_date, data_type, data_dir, period=None):
    """
    Gets finnhub data saved and processed on disk.
    This is a local copy of the finnhub_utils function to avoid import issues.
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
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

    # filter keys (date, str in format YYYY-MM-DD) by the date range (str, str in format YYYY-MM-DD)
    filtered_data = {}
    for key, value in data.items():
        if start_date <= key <= end_date and len(value) > 0:
            filtered_data[key] = value
    return filtered_data


class FinnhubProvider(DataProvider):
    """Finnhub data provider implementation.
    
    This provider wraps the existing Finnhub functionality and provides
    a standardized interface for accessing Finnhub data.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the Finnhub provider.
        
        Args:
            config: Configuration dictionary containing data_dir and other settings
        """
        super().__init__(config)
        self.data_dir = self.config.get('data_dir', '/Users/yluo/Documents/Code/ScAI/FR1-data')
    
    def get_news(self, ticker: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """Retrieve news data for a company from Finnhub.
        
        Args:
            ticker: Company ticker symbol
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            Dictionary with date keys and news data arrays as values
        """
        return _get_data_in_range(ticker, start_date, end_date, "news_data", self.data_dir)
    
    def get_insider_sentiment(self, ticker: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """Retrieve insider sentiment data for a company from Finnhub.
        
        Args:
            ticker: Company ticker symbol
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            Dictionary with date keys and insider sentiment data arrays as values
        """
        return _get_data_in_range(ticker, start_date, end_date, "insider_senti", self.data_dir)
    
    def get_insider_transactions(self, ticker: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """Retrieve insider transaction data for a company from Finnhub.
        
        Args:
            ticker: Company ticker symbol
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            Dictionary with date keys and insider transaction data arrays as values
        """
        return _get_data_in_range(ticker, start_date, end_date, "insider_trans", self.data_dir)