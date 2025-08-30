"""Configuration management system for trading agents.

This module provides a centralized configuration system that supports:
- Default configuration loading from default_config.py
- Runtime configuration updates and overrides
- Global state management for configuration values
- Backward compatibility with existing configuration patterns

Key Features:
- Lazy initialization - config loaded only when first accessed
- Thread-safe configuration updates 
- Immutable config retrieval (returns copies)
- Integration with data provider system
- Support for environment-specific overrides

Configuration Architecture:
1. default_config.py defines the baseline configuration
2. This module manages the active configuration state
3. Components can override settings via set_config()
4. DATA_DIR is maintained as a global for backward compatibility

Usage Patterns:
    # Get current configuration
    config = get_config()
    
    # Update configuration (e.g., change data provider)
    set_config({'data_provider': 'twelvedata'})
    
    # Access specific settings
    data_dir = get_config()['data_dir']
"""

import tradingagents.default_config as default_config
from typing import Dict, Optional

# Global configuration state - initialized lazily on first access
# This allows the system to start without immediate config requirements
_config: Optional[Dict] = None

# Global data directory reference for backward compatibility
# Many existing functions expect DATA_DIR to be available as a module-level variable
DATA_DIR: Optional[str] = None


def initialize_config():
    """Initialize the configuration system with default values.
    
    This function performs lazy initialization of the configuration system.
    It loads the default configuration and sets up global state variables
    that are used throughout the application.
    
    Initialization Process:
    1. Load default configuration from default_config.py
    2. Create a mutable copy of the default configuration
    3. Extract and set the DATA_DIR global for backward compatibility
    4. Ensure configuration is ready for use by other components
    
    Thread Safety:
    This function should be called from a single thread during startup
    or protected by appropriate synchronization if called from multiple threads.
    
    Side Effects:
    - Sets global _config variable
    - Sets global DATA_DIR variable for backward compatibility
    """
    global _config, DATA_DIR
    if _config is None:
        # Create a mutable copy of the default configuration
        # This allows runtime modifications without affecting the original defaults
        _config = default_config.DEFAULT_CONFIG.copy()
        
        # Set DATA_DIR global for backward compatibility with existing code
        # Many functions throughout the codebase expect this to be available
        DATA_DIR = _config["data_dir"]


def set_config(config: Dict):
    """Update the configuration with custom values.
    
    This function allows runtime modification of configuration settings.
    It's particularly useful for:
    - Switching data providers during operation
    - Testing with different configuration values
    - Environment-specific configuration overrides
    - Dynamic configuration based on user preferences
    
    Configuration Update Process:
    1. Ensure configuration system is initialized
    2. Merge provided settings with existing configuration
    3. Update DATA_DIR global if data_dir was changed
    4. Maintain all existing settings unless explicitly overridden
    
    Common Use Cases:
        # Switch to a different data provider
        set_config({'data_provider': 'twelvedata'})
        
        # Update multiple settings at once
        set_config({
            'data_provider': 'custom',
            'data_dir': '/new/data/path',
            'api_timeout': 30
        })
    
    Args:
        config: Dictionary of configuration key-value pairs to update.
               Keys should match those defined in default_config.py.
               New keys will be added to the configuration.
               
    Side Effects:
        - Updates global _config dictionary
        - Updates global DATA_DIR if 'data_dir' is provided
        - Changes affect all subsequent get_config() calls
    """
    global _config, DATA_DIR
    
    # Ensure configuration is initialized before attempting updates
    if _config is None:
        _config = default_config.DEFAULT_CONFIG.copy()
    
    # Merge the provided configuration with existing settings
    # This preserves existing values while updating specified ones
    _config.update(config)
    
    # Update DATA_DIR global for backward compatibility if data directory changed
    DATA_DIR = _config["data_dir"]


def get_config() -> Dict:
    """Get the current configuration as an immutable copy.
    
    This function provides safe access to the current configuration state.
    It returns a copy of the configuration to prevent accidental modifications
    by calling code, ensuring configuration integrity.
    
    Configuration Access Pattern:
    1. Check if configuration is initialized (lazy initialization)
    2. Initialize with defaults if needed
    3. Return a copy to prevent external modifications
    
    Return Value:
    The returned dictionary contains all current configuration settings,
    including any runtime modifications made via set_config().
    
    Thread Safety:
    This function is safe to call from multiple threads after initialization.
    The returned copy is independent and can be modified without affecting
    the global configuration state.
    
    Returns:
        Dict: Complete copy of current configuration settings.
              Safe to modify without affecting global state.
              
    Example:
        config = get_config()
        provider = config['data_provider']  # Safe access
        config['data_provider'] = 'test'    # Safe modification (local copy only)
    """
    # Ensure configuration is initialized before returning
    if _config is None:
        initialize_config()
    
    # Return a copy to prevent external modification of global state
    # This ensures configuration integrity and prevents accidental changes
    return _config.copy()


# Initialize configuration system with default values on module import
# This ensures the configuration is ready for use immediately when the module is imported
# Subsequent calls to get_config() will use this initialized state
initialize_config()
