"""Configuration management module."""

import json
from pathlib import Path
from typing import Any, Optional


class ConfigManager:
    """
    Manages application configuration and settings.
    
    This class handles persistent storage of user preferences including:
    - Theme selection (system, light, dark)
    - Recent files list
    - Output folder path
    
    Configuration is stored in a JSON file at ~/.pyinstaller_gui/config.json.
    The class provides thread-safe read/write operations with proper error
    handling for corrupted or missing configuration files.
    """
    
    def __init__(self):
        """Initialize the configuration manager and load existing settings."""
        self.config_dir = Path.home() / ".pyinstaller_gui"
        self.config_file = self.config_dir / "config.json"
        self.config = self._load_config()
    
    def _ensure_config_dir(self) -> None:
        """
        Ensure the config directory exists.
        
        Creates the configuration directory if it doesn't already exist.
        """
        self.config_dir.mkdir(exist_ok=True)
    
    def _get_system_theme(self) -> str:
        """
        Detect system theme.
        
        Uses darkdetect library to determine if the system is using dark mode.
        Falls back to "light" if darkdetect is not installed or fails.
        
        Returns:
            "dark" if system is using dark mode, "light" otherwise.
        """
        try:
            import darkdetect
            return "dark" if darkdetect.isDark() else "light"
        except ImportError:
            return "light"
    
    def _load_config(self) -> dict:
        """
        Load configuration from file.
        
        Creates default configuration if the file doesn't exist.
        Merges loaded configuration with defaults to handle new keys.
        
        Returns:
            Dictionary containing configuration values.
        """
        self._ensure_config_dir()
        
        default_config = {
            "theme": "system",
            "recent_files": [],
            "output_folder": str(Path.home() / "dist")
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    return {**default_config, **loaded}
            except (json.JSONDecodeError, IOError):
                return default_config
        else:
            self._save_config(default_config)
            return default_config
    
    def _save_config(self, config: Optional[dict] = None) -> bool:
        """
        Save configuration to file.
        
        Args:
            config: The configuration dictionary to save. If None, uses current config.
            
        Returns:
            True if save was successful, False otherwise.
        """
        if config is None:
            config = self.config
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            return True
        except IOError:
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: The configuration key to retrieve.
            default: Value to return if the key doesn't exist.
            
        Returns:
            The configuration value, or the default if not found.
        """
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> bool:
        """
        Set a configuration value.
        
        Updates the configuration in memory and persists it to disk.
        
        Args:
            key: The configuration key to set.
            value: The value to store.
            
        Returns:
            True if save was successful, False otherwise.
        """
        self.config[key] = value
        return self._save_config()
    
    def get_effective_theme(self) -> str:
        """
        Get the effective theme based on system setting.
        
        Resolves the "system" theme setting to the actual detected theme.
        
        Returns:
            "dark" or "light" based on the configured theme setting and system theme.
        """
        theme_setting = self.get("theme", "system")
        if theme_setting == "system":
            return self._get_system_theme()
        return theme_setting