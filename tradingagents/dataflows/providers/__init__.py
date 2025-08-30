"""
Data providers package for the TradingAgents system.

This package provides an abstract data layer that allows for easy switching
between different financial data providers like Finnhub, 12data, etc.
"""

# Import only the classes directly, not through dataflows init
from .factory import DataProviderFactory
from .base import DataProvider
from .finnhub_provider import FinnhubProvider
from .twelvedata_provider import TwelveDataProvider

__all__ = [
    "DataProvider",
    "DataProviderFactory", 
    "FinnhubProvider",
    "TwelveDataProvider",
]