"""Data provider factory for instantiating the correct provider based on configuration."""

from typing import Any, Dict
from .base import DataProvider
from .finnhub_provider import FinnhubProvider
from .twelvedata_provider import TwelveDataProvider


class DataProviderFactory:
    """Factory class for creating data provider instances based on configuration."""
    
    # Registry of available providers
    _providers = {
        'finnhub': FinnhubProvider,
        'twelvedata': TwelveDataProvider,
    }
    
    @classmethod
    def get_provider(cls, provider_name: str = None, config: Dict[str, Any] = None) -> DataProvider:
        """Get a data provider instance based on the provider name.
        
        Args:
            provider_name: Name of the provider to instantiate ('finnhub', 'twelvedata', etc.)
            config: Configuration dictionary to pass to the provider
            
        Returns:
            DataProvider instance
            
        Raises:
            ValueError: If the provider name is not supported
        """
        if provider_name is None:
            # Default to finnhub if no provider specified
            provider_name = 'finnhub'
        
        provider_name = provider_name.lower()
        
        if provider_name not in cls._providers:
            available_providers = ', '.join(cls._providers.keys())
            raise ValueError(
                f"Unsupported provider '{provider_name}'. "
                f"Available providers: {available_providers}"
            )
        
        provider_class = cls._providers[provider_name]
        return provider_class(config)
    
    @classmethod
    def register_provider(cls, name: str, provider_class: type):
        """Register a new provider class.
        
        Args:
            name: Name to register the provider under
            provider_class: Provider class that implements DataProvider interface
        """
        if not issubclass(provider_class, DataProvider):
            raise ValueError("Provider class must inherit from DataProvider")
        
        cls._providers[name.lower()] = provider_class
    
    @classmethod
    def get_available_providers(cls) -> list:
        """Get a list of available provider names.
        
        Returns:
            List of available provider names
        """
        return list(cls._providers.keys())