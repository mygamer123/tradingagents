"""
TwelveData provider implementation.

This module provides integration with the TwelveData API for financial data.
Includes rate limiting, error handling, and data transformation.
"""

import time
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import requests
from .base import DataProvider
from ..config import get_config

logger = logging.getLogger(__name__)


class TwelveDataProvider(DataProvider):
    """
    TwelveData provider implementation.
    
    This provider integrates with the TwelveData API to fetch financial data
    including news, insider sentiment, and insider transactions.
    """
    
    def __init__(self, data_dir: str):
        """
        Initialize the TwelveData provider.
        
        Args:
            data_dir (str): Directory where data is stored/cached
        """
        super().__init__(data_dir)
        config = get_config()
        self.api_key = config.get("twelvedata_api_key", "")
        self.base_url = "https://api.twelvedata.com"
        self.session = requests.Session()
        self.last_request_time = 0
        self.rate_limit_delay = 1.2  # Delay between requests in seconds
        
        if not self.api_key:
            logger.warning("TwelveData API key not configured. Set TWELVEDATA_API_KEY environment variable.")
    
    def _rate_limit(self):
        """Implement rate limiting between API calls."""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < self.rate_limit_delay:
            sleep_time = self.rate_limit_delay - time_since_last_request
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Make a rate-limited API request to TwelveData.
        
        Args:
            endpoint (str): API endpoint
            params (Dict[str, Any]): Request parameters
            
        Returns:
            Optional[Dict[str, Any]]: API response data or None on error
        """
        if not self.api_key:
            logger.error("TwelveData API key not configured")
            return None
        
        self._rate_limit()
        
        params["apikey"] = self.api_key
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Check for API error responses
            if isinstance(data, dict) and "status" in data and data["status"] == "error":
                logger.error(f"TwelveData API error: {data.get('message', 'Unknown error')}")
                return None
                
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"TwelveData API request failed: {e}")
            return None
        except Exception as e:
            logger.error(f"Error processing TwelveData response: {e}")
            return None
    
    def _parse_date_range(self, start_date: str, end_date: str) -> tuple:
        """
        Parse and validate date range.
        
        Args:
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format
            
        Returns:
            tuple: (start_datetime, end_datetime)
        """
        try:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            return start_dt, end_dt
        except ValueError as e:
            logger.error(f"Invalid date format: {e}")
            raise
    
    def get_news(self, ticker: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """
        Get news data from TwelveData for a company within a date range.
        
        Args:
            ticker (str): Company ticker symbol (e.g., 'AAPL')
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format
            
        Returns:
            Dict[str, Any]: News data organized by date
        """
        try:
            start_dt, end_dt = self._parse_date_range(start_date, end_date)
            
            # TwelveData news endpoint parameters
            params = {
                "symbol": ticker,
                "outputsize": 1000,  # Maximum number of articles
            }
            
            data = self._make_request("news", params)
            
            if not data or "data" not in data:
                return {}
            
            # Transform TwelveData news format to match expected format
            news_by_date = {}
            
            for article in data["data"]:
                # Parse article date
                article_date = article.get("datetime", "")
                if article_date:
                    try:
                        # TwelveData provides datetime in ISO format
                        article_dt = datetime.fromisoformat(article_date.replace("Z", "+00:00"))
                        article_date_str = article_dt.strftime("%Y-%m-%d")
                        
                        # Filter by date range
                        if start_dt <= article_dt.date() <= end_dt.date():
                            if article_date_str not in news_by_date:
                                news_by_date[article_date_str] = []
                            
                            # Transform article format
                            transformed_article = {
                                "headline": article.get("title", ""),
                                "summary": article.get("content", "")[:500],  # Truncate for consistency
                                "source": article.get("source", "TwelveData"),
                                "url": article.get("url", ""),
                                "datetime": article_date,
                            }
                            news_by_date[article_date_str].append(transformed_article)
                    except (ValueError, TypeError) as e:
                        logger.warning(f"Error parsing article date {article_date}: {e}")
                        continue
            
            return news_by_date
            
        except Exception as e:
            logger.error(f"Error fetching news from TwelveData: {e}")
            return {}
    
    def get_insider_sentiment(self, ticker: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """
        Get insider sentiment data from TwelveData for a company within a date range.
        
        Note: TwelveData doesn't provide insider sentiment endpoint directly.
        This implementation uses analyst recommendations as a proxy.
        
        Args:
            ticker (str): Company ticker symbol (e.g., 'AAPL')
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format
            
        Returns:
            Dict[str, Any]: Insider sentiment data organized by date
        """
        try:
            # Use analyst recommendations as proxy for insider sentiment
            params = {
                "symbol": ticker,
            }
            
            data = self._make_request("recommendations", params)
            
            if not data or "data" not in data:
                return {}
            
            # Transform recommendations to sentiment-like format
            sentiment_by_date = {}
            start_dt, end_dt = self._parse_date_range(start_date, end_date)
            
            for recommendation in data["data"]:
                rec_date = recommendation.get("date", "")
                if rec_date:
                    try:
                        rec_dt = datetime.strptime(rec_date, "%Y-%m-%d")
                        
                        # Filter by date range
                        if start_dt <= rec_dt <= end_dt:
                            if rec_date not in sentiment_by_date:
                                sentiment_by_date[rec_date] = {
                                    "change": 0,
                                    "mspr": 0,  # Mock sentiment score
                                }
                            
                            # Convert recommendation to sentiment score
                            rating = recommendation.get("rating", "").lower()
                            if "buy" in rating or "positive" in rating:
                                sentiment_by_date[rec_date]["mspr"] += 1
                            elif "sell" in rating or "negative" in rating:
                                sentiment_by_date[rec_date]["mspr"] -= 1
                                
                    except (ValueError, TypeError) as e:
                        logger.warning(f"Error parsing recommendation date {rec_date}: {e}")
                        continue
            
            return sentiment_by_date
            
        except Exception as e:
            logger.error(f"Error fetching insider sentiment from TwelveData: {e}")
            return {}
    
    def get_insider_transactions(self, ticker: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """
        Get insider transaction data from TwelveData for a company within a date range.
        
        Note: TwelveData doesn't provide insider transactions endpoint.
        This implementation returns structured placeholder data that could be
        extended with alternative data sources.
        
        Args:
            ticker (str): Company ticker symbol (e.g., 'AAPL')
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format
            
        Returns:
            Dict[str, Any]: Insider transaction data organized by date
        """
        try:
            # TwelveData doesn't provide insider transactions
            # This could be extended to use other data sources or APIs
            logger.info(f"Insider transactions not available from TwelveData for {ticker}")
            return {}
            
        except Exception as e:
            logger.error(f"Error fetching insider transactions from TwelveData: {e}")
            return {}
    
    def get_company_profile(self, ticker: str) -> Dict[str, Any]:
        """
        Get company profile data from TwelveData.
        
        Args:
            ticker (str): Company ticker symbol (e.g., 'AAPL')
            
        Returns:
            Dict[str, Any]: Company profile data
        """
        try:
            params = {
                "symbol": ticker,
            }
            
            data = self._make_request("profile", params)
            
            if not data:
                return {}
                
            return data
            
        except Exception as e:
            logger.error(f"Error fetching company profile from TwelveData: {e}")
            return {}