"""
Finnhub data provider implementation.

This module wraps the existing Finnhub functionality in the abstract provider interface.
"""

from typing import Dict, Any
from .base import DataProvider
from ..finnhub_utils import get_data_in_range


class FinnhubProvider(DataProvider):
    """
    Finnhub data provider implementation.
    
    This provider wraps the existing Finnhub functionality to fit the
    abstract provider interface while maintaining backward compatibility.
    """
    
    def get_news(self, ticker: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """
        Get news data from Finnhub for a company within a date range.
        
        Args:
            ticker (str): Company ticker symbol (e.g., 'AAPL')
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format
            
        Returns:
            Dict[str, Any]: News data organized by date
        """
        return get_data_in_range(ticker, start_date, end_date, "news_data", self.data_dir)
    
    def get_insider_sentiment(self, ticker: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """
        Get insider sentiment data from Finnhub for a company within a date range.
        
        Args:
            ticker (str): Company ticker symbol (e.g., 'AAPL')
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format
            
        Returns:
            Dict[str, Any]: Insider sentiment data organized by date
        """
        return get_data_in_range(ticker, start_date, end_date, "insider_senti", self.data_dir)
    
    def get_insider_transactions(self, ticker: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """
        Get insider transaction data from Finnhub for a company within a date range.
        
        Args:
            ticker (str): Company ticker symbol (e.g., 'AAPL')
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format
            
        Returns:
            Dict[str, Any]: Insider transaction data organized by date
        """
        return get_data_in_range(ticker, start_date, end_date, "insider_trans", self.data_dir)