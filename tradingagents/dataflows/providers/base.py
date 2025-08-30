"""Abstract base class for data providers.

This module defines the core interface that all data providers must implement
to ensure consistent data access across different data sources like Finnhub,
TwelveData, Alpha Vantage, etc.

The provider abstraction allows the system to:
- Switch between data sources without changing client code
- Maintain consistent data formats across providers
- Enable provider-specific optimizations and configurations
- Support easy extension with new data sources
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class DataProvider(ABC):
    """Abstract base class for all data providers.
    
    This class defines the standard interface that all data providers must implement
    to ensure consistent data access across different data sources. It establishes
    the contract for how data should be retrieved and formatted.
    
    Key Design Principles:
    - All providers must return data in consistent formats
    - Date ranges are specified in YYYY-MM-DD format
    - Return values are dictionaries with date keys and data arrays as values
    - Providers handle their own error conditions and return empty dicts on failure
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the data provider with configuration.
        
        The configuration dictionary can contain provider-specific settings such as:
        - API keys and authentication credentials
        - Data directory paths for file-based providers
        - Request timeouts and retry settings
        - Caching preferences
        
        Args:
            config: Provider-specific configuration dictionary. Common keys include:
                   - 'data_dir': Path to local data files (for file-based providers)
                   - 'api_key': API authentication key
                   - Various provider-specific settings
        """
        self.config = config or {}
    
    @abstractmethod
    def get_news(self, ticker: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """Retrieve news data for a company within a date range.
        
        This method fetches news articles and press releases related to the specified
        company within the given date range. News data is crucial for sentiment analysis
        and understanding market-moving events.
        
        Data Format Requirements:
        - Each news item should include headline, summary, and publication date
        - Results are grouped by date for temporal analysis
        - Empty dates (no news) should not be included in the result
        
        Args:
            ticker: Company ticker symbol (e.g., 'AAPL', 'MSFT')
            start_date: Start date in YYYY-MM-DD format (inclusive)
            end_date: End date in YYYY-MM-DD format (inclusive)
            
        Returns:
            Dictionary with date keys (YYYY-MM-DD) and news data arrays as values.
            Each news item should contain fields like 'headline', 'summary', 'datetime'.
            Returns empty dict {} if no data found or on error.
            
        Example:
            {
                "2024-01-15": [
                    {"headline": "Company Q4 Results", "summary": "...", "datetime": "..."},
                    {"headline": "New Product Launch", "summary": "...", "datetime": "..."}
                ],
                "2024-01-16": [...]
            }
        """
        pass
    
    @abstractmethod
    def get_insider_sentiment(self, ticker: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """Retrieve insider sentiment data for a company within a date range.
        
        Insider sentiment reflects the buying and selling behavior of company insiders
        (executives, directors, large shareholders) and can be a leading indicator of
        company performance. This data is typically derived from SEC filings.
        
        Data Format Requirements:
        - Monthly aggregated data showing net insider activity
        - Includes metrics like Monthly Share Purchase Ratio (MSPR)
        - Shows net change in insider holdings
        
        Args:
            ticker: Company ticker symbol (e.g., 'AAPL', 'MSFT') 
            start_date: Start date in YYYY-MM-DD format (inclusive)
            end_date: End date in YYYY-MM-DD format (inclusive)
            
        Returns:
            Dictionary with date keys (YYYY-MM-DD) and insider sentiment arrays as values.
            Each sentiment item should contain fields like 'change', 'mspr', 'year', 'month'.
            Returns empty dict {} if no data found or on error.
            
        Example:
            {
                "2024-01-15": [
                    {"year": 2024, "month": 1, "change": 1500, "mspr": 0.65}
                ]
            }
        """
        pass
    
    @abstractmethod
    def get_insider_transactions(self, ticker: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """Retrieve insider transaction data for a company within a date range.
        
        Insider transactions provide detailed information about individual trades made
        by company insiders. This granular data complements the sentiment analysis
        by showing specific transaction details, amounts, and timing.
        
        Data Format Requirements:
        - Individual transaction records with full details
        - Includes transaction type, amounts, prices, and filing dates
        - Shows insider names and their relationships to the company
        
        Args:
            ticker: Company ticker symbol (e.g., 'AAPL', 'MSFT')
            start_date: Start date in YYYY-MM-DD format (inclusive) 
            end_date: End date in YYYY-MM-DD format (inclusive)
            
        Returns:
            Dictionary with date keys (YYYY-MM-DD) and transaction arrays as values.
            Each transaction should contain fields like 'filingDate', 'name', 'change',
            'share', 'transactionPrice', 'transactionCode', 'transactionDate'.
            Returns empty dict {} if no data found or on error.
            
        Example:
            {
                "2024-01-15": [
                    {
                        "filingDate": "2024-01-15",
                        "name": "John Doe", 
                        "change": -1000,
                        "share": 5000,
                        "transactionPrice": 150.25,
                        "transactionCode": "S"
                    }
                ]
            }
        """
        pass