"""
Factory for creating data provider instances.

This module provides a factory pattern implementation for creating and managing
different financial data provider instances based on configuration.
"""

from typing import Dict, Any, Optional

# Try absolute import first, fall back to relative import for package context
try:
    from tradingagents.dataflows.providers.base import DataProvider
    from tradingagents.dataflows.providers.finnhub_provider import FinnhubProvider
    from tradingagents.dataflows.providers.twelvedata_provider import TwelveDataProvider
except ImportError:
    from .base import DataProvider
    from .finnhub_provider import FinnhubProvider
    from .twelvedata_provider import TwelveDataProvider


class DataProviderFactory:
    """
    Factory class for creating data provider instances.
    
    This factory manages the creation and configuration of different data providers,
    allowing easy switching between providers based on configuration.
    """
    
    # Registry of available providers
    _providers = {
        "finnhub": FinnhubProvider,
        "twelvedata": TwelveDataProvider,
    }
    
    @classmethod
    def get_provider(cls, provider_name: Optional[str] = None, config: Optional[Dict[str, Any]] = None) -> DataProvider:
        """
        Create and return a data provider instance.
        
        Args:
            provider_name: Name of the provider to create. If None, uses default from config.
            config: Configuration dictionary for the provider
            
        Returns:
            DataProvider instance
            
        Raises:
            ValueError: If the provider name is not supported
        """
        if config is None:
            config = {}
        
        # Use provider_name parameter or fall back to config or default
        if provider_name is None:
            provider_name = config.get("data_provider", "finnhub")
        
        if provider_name not in cls._providers:
            available_providers = list(cls._providers.keys())
            raise ValueError(
                f"Unsupported data provider: {provider_name}. "
                f"Available providers: {available_providers}"
            )
        
        provider_class = cls._providers[provider_name]
        return provider_class(config)
    
    @classmethod
    def register_provider(cls, name: str, provider_class: type):
        """
        Register a new data provider class.
        
        Args:
            name: Name to register the provider under
            provider_class: Class that implements the DataProvider interface
            
        Raises:
            ValueError: If the provider class doesn't inherit from DataProvider
        """
        if not issubclass(provider_class, DataProvider):
            raise ValueError(f"Provider class must inherit from DataProvider")
        
        cls._providers[name] = provider_class
    
    @classmethod
    def get_available_providers(cls) -> list:
        """
        Get a list of all available provider names.
        
        Returns:
            List of provider names
        """
        return list(cls._providers.keys())
    
    @classmethod
    def create_provider_with_fallback(cls, primary_provider: str, fallback_provider: str = "finnhub", config: Optional[Dict[str, Any]] = None) -> DataProvider:
        """
        Create a provider with fallback support.
        
        Args:
            primary_provider: Primary provider to try first
            fallback_provider: Fallback provider if primary is not available
            config: Configuration dictionary for the provider
            
        Returns:
            DataProvider instance (primary if available, otherwise fallback)
        """
        if config is None:
            config = {}
        
        try:
            # Try to create primary provider
            provider = cls.get_provider(primary_provider, config)
            if provider.is_available():
                return provider
        except (ValueError, Exception) as e:
            print(f"Primary provider {primary_provider} not available: {e}")
        
        # Fall back to secondary provider
        try:
            provider = cls.get_provider(fallback_provider, config)
            print(f"Using fallback provider: {fallback_provider}")
            return provider
        except (ValueError, Exception) as e:
            raise RuntimeError(f"Both primary and fallback providers failed: {e}")