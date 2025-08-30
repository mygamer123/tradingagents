"""Finnhub data provider implementation.

This module provides access to pre-processed Finnhub data stored in local files.
It implements the DataProvider interface to access news, insider sentiment, and
insider transaction data from Finnhub's financial data service.

Key Features:
- File-based data access for reliable offline operation
- Efficient date-range filtering for temporal analysis  
- Robust error handling with graceful fallbacks
- Structured data formats compatible with existing workflows

Data Storage Structure:
The provider expects data to be organized in the following directory structure:
{data_dir}/finnhub_data/{data_type}/{ticker}_data_formatted.json

Where:
- data_dir: Configurable base directory for data files
- data_type: One of 'news_data', 'insider_senti', 'insider_trans'
- ticker: Company ticker symbol (e.g., 'AAPL', 'MSFT')

Data Format:
All data files contain JSON with date keys (YYYY-MM-DD) mapping to arrays of data objects.
This format enables efficient date-range queries and temporal analysis.
"""

import os
import json
from typing import Any, Dict
from .base import DataProvider


def _get_data_in_range(ticker, start_date, end_date, data_type, data_dir, period=None):
    """
    Internal utility function to retrieve Finnhub data from local files within a date range.
    
    This function handles the low-level file operations and date filtering for all data types.
    It's designed to be robust and return empty results rather than failing on missing data.
    
    Data File Location Logic:
    - Tries to find data files in the expected directory structure
    - Supports optional period parameter for time-series data variants
    - Handles missing files gracefully by returning empty dict
    
    Date Filtering Logic:
    - Filters data keys by date range (inclusive on both ends)
    - Only includes dates that have non-empty data arrays
    - Date keys must be in YYYY-MM-DD format for proper comparison
    
    Args:
        ticker: Company ticker symbol (e.g., 'AAPL')
        start_date: Start date in YYYY-MM-DD format (inclusive)
        end_date: End date in YYYY-MM-DD format (inclusive)  
        data_type: Type of data to retrieve ('news_data', 'insider_senti', 'insider_trans')
        data_dir: Base directory containing the finnhub_data folder
        period: Optional period parameter for specialized data files
        
    Returns:
        Dictionary with date keys and data arrays, filtered by date range.
        Returns empty dict {} if file not found or on any error.
        
    Error Handling:
    - FileNotFoundError: Returns {} if data file doesn't exist
    - JSONDecodeError: Returns {} if data file is corrupted
    - Any other exception: Silently handled, returns {}
    """
    # Construct the file path based on data organization convention
    if period:
        # Handle time-series data with period specifications
        data_path = os.path.join(
            data_dir,
            "finnhub_data",
            data_type,
            f"{ticker}_{period}_data_formatted.json",
        )
    else:
        # Handle standard data files without period specification
        data_path = os.path.join(
            data_dir, "finnhub_data", data_type, f"{ticker}_data_formatted.json"
        )

    try:
        # Attempt to load and parse the JSON data file
        with open(data_path, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Gracefully handle missing or corrupted files
        # This allows the system to continue operating even with incomplete data
        return {}

    # Filter data by date range and remove empty entries
    # This ensures only relevant, non-empty data is returned
    filtered_data = {}
    for key, value in data.items():
        # Check if date is within range and data is non-empty
        if start_date <= key <= end_date and len(value) > 0:
            filtered_data[key] = value
    
    return filtered_data


class FinnhubProvider(DataProvider):
    """Finnhub data provider implementation for file-based data access.
    
    This provider accesses pre-processed Finnhub data stored in local JSON files.
    It's designed for scenarios where data has been previously downloaded and processed,
    providing fast, reliable access without network dependencies.
    
    Advantages of File-Based Approach:
    - No API rate limits or network dependency
    - Consistent data format and availability
    - Fast data access for backtesting and analysis
    - Predictable performance characteristics
    
    Configuration Requirements:
    - 'data_dir': Path to directory containing finnhub_data folder
    - The data directory should follow the expected structure with processed JSON files
    
    Data Quality Assumptions:
    - Data files are properly formatted and validated
    - Date keys are in YYYY-MM-DD format
    - Data arrays contain properly structured objects
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the Finnhub provider with file system configuration.
        
        The provider requires a data directory path where Finnhub data files are stored.
        If no configuration is provided, it falls back to a default path that should
        be updated based on your deployment environment.
        
        Args:
            config: Configuration dictionary. Required keys:
                   - 'data_dir': Path to the directory containing finnhub_data folder
                   
        Note:
            The default data_dir path should be updated to match your actual data location.
            In production, this should be configured through the application configuration.
        """
        super().__init__(config)
        # Get data directory from config with fallback to default path
        # TODO: Update default path to match your actual data directory structure
        self.data_dir = self.config.get('data_dir', '/Users/yluo/Documents/Code/ScAI/FR1-data')
    
    def get_news(self, ticker: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """Retrieve news data for a company from Finnhub local files.
        
        Accesses pre-processed news data that includes headlines, summaries, and metadata
        for the specified company and date range. News data is essential for understanding
        market sentiment and identifying events that may impact stock performance.
        
        Expected Data Structure:
        - File: {data_dir}/finnhub_data/news_data/{ticker}_data_formatted.json
        - Format: {"YYYY-MM-DD": [{"headline": "...", "summary": "...", "datetime": "..."}]}
        
        Args:
            ticker: Company ticker symbol (e.g., 'AAPL', 'MSFT')
            start_date: Start date in YYYY-MM-DD format (inclusive)
            end_date: End date in YYYY-MM-DD format (inclusive)
            
        Returns:
            Dictionary with date keys and news article arrays as values.
            Each news item contains headline, summary, and timing information.
            Returns empty dict {} if no data found or file doesn't exist.
        """
        return _get_data_in_range(ticker, start_date, end_date, "news_data", self.data_dir)
    
    def get_insider_sentiment(self, ticker: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """Retrieve insider sentiment data for a company from Finnhub local files.
        
        Accesses aggregated insider trading sentiment data derived from SEC filings.
        This data provides insights into insider confidence and can be a leading indicator
        of company performance and stock price movements.
        
        Expected Data Structure:
        - File: {data_dir}/finnhub_data/insider_senti/{ticker}_data_formatted.json  
        - Format: {"YYYY-MM-DD": [{"year": 2024, "month": 1, "change": 1500, "mspr": 0.65}]}
        
        Key Metrics Included:
        - change: Net change in insider holdings (positive = net buying)
        - mspr: Monthly Share Purchase Ratio (0.0 to 1.0, higher = more bullish)
        - year/month: Time period for the aggregated data
        
        Args:
            ticker: Company ticker symbol (e.g., 'AAPL', 'MSFT')
            start_date: Start date in YYYY-MM-DD format (inclusive)
            end_date: End date in YYYY-MM-DD format (inclusive)
            
        Returns:
            Dictionary with date keys and insider sentiment arrays as values.
            Each sentiment record contains aggregated monthly insider trading metrics.
            Returns empty dict {} if no data found or file doesn't exist.
        """
        return _get_data_in_range(ticker, start_date, end_date, "insider_senti", self.data_dir)
    
    def get_insider_transactions(self, ticker: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """Retrieve insider transaction data for a company from Finnhub local files.
        
        Accesses detailed insider trading transaction records from SEC filings.
        This granular data shows individual trades by company insiders, providing
        specific insights into insider activity patterns and timing.
        
        Expected Data Structure:
        - File: {data_dir}/finnhub_data/insider_trans/{ticker}_data_formatted.json
        - Format: {"YYYY-MM-DD": [{"filingDate": "...", "name": "...", "change": -1000, ...}]}
        
        Key Transaction Details:
        - filingDate: When the transaction was filed with SEC
        - name: Name of the insider making the transaction
        - change: Share count change (negative = sale, positive = purchase)  
        - share: Total shares involved in the transaction
        - transactionPrice: Price per share for the transaction
        - transactionCode: SEC transaction code (S=Sale, P=Purchase, etc.)
        - transactionDate: When the actual transaction occurred
        
        Args:
            ticker: Company ticker symbol (e.g., 'AAPL', 'MSFT')
            start_date: Start date in YYYY-MM-DD format (inclusive)
            end_date: End date in YYYY-MM-DD format (inclusive)
            
        Returns:
            Dictionary with date keys and transaction record arrays as values.
            Each transaction contains detailed information about the insider trade.
            Returns empty dict {} if no data found or file doesn't exist.
        """
        return _get_data_in_range(ticker, start_date, end_date, "insider_trans", self.data_dir)