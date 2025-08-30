"""Data provider factory for instantiating the correct provider based on configuration.

This module implements the Factory pattern to create data provider instances dynamically
based on configuration. It provides a central registry for all available providers and
enables runtime switching between different data sources.

Key Features:
- Dynamic provider registration and instantiation
- Configuration-driven provider selection
- Extensible registry system for adding new providers
- Validation of provider implementations
- Fallback to default provider when none specified

Usage:
    # Get the default provider (typically Finnhub)
    provider = DataProviderFactory.get_provider()
    
    # Get a specific provider with configuration
    config = {'api_key': 'your_key', 'data_dir': '/path/to/data'}
    provider = DataProviderFactory.get_provider('twelvedata', config)
    
    # Register a new custom provider
    DataProviderFactory.register_provider('custom', CustomProvider)
"""

from typing import Any, Dict
from .base import DataProvider
from .finnhub_provider import FinnhubProvider
from .twelvedata_provider import TwelveDataProvider


class DataProviderFactory:
    """Factory class for creating data provider instances based on configuration.
    
    This factory manages a registry of available data providers and creates instances
    on demand. It ensures that all providers implement the correct interface and
    provides a clean abstraction for the rest of the system.
    
    The factory supports:
    - Built-in providers (Finnhub, TwelveData)
    - Custom provider registration at runtime
    - Provider validation and error handling
    - Configuration passing to provider instances
    """
    
    # Registry of available providers - maps provider names to their implementation classes
    # This acts as a plugin system where new providers can be registered dynamically
    _providers = {
        'finnhub': FinnhubProvider,      # File-based provider using local Finnhub data
        'twelvedata': TwelveDataProvider, # API-based provider (placeholder implementation)
    }
    
    @classmethod
    def get_provider(cls, provider_name: str = None, config: Dict[str, Any] = None) -> DataProvider:
        """Get a data provider instance based on the provider name.
        
        This is the main factory method that creates and returns data provider instances.
        It handles provider lookup, validation, and instantiation with proper error handling.
        
        Provider Selection Logic:
        1. Use provided provider_name if specified
        2. Fall back to 'finnhub' as the default provider
        3. Normalize provider name to lowercase for consistency
        4. Validate provider exists in registry
        5. Instantiate provider with given configuration
        
        Args:
            provider_name: Name of the provider to instantiate ('finnhub', 'twelvedata', etc.)
                          If None, defaults to 'finnhub' for backward compatibility
            config: Configuration dictionary to pass to the provider constructor.
                   Common configuration keys:
                   - 'data_dir': Path to local data files
                   - 'api_key': API authentication key  
                   - Provider-specific settings
            
        Returns:
            DataProvider instance ready for use
            
        Raises:
            ValueError: If the provider name is not supported or invalid
            
        Example:
            # Use default provider
            provider = DataProviderFactory.get_provider()
            
            # Use specific provider with config
            config = {'data_dir': '/path/to/data', 'api_key': 'key123'}
            provider = DataProviderFactory.get_provider('twelvedata', config)
        """
        # Default to finnhub for backward compatibility and stable operation
        if provider_name is None:
            provider_name = 'finnhub'
        
        # Normalize to lowercase to handle case variations (FinnHub, FINNHUB, etc.)
        provider_name = provider_name.lower()
        
        # Validate that the requested provider is available
        if provider_name not in cls._providers:
            available_providers = ', '.join(cls._providers.keys())
            raise ValueError(
                f"Unsupported provider '{provider_name}'. "
                f"Available providers: {available_providers}"
            )
        
        # Get the provider class from the registry
        provider_class = cls._providers[provider_name]
        
        # Instantiate the provider with the provided configuration
        # The provider constructor will handle config validation and setup
        return provider_class(config)
    
    @classmethod
    def register_provider(cls, name: str, provider_class: type):
        """Register a new provider class for dynamic extension.
        
        This method enables the system to be extended with new data providers at runtime.
        It's particularly useful for:
        - Adding custom providers specific to an organization
        - Testing with mock providers
        - Integrating third-party data sources
        - Creating specialized providers for specific use cases
        
        Provider Registration Requirements:
        - Provider class must inherit from DataProvider
        - Provider must implement all abstract methods
        - Provider name should be unique and descriptive
        
        Args:
            name: Unique name to register the provider under (e.g., 'alpha_vantage', 'yahoo')
                 Will be converted to lowercase for consistency
            provider_class: Provider class that implements the DataProvider interface
            
        Raises:
            ValueError: If the provider class doesn't inherit from DataProvider
            
        Example:
            # Register a custom provider
            class CustomProvider(DataProvider):
                def get_news(self, ticker, start_date, end_date):
                    # Custom implementation
                    return {}
                # ... implement other required methods
            
            DataProviderFactory.register_provider('custom', CustomProvider)
            
            # Now use the custom provider
            provider = DataProviderFactory.get_provider('custom')
        """
        # Validate that the provider follows the correct interface
        if not issubclass(provider_class, DataProvider):
            raise ValueError(
                f"Provider class {provider_class.__name__} must inherit from DataProvider. "
                f"Please ensure your provider implements all required abstract methods."
            )
        
        # Register the provider with normalized name for consistent lookup
        cls._providers[name.lower()] = provider_class
    
    @classmethod
    def get_available_providers(cls) -> list:
        """Get a list of available provider names for discovery and validation.
        
        This method is useful for:
        - Displaying available options to users
        - Validating configuration settings
        - Building dynamic UI elements
        - Testing and debugging
        
        Returns:
            List of available provider names (all lowercase)
            
        Example:
            providers = DataProviderFactory.get_available_providers()
            print(f"Available providers: {', '.join(providers)}")
            # Output: Available providers: finnhub, twelvedata
        """
        return list(cls._providers.keys())