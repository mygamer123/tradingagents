"""Abstract base class for data providers."""

from abc import ABC, abstractmethod
from typing import Any, Dict


class DataProvider(ABC):
    """Abstract base class for all data providers.
    
    This class defines the standard interface that all data providers must implement
    to ensure consistent data access across different data sources.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the data provider with configuration.
        
        Args:
            config: Provider-specific configuration dictionary
        """
        self.config = config or {}
    
    @abstractmethod
    def get_news(self, ticker: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """Retrieve news data for a company within a date range.
        
        Args:
            ticker: Company ticker symbol
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            Dictionary with date keys and news data arrays as values
        """
        pass
    
    @abstractmethod
    def get_insider_sentiment(self, ticker: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """Retrieve insider sentiment data for a company within a date range.
        
        Args:
            ticker: Company ticker symbol
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            Dictionary with date keys and insider sentiment data arrays as values
        """
        pass
    
    @abstractmethod
    def get_insider_transactions(self, ticker: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """Retrieve insider transaction data for a company within a date range.
        
        Args:
            ticker: Company ticker symbol
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            Dictionary with date keys and insider transaction data arrays as values
        """
        pass