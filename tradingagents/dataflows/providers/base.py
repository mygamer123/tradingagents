"""
Abstract base class for financial data providers.

This module defines the interface that all data providers must implement,
ensuring consistent data access patterns across different financial data sources.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class DataProvider(ABC):
    """
    Abstract base class for financial data providers.
    
    This class defines the standard interface that all data providers must implement,
    ensuring consistent data access patterns regardless of the underlying data source.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the data provider.
        
        Args:
            config: Optional configuration dictionary for the provider
        """
        self.config = config or {}
    
    @abstractmethod
    def get_news(self, ticker: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """
        Retrieve news data for a given ticker within a date range.
        
        Args:
            ticker: Ticker symbol for the company
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            Dict containing news data organized by date
        """
        pass
    
    @abstractmethod
    def get_insider_sentiment(self, ticker: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """
        Retrieve insider sentiment data for a given ticker within a date range.
        
        Args:
            ticker: Ticker symbol for the company
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            Dict containing insider sentiment data organized by date
        """
        pass
    
    @abstractmethod
    def get_insider_transactions(self, ticker: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """
        Retrieve insider transaction data for a given ticker within a date range.
        
        Args:
            ticker: Ticker symbol for the company
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            Dict containing insider transaction data organized by date
        """
        pass
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """
        Return the name of this data provider.
        
        Returns:
            String identifier for this provider
        """
        pass
    
    def is_available(self) -> bool:
        """
        Check if the data provider is available and properly configured.
        
        Returns:
            True if the provider is available, False otherwise
        """
        return True
    
    def get_supported_data_types(self) -> list:
        """
        Return a list of data types supported by this provider.
        
        Returns:
            List of supported data type strings
        """
        return ["news", "insider_sentiment", "insider_transactions"]