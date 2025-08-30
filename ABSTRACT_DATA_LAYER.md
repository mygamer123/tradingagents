# Abstract Data Provider System

The TradingAgents system now includes an abstract data layer that provides a clean interface for switching between different financial data providers.

## Overview

Previously, the system was tightly coupled to Finnhub as the primary data source. The new abstract data provider system allows for:

- **Easy switching** between data providers via configuration
- **Clean separation** of concerns between data access and business logic  
- **Backward compatibility** - all existing functions continue to work unchanged
- **Extensibility** - simple process to add new data providers
- **Vendor independence** - no more lock-in to a single data provider

## Architecture

### Core Components

1. **DataProvider (Abstract Base Class)** - Defines the interface all providers must implement
2. **FinnhubProvider** - Wraps existing Finnhub functionality
3. **TwelveDataProvider** - Framework for 12data integration (extensible)
4. **DataProviderFactory** - Creates provider instances based on configuration

### File Structure

```
tradingagents/dataflows/providers/
├── __init__.py                 # Package exports
├── base.py                     # DataProvider abstract base class
├── finnhub_provider.py         # Finnhub implementation  
├── twelvedata_provider.py      # TwelveData framework
└── factory.py                  # Provider factory
```

## Usage

### Configuration

Set your preferred data provider in the configuration:

```python
# In config
DATA_PROVIDER = "finnhub"  # or "twelvedata"
```

### Using Existing Functions (Backward Compatible)

All existing functions work exactly as before:

```python
# These functions now use the abstract provider layer internally
result = get_finnhub_news(ticker, curr_date, look_back_days)
sentiment = get_finnhub_company_insider_sentiment(ticker, curr_date, look_back_days)
transactions = get_finnhub_company_insider_transactions(ticker, curr_date, look_back_days)
```

### Using the Provider System Directly

For more control, use the provider system directly:

```python
from tradingagents.dataflows.providers import DataProviderFactory

# Get the configured provider
provider = DataProviderFactory.get_provider()

# Use provider methods
news = provider.get_news("AAPL", "2024-01-01", "2024-01-15")
sentiment = provider.get_insider_sentiment("AAPL", "2024-01-01", "2024-01-15")
transactions = provider.get_insider_transactions("AAPL", "2024-01-01", "2024-01-15")

# Or specify a provider explicitly
finnhub_provider = DataProviderFactory.get_provider("finnhub")
twelve_provider = DataProviderFactory.get_provider("twelvedata")
```

### Available Providers

```python
# List all available providers
providers = DataProviderFactory.list_providers()
print(providers)  # ['finnhub', 'twelvedata']
```

## Adding New Data Providers

To add a new data provider:

1. **Create the provider class** inheriting from `DataProvider`:

```python
from tradingagents.dataflows.providers.base import DataProvider

class AlphaVantageProvider(DataProvider):
    def get_news(self, ticker: str, start_date: str, end_date: str):
        # Implement Alpha Vantage news API integration
        return {}
    
    def get_insider_sentiment(self, ticker: str, start_date: str, end_date: str):
        # Implement Alpha Vantage insider sentiment
        return {}
    
    def get_insider_transactions(self, ticker: str, start_date: str, end_date: str):
        # Implement Alpha Vantage insider transactions  
        return {}
```

2. **Register the provider** with the factory:

```python
from tradingagents.dataflows.providers import DataProviderFactory

DataProviderFactory.register_provider("alphavantage", AlphaVantageProvider)
```

3. **Use the new provider**:

```python
# Set in config
DATA_PROVIDER = "alphavantage"

# Or use directly
provider = DataProviderFactory.get_provider("alphavantage")
```

## Data Format Standardization

All providers must return data in the same format:

### News Data Format
```python
{
    "2024-01-01": [
        {
            "headline": "Company Announces...",
            "summary": "Company XYZ today announced..."
        }
    ]
}
```

### Insider Sentiment Format
```python
{
    "2024-01-01": [
        {
            "year": "2024",
            "month": "01", 
            "change": 100,
            "mspr": 0.5
        }
    ]
}
```

### Insider Transactions Format
```python
{
    "2024-01-01": [
        {
            "filingDate": "2024-01-01",
            "name": "John Doe",
            "change": -100,
            "share": 1000,
            "transactionPrice": 150.0,
            "transactionCode": "S"
        }
    ]
}
```

## Migration Guide

### For Users
No changes required! All existing code continues to work exactly as before.

### For Developers
- Use `DataProviderFactory.get_provider()` for new code
- Existing functions now delegate to the provider system internally
- Configuration drives provider selection automatically

## Benefits

- **Flexibility**: Switch data providers via configuration
- **Maintainability**: Clean separation between data access and business logic
- **Testability**: Easy to mock different providers for testing
- **Extensibility**: Simple process to add new data sources
- **Reliability**: Can implement fallback mechanisms between providers
- **Backward Compatibility**: Zero breaking changes to existing code