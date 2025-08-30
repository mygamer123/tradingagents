# LLM Provider Abstraction System

The TradingAgents framework now includes a clean abstraction layer for LLM APIs that provides a unified interface for switching between different LLM providers including OpenAI, Anthropic, Google, OpenRouter, and Ollama.

## Overview

Previously, the system had provider-specific conditional logic scattered throughout the codebase. The new abstract LLM provider system allows for:

- **Easy switching** between LLM providers via configuration
- **Clean separation** of concerns between LLM access and business logic  
- **Backward compatibility** - all existing configurations continue to work unchanged
- **Extensibility** - simple process to add new LLM providers
- **Vendor independence** - no more lock-in to a single LLM provider
- **Unified embedding interface** - consistent embedding API across all providers

## Architecture

### Core Components

1. **LLMProvider (Abstract Base Class)** - Defines the interface all LLM providers must implement
2. **EmbeddingProvider (Abstract Base Class)** - Defines the interface all embedding providers must implement
3. **Provider Implementations** - Concrete implementations for each supported provider
4. **LLMProviderFactory** - Creates LLM provider instances based on configuration
5. **EmbeddingProviderFactory** - Creates embedding provider instances based on configuration

### File Structure

```
tradingagents/providers/
├── __init__.py                 # Package exports
├── base.py                     # Abstract base classes
├── openai_provider.py          # OpenAI implementation  
├── anthropic_provider.py       # Anthropic implementation
├── google_provider.py          # Google implementation
├── openrouter_provider.py      # OpenRouter implementation
├── ollama_provider.py          # Ollama implementation
└── factory.py                  # Provider factories
```

## Usage

### Configuration

Set your preferred LLM provider in the configuration:

```python
# In config
config = {
    "llm_provider": "openai",  # or "anthropic", "google", "openrouter", "ollama"
    "deep_think_llm": "gpt-4",
    "quick_think_llm": "gpt-3.5-turbo",
    "backend_url": "https://api.openai.com/v1"
}
```

### Using the Provider System in Code

The TradingAgentsGraph now uses the provider system automatically:

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# The graph will automatically use the configured provider
graph = TradingAgentsGraph(config=DEFAULT_CONFIG)
```

### Using the Provider System Directly

For more control, use the provider system directly:

```python
from tradingagents.providers import LLMProviderFactory, EmbeddingProviderFactory

# Get the configured LLM provider
llm_provider = LLMProviderFactory.get_provider()
deep_thinking_llm = llm_provider.get_deep_thinking_llm()
quick_thinking_llm = llm_provider.get_quick_thinking_llm()

# Get the configured embedding provider
embedding_provider = EmbeddingProviderFactory.get_provider()
embedding = embedding_provider.get_embedding("some text")

# Or specify a provider explicitly
openai_llm_provider = LLMProviderFactory.get_provider({"llm_provider": "openai"})
anthropic_llm_provider = LLMProviderFactory.get_provider({"llm_provider": "anthropic"})
```

### Available Providers

```python
# List all available providers
llm_providers = LLMProviderFactory.list_providers()
print(llm_providers)  # ['openai', 'anthropic', 'google', 'openrouter', 'ollama']

embedding_providers = EmbeddingProviderFactory.list_providers()
print(embedding_providers)  # ['openai', 'anthropic', 'google', 'openrouter', 'ollama']
```

## Provider-Specific Configurations

### OpenAI
```python
config = {
    "llm_provider": "openai",
    "deep_think_llm": "gpt-4",
    "quick_think_llm": "gpt-3.5-turbo",
    "backend_url": "https://api.openai.com/v1"
}
```

### Anthropic
```python
config = {
    "llm_provider": "anthropic",
    "deep_think_llm": "claude-3-opus-20240229",
    "quick_think_llm": "claude-3-haiku-20240307",
    "backend_url": "https://api.anthropic.com/"
}
```

### Google
```python
config = {
    "llm_provider": "google",
    "deep_think_llm": "gemini-2.5-pro-preview-06-05",
    "quick_think_llm": "gemini-pro"
}
```

### OpenRouter
```python
config = {
    "llm_provider": "openrouter",
    "deep_think_llm": "deepseek/deepseek-chat-v3-0324:free",
    "quick_think_llm": "deepseek/deepseek-chat-v3-0324:free",
    "backend_url": "https://openrouter.ai/api/v1"
}
```

### Ollama
```python
config = {
    "llm_provider": "ollama",
    "deep_think_llm": "llama3.1",
    "quick_think_llm": "qwen3",
    "backend_url": "http://localhost:11434/v1"
}
```

## Embedding Provider Fallbacks

Since not all LLM providers offer embedding services, the system includes intelligent fallbacks:

- **OpenAI**: Uses native OpenAI embeddings (`text-embedding-3-small` or `nomic-embed-text` for Ollama)
- **Anthropic**: Falls back to OpenAI embeddings (Anthropic doesn't provide embeddings)
- **Google**: Falls back to OpenAI embeddings (Google doesn't provide embeddings via the same API)
- **OpenRouter**: Falls back to OpenAI embeddings (OpenRouter doesn't provide embeddings)
- **Ollama**: Uses OpenAI-compatible API with local models (`nomic-embed-text`)

## Adding New LLM Providers

To add a new LLM provider:

1. **Create the provider classes** inheriting from the base classes:

```python
from tradingagents.providers.base import LLMProvider, EmbeddingProvider
from langchain_core.language_models.base import BaseLanguageModel

