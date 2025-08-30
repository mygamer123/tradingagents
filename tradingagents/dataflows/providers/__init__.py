"""Data providers package initialization.

This package implements the provider abstraction system that enables clean separation
between data sources and the interface layer. It provides a pluggable architecture
for accessing financial data from different sources like Finnhub, TwelveData, and
custom providers.

Package Structure:
- base.py: Abstract DataProvider interface defining the contract all providers must follow
- factory.py: Provider factory for instantiating and managing provider instances  
- finnhub_provider.py: File-based provider for pre-processed Finnhub data
- twelvedata_provider.py: Framework for TwelveData API integration (placeholder)

Key Design Principles:
1. Interface Segregation: Clean abstract interface that all providers implement
2. Factory Pattern: Centralized provider instantiation and management
3. Configuration-Driven: Provider selection via configuration, not code changes
4. Backward Compatibility: Seamless integration with existing codebase
5. Extensibility: Easy registration of new custom providers

Usage Examples:
    # Basic provider usage
    from .providers import DataProviderFactory
    provider = DataProviderFactory.get_provider('finnhub')
    news = provider.get_news('AAPL', '2024-01-01', '2024-01-07')
    
    # Custom provider registration
    from .providers import DataProvider, DataProviderFactory
    
    class MyProvider(DataProvider):
        def get_news(self, ticker, start_date, end_date):
            # Custom implementation
            return {}
        # ... implement other required methods
            
    DataProviderFactory.register_provider('my_provider', MyProvider)

Integration with Configuration System:
The providers work seamlessly with the configuration system to enable runtime
provider switching without code changes:

    from tradingagents.dataflows.config import set_config
    
    # Switch to a different provider
    set_config({'data_provider': 'twelvedata'})
    
    # All existing interface functions now use the new provider internally
    # No changes needed to existing calling code
"""

from .base import DataProvider
from .factory import DataProviderFactory

# Export the key classes that external code needs to interact with
# DataProvider: For implementing custom providers
# DataProviderFactory: For provider instantiation and management
__all__ = ["DataProvider", "DataProviderFactory"]