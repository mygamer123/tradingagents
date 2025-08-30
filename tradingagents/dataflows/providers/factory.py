"""
Data provider factory.

This module provides the factory pattern for creating data provider instances
based on configuration.
"""

from typing import Optional
from .base import DataProvider
from .finnhub_provider import FinnhubProvider
from .twelvedata_provider import TwelveDataProvider


class DataProviderFactory:
    """
    Factory class for creating data provider instances.
    
    This factory allows for easy switching between different data providers
    based on configuration settings.
    """
    
    # Registry of available providers
    _providers = {
        "finnhub": FinnhubProvider,
        "twelvedata": TwelveDataProvider,
    }
    
    @classmethod
    def get_provider(cls, provider_name: Optional[str] = None, data_dir: Optional[str] = None) -> DataProvider:
        """
        Get a data provider instance.
        
        Args:
            provider_name (Optional[str]): Name of the provider to create.
                                         If None, uses config or defaults to "finnhub"
            data_dir (Optional[str]): Data directory path. If None, uses config.
            
        Returns:
            DataProvider: An instance of the requested data provider
            
        Raises:
            ValueError: If the provider name is not recognized
        """
        # Import config here to avoid circular imports
        from ..config import get_config
        
        config = get_config()
        
        # Use provided values or fall back to config
        if provider_name is None:
            provider_name = config.get("data_provider", "finnhub")
        
        if data_dir is None:
            data_dir = config.get("data_dir", "")
        
        # Normalize provider name
        provider_name = provider_name.lower().strip()
        
        # Get provider class
        if provider_name not in cls._providers:
            available = ", ".join(cls._providers.keys())
            raise ValueError(f"Unknown data provider '{provider_name}'. Available providers: {available}")
        
        provider_class = cls._providers[provider_name]
        return provider_class(data_dir)
    
    @classmethod
    def list_providers(cls) -> list[str]:
        """
        Get a list of available data provider names.
        
        Returns:
            list[str]: List of provider names
        """
        return list(cls._providers.keys())
    
    @classmethod
    def register_provider(cls, name: str, provider_class: type) -> None:
        """
        Register a new data provider.
        
        Args:
            name (str): Name of the provider
            provider_class (type): Provider class that inherits from DataProvider
        """
        if not issubclass(provider_class, DataProvider):
            raise ValueError("Provider class must inherit from DataProvider")
        
        cls._providers[name.lower().strip()] = provider_class