class CustomLLMProvider(LLMProvider):
    def get_deep_thinking_llm(self) -> BaseLanguageModel:
        # Implement custom LLM integration
        return CustomLLM(model=self.config["deep_think_llm"])
    
    def get_quick_thinking_llm(self) -> BaseLanguageModel:
        # Implement custom LLM integration
        return CustomLLM(model=self.config["quick_think_llm"])

class CustomEmbeddingProvider(EmbeddingProvider):
    def get_embedding(self, text: str) -> List[float]:
        # Implement custom embedding integration
        return custom_embedding_api.embed(text)
    
    def get_embedding_model_name(self) -> str:
        return "custom-embedding-model"
```

2. **Register the providers** with the factories:

```python
from tradingagents.providers import LLMProviderFactory, EmbeddingProviderFactory

LLMProviderFactory.register_provider("custom", CustomLLMProvider)
EmbeddingProviderFactory.register_provider("custom", CustomEmbeddingProvider)
```

3. **Use the new provider**:

```python
# Set in config
config = {"llm_provider": "custom", ...}

# Or use directly
custom_provider = LLMProviderFactory.get_provider({"llm_provider": "custom"})
```

## Error Handling and Fallbacks

The provider system includes comprehensive error handling:

- **Unknown Provider**: Clear error messages with available providers listed
- **Missing Configuration**: Sensible defaults for missing configuration values
- **Provider Registration**: Validation that new providers implement required interfaces
- **Embedding Fallbacks**: Automatic fallback to OpenAI for providers without embedding support

## Migration Guide

### For Users
No changes required! All existing code continues to work exactly as before. The provider abstraction is completely transparent to existing usage.

### For Developers
- Use `LLMProviderFactory.get_provider()` for new code instead of conditional provider logic
- Use `EmbeddingProviderFactory.get_provider()` for new embedding functionality
- Configuration drives provider selection automatically
- Existing functions continue to work unchanged

## Benefits

- **Easier Provider Integration**: Adding new providers becomes a simple matter of implementing the abstract interface
- **Better Maintainability**: Provider-specific logic is isolated and easier to maintain
- **Improved Testing**: Each provider can be tested independently (37+ unit tests included)
- **Future-Proof**: The abstraction makes it easy to adapt to new LLM APIs and providers
- **Cleaner Code**: Removes conditional provider logic from business logic files
- **Flexible Configuration**: Easy switching between providers via configuration
- **Consistent Interface**: All providers expose the same methods regardless of underlying implementation

## Testing

The provider system includes comprehensive unit tests covering:

- Abstract base class validation
- Factory pattern implementation
- Provider-specific implementations
- Error handling and edge cases
- Integration scenarios
- Backward compatibility

Run the tests with:
```bash
python -m pytest tests/test_providers_llm/ -v
```

## Example: Complete Provider Switching

```python
# Example showing how easy it is to switch providers
configs = [
    {"llm_provider": "openai", "backend_url": "https://api.openai.com/v1"},
    {"llm_provider": "anthropic", "backend_url": "https://api.anthropic.com/"},
    {"llm_provider": "google"},
    {"llm_provider": "ollama", "backend_url": "http://localhost:11434/v1"}
]

for config in configs:
    print(f"Using {config['llm_provider']} provider:")
    
    # Get providers
    llm_provider = LLMProviderFactory.get_provider(config)
    embedding_provider = EmbeddingProviderFactory.get_provider(config)
    
    # Use them (same interface regardless of provider)
    deep_llm = llm_provider.get_deep_thinking_llm()
    quick_llm = llm_provider.get_quick_thinking_llm()
    embedding = embedding_provider.get_embedding("test text")
    
    print(f"  Deep LLM: {type(deep_llm).__name__}")
    print(f"  Quick LLM: {type(quick_llm).__name__}")
    print(f"  Embedding model: {embedding_provider.get_embedding_model_name()}")
```

The comprehensive provider abstraction ensures that TradingAgents is flexible, maintainable, and ready for future LLM providers while maintaining 100% backward compatibility with existing code.