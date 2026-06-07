"""Tests for config manager module."""

import unittest
import tempfile
import json
import os
from pathlib import Path
from unittest.mock import patch

from pyinstaller_gui.core.config_manager import ConfigManager


class TestConfigManager(unittest.TestCase):
    """Test cases for ConfigManager class."""
    
    def setUp(self):
        """
        Set up test fixtures with temporary directory.
        
        Creates an isolated temporary directory for configuration files and
        mocks Path.home to point to this directory, preventing interference
        with the user's real configuration.
        """
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_home = Path.home
        
        def mock_home():
            """Mock function to return temporary directory as home path."""
            return Path(self.temp_dir.name)
        
        Path.home = mock_home
        self.config_manager = ConfigManager()
    
    def tearDown(self):
        """
        Clean up test fixtures.
        
        Restores the original Path.home function and removes the temporary
        directory after each test.
        """
        Path.home = self.original_home
        self.temp_dir.cleanup()
    
    def test_config_file_created(self):
        """
        Test that config file is created automatically.
        
        Verifies that when a ConfigManager instance is created, it automatically
        creates the configuration directory and JSON file with default values.
        """
        config_file = Path(self.temp_dir.name) / ".pyinstaller_gui" / "config.json"
        self.assertTrue(config_file.exists())
    
    def test_default_config_values(self):
        """
        Test default configuration values.
        
        Ensures that the configuration manager initializes with the expected
        default settings: system theme, empty recent files list, and default
        output folder path.
        """
        self.assertEqual(self.config_manager.get("theme"), "system")
        self.assertEqual(self.config_manager.get("recent_files"), [])
        self.assertIsNotNone(self.config_manager.get("output_folder"))
    
    def test_set_and_get(self):
        """
        Test setting and getting configuration values.
        
        Verifies that key-value pairs can be stored in the configuration and
        retrieved correctly.
        """
        self.config_manager.set("test_key", "test_value")
        self.assertEqual(self.config_manager.get("test_key"), "test_value")
    
    def test_get_default_value(self):
        """
        Test getting default value for missing key.
        
        Checks that when a non-existent key is requested, the specified default
        value is returned instead of raising an error.
        """
        value = self.config_manager.get("nonexistent_key", "default")
        self.assertEqual(value, "default")
    
    def test_config_persistence(self):
        """
        Test that configuration persists between instances.
        
        Verifies that configuration values saved in one ConfigManager instance
        are persisted to disk and can be loaded by a new instance.
        """
        self.config_manager.set("persistent_key", "persistent_value")
        
        new_manager = ConfigManager()
        self.assertEqual(new_manager.get("persistent_key"), "persistent_value")
    
    def test_effective_theme_system(self):
        """
        Test effective theme with system setting.
        
        When theme is set to "system", the effective theme should be either
        "dark" or "light" based on the actual system theme detection.
        """
        self.config_manager.set("theme", "system")
        theme = self.config_manager.get_effective_theme()
        self.assertIn(theme, ["dark", "light"])
    
    def test_effective_theme_dark(self):
        """
        Test effective theme with dark setting.
        
        When theme is explicitly set to "dark", the effective theme should
        always be "dark" regardless of system settings.
        """
        self.config_manager.set("theme", "dark")
        self.assertEqual(self.config_manager.get_effective_theme(), "dark")
    
    def test_effective_theme_light(self):
        """
        Test effective theme with light setting.
        
        When theme is explicitly set to "light", the effective theme should
        always be "light" regardless of system settings.
        """
        self.config_manager.set("theme", "light")
        self.assertEqual(self.config_manager.get_effective_theme(), "light")
    
    def test_recent_files_save_load(self):
        """
        Test saving and loading recent files.
        
        Verifies that the list of recently opened files is correctly persisted
        to disk and restored when a new ConfigManager instance is created.
        """
        recent_files = ["/path/to/file1.py", "/path/to/file2.py"]
        self.config_manager.set("recent_files", recent_files)
        
        new_manager = ConfigManager()
        self.assertEqual(new_manager.get("recent_files"), recent_files)
    
    def test_output_folder_save_load(self):
        """
        Test saving and loading output folder.
        
        Ensures that the user's preferred output directory setting is properly
        saved to disk and restored on application restart.
        """
        output_folder = "/custom/output/path"
        self.config_manager.set("output_folder", output_folder)
        
        new_manager = ConfigManager()
        self.assertEqual(new_manager.get("output_folder"), output_folder)

    def test_save_config_failure(self):
        """
        Test save_config handles IOError gracefully.
        
        Verifies that save_config returns False when there's an IOError.
        """
        with patch('builtins.open', side_effect=IOError("Permission denied")):
            result = self.config_manager.set("test_key", "test_value")
            self.assertFalse(result)

    def test_load_config_corrupted_json(self):
        """
        Test loading corrupted JSON file.
        
        Ensures that when config.json is corrupted, default config is loaded.
        """
        config_file = Path(self.temp_dir.name) / ".pyinstaller_gui" / "config.json"
        config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(config_file, 'w') as f:
            f.write("invalid json {")
        
        new_manager = ConfigManager()
        self.assertEqual(new_manager.get("theme"), "system")

    def test_ensure_config_dir_creates_directory(self):
        """
        Test ensure_config_dir creates directory if it doesn't exist.
        
        Verifies that the config directory is created automatically.
        """
        import shutil
        shutil.rmtree(self.config_manager.config_dir)
        self.config_manager._ensure_config_dir()
        self.assertTrue(self.config_manager.config_dir.exists())

if __name__ == "__main__":
    unittest.main()