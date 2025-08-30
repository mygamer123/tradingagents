"""
Abstract base class for data providers.

This module defines the interface that all data providers must implement.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class DataProvider(ABC):
    """
    Abstract base class for financial data providers.
    
    All data providers must implement these methods with consistent
    return formats to ensure compatibility across different data sources.
    """
    
    def __init__(self, data_dir: str):
        """
        Initialize the data provider.
        
        Args:
            data_dir (str): Directory where data is stored/cached
        """
        self.data_dir = data_dir
    
    @abstractmethod
    def get_news(self, ticker: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """
        Get news data for a company within a date range.
        
        Args:
            ticker (str): Company ticker symbol (e.g., 'AAPL')
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format
            
        Returns:
            Dict[str, Any]: News data organized by date
        """
        pass
    
    @abstractmethod
    def get_insider_sentiment(self, ticker: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """
        Get insider sentiment data for a company within a date range.
        
        Args:
            ticker (str): Company ticker symbol (e.g., 'AAPL')
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format
            
        Returns:
            Dict[str, Any]: Insider sentiment data organized by date
        """
        pass
    
    @abstractmethod
    def get_insider_transactions(self, ticker: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """
        Get insider transaction data for a company within a date range.
        
        Args:
            ticker (str): Company ticker symbol (e.g., 'AAPL')
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format
            
        Returns:
            Dict[str, Any]: Insider transaction data organized by date
        """
        pass
    
    def get_provider_name(self) -> str:
        """
        Get the name of this data provider.
        
        Returns:
            str: Provider name
        """
        return self.__class__.__name__.replace("Provider", "").lower()