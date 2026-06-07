"""Tests for build config model."""

import unittest
from pathlib import Path

from pyinstaller_gui.models.build_config import BuildConfig
from pyinstaller_gui.models.file_item import FileItem, FileType


class TestBuildConfig(unittest.TestCase):
    """Test cases for BuildConfig class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = BuildConfig()
    
    def test_default_values(self):
        """
        Test default values of BuildConfig.
        
        Verifies that all configuration attributes have their expected default
        values when a new BuildConfig instance is created.
        """
        self.assertIsNone(self.config.script_path)
        self.assertEqual(self.config.app_name, "")
        self.assertFalse(self.config.onefile)
        self.assertFalse(self.config.noconsole)
        self.assertEqual(self.config.hidden_imports, [])
        self.assertIsNone(self.config.icon_path)
        self.assertIsNone(self.config.output_folder)
        self.assertEqual(self.config.additional_files, [])
        self.assertEqual(self.config.log_level, "INFO")
        self.assertIsNone(self.config.upx_dir)
        self.assertEqual(self.config.debug_mode, "none")
        self.assertFalse(self.config.clean_cache)
        self.assertEqual(self.config.tmpdir, "")
        self.assertEqual(self.config.custom_commands, "")
    
    def test_set_script_path(self):
        """
        Test setting script path.
        
        Ensures that the script_path attribute can be set to a Path object
        and retrieved correctly.
        """
        test_path = Path("/path/to/script.py")
        self.config.script_path = test_path
        self.assertEqual(self.config.script_path, test_path)
    
    def test_set_app_name(self):
        """
        Test setting app name.
        
        Verifies that the application name attribute can be set and retrieved
        as a string value.
        """
        self.config.app_name = "MyApp"
        self.assertEqual(self.config.app_name, "MyApp")
    
    def test_set_onefile(self):
        """
        Test setting onefile option.
        
        Checks that the onefile boolean flag can be enabled and properly
        reflects the True state.
        """
        self.config.onefile = True
        self.assertTrue(self.config.onefile)
    
    def test_set_noconsole(self):
        """
        Test setting noconsole option.
        
        Verifies that the noconsole boolean flag can be enabled and properly
        reflects the True state.
        """
        self.config.noconsole = True
        self.assertTrue(self.config.noconsole)
    
    def test_set_hidden_imports(self):
        """
        Test setting hidden imports.
        
        Ensures that a list of hidden import module names can be stored and
        retrieved correctly as a list.
        """
        imports = ["requests", "json", "datetime"]
        self.config.hidden_imports = imports
        self.assertEqual(self.config.hidden_imports, imports)
    
    def test_set_icon_path(self):
        """
        Test setting icon path.
        
        Verifies that the icon path can be set to a Path object pointing to
        an icon file (.ico for Windows, .icns for macOS).
        """
        icon_path = Path("/path/to/icon.ico")
        self.config.icon_path = icon_path
        self.assertEqual(self.config.icon_path, icon_path)
    
    def test_set_output_folder(self):
        """
        Test setting output folder.
        
        Checks that the output directory path can be configured and retrieved
        as a Path object.
        """
        output_folder = Path("/output/folder")
        self.config.output_folder = output_folder
        self.assertEqual(self.config.output_folder, output_folder)
    
    def test_set_additional_files(self):
        """
        Test setting additional files.
        
        Verifies that a list of FileItem objects can be stored and retrieved,
        representing files, folders, or binaries to be bundled.
        """
        files = [
            FileItem("/path/to/file.txt", FileType.FILE),
            FileItem("/path/to/folder", FileType.FOLDER)
        ]
        self.config.additional_files = files
        self.assertEqual(self.config.additional_files, files)
    
    def test_set_log_level(self):
        """
        Test setting log level.
        
        Ensures that the log level can be set to a string value that matches
        PyInstaller's valid log levels (TRACE, DEBUG, INFO, WARN, ERROR, FATAL).
        """
        self.config.log_level = "DEBUG"
        self.assertEqual(self.config.log_level, "DEBUG")
    
    def test_set_upx_dir(self):
        """
        Test setting UPX directory.
        
        Verifies that the UPX utility directory path can be configured for
        executable compression.
        """
        upx_dir = Path("/usr/bin/upx")
        self.config.upx_dir = upx_dir
        self.assertEqual(self.config.upx_dir, upx_dir)
    
    def test_set_debug_mode(self):
        """
        Test setting debug mode.
        
        Checks that debug mode can be set to valid PyInstaller debug options:
        none, all, imports, bootloader, or noarchive.
        """
        self.config.debug_mode = "all"
        self.assertEqual(self.config.debug_mode, "all")
    
    def test_set_clean_cache(self):
        """
        Test setting clean cache.
        
        Verifies that the clean cache flag can be enabled, which tells
        PyInstaller to clear its cache before building.
        """
        self.config.clean_cache = True
        self.assertTrue(self.config.clean_cache)
    
    def test_set_tmpdir(self):
        """
        Test setting tmpdir.
        
        Ensures that a custom runtime temporary directory path can be
        configured for onefile mode extraction.
        """
        self.config.tmpdir = "/tmp/mydir"
        self.assertEqual(self.config.tmpdir, "/tmp/mydir")
    
    def test_set_custom_commands(self):
        """
        Test setting custom commands.
        
        Verifies that additional PyInstaller command-line arguments can be
        appended to the build command.
        """
        self.config.custom_commands = "--optimize 2"
        self.assertEqual(self.config.custom_commands, "--optimize 2")


if __name__ == "__main__":
    unittest.main()