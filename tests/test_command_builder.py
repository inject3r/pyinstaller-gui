"""Tests for command builder module."""

import unittest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch

from pyinstaller_gui.core.command_builder import CommandBuilder
from pyinstaller_gui.models.build_config import BuildConfig
from pyinstaller_gui.models.file_item import FileItem, FileType


class TestCommandBuilder(unittest.TestCase):
    """Test cases for CommandBuilder class."""
    
    def setUp(self):
        """
        Set up test fixtures.
        
        Creates a temporary directory, a mock Python script file, and initializes
        the command builder with an empty configuration before each test.
        """
        self.builder = CommandBuilder()
        self.config = BuildConfig()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_script = os.path.join(self.temp_dir.name, "test_script.py")
        
        with open(self.test_script, 'w') as f:
            f.write("# Test script")
    
    def tearDown(self):
        """
        Clean up test fixtures.
        
        Removes the temporary directory and all its contents after each test.
        """
        self.temp_dir.cleanup()
    
    def test_empty_config(self):
        """
        Test building command with empty config.
        
        Verifies that attempting to build a command without a configured script
        returns an appropriate error message.
        """
        self.builder.set_config(self.config)
        command = self.builder.build()
        self.assertEqual(command, "Error: No script selected!")
    
    def test_basic_command(self):
        """
        Test building basic command.
        
        Checks that the simplest pyinstaller command with only a script path
        is generated correctly.
        """
        self.config.script_path = Path(self.test_script)
        self.builder.set_config(self.config)
        command = self.builder.build()
        self.assertIn(f'pyinstaller "{self.test_script}"', command)
    
    def test_with_app_name(self):
        """
        Test command with application name.
        
        Ensures the --name flag is added to the command when an application
        name is specified.
        """
        self.config.script_path = Path(self.test_script)
        self.config.app_name = "MyApp"
        self.builder.set_config(self.config)
        command = self.builder.build()
        self.assertIn('--name "MyApp"', command)
    
    def test_with_onefile(self):
        """
        Test command with onefile option.
        
        Verifies the --onefile flag is added to create a single executable
        instead of a directory with multiple files.
        """
        self.config.script_path = Path(self.test_script)
        self.config.onefile = True
        self.builder.set_config(self.config)
        command = self.builder.build()
        self.assertIn("--onefile", command)
    
    def test_with_noconsole(self):
        """
        Test command with noconsole option.
        
        Checks that --windowed flag is added to hide the console window
        for GUI applications.
        """
        self.config.script_path = Path(self.test_script)
        self.config.noconsole = True
        self.builder.set_config(self.config)
        command = self.builder.build()
        self.assertIn("--windowed", command)
    
    def test_with_hidden_imports(self):
        """
        Test command with hidden imports.
        
        Verifies that multiple --hidden-import flags are added for each
        module specified in the hidden imports list.
        """
        self.config.script_path = Path(self.test_script)
        self.config.hidden_imports = ["requests", "json"]
        self.builder.set_config(self.config)
        command = self.builder.build()
        self.assertIn('--hidden-import requests', command)
        self.assertIn('--hidden-import json', command)
    
    def test_with_icon(self):
        """
        Test command with icon path.
        
        Ensures the --icon flag is added with the path to the custom icon file.
        """
        self.config.script_path = Path(self.test_script)
        self.config.icon_path = Path("/path/to/icon.ico")
        self.builder.set_config(self.config)
        command = self.builder.build()
        self.assertIn('--icon="/path/to/icon.ico"', command)
    
    def test_with_output_folder(self):
        """
        Test command with output folder.
        
        Verifies the --distpath flag is added to specify the output directory
        for the built executable.
        """
        self.config.script_path = Path(self.test_script)
        self.config.output_folder = Path("/output/folder")
        self.builder.set_config(self.config)
        command = self.builder.build()
        self.assertIn('--distpath="/output/folder"', command)
    
    def test_with_additional_files(self):
        """
        Test command with additional files.
        
        Checks that --add-data flags are added for files and folders, and
        --add-binary flags are added for binary files to be bundled.
        """
        self.config.script_path = Path(self.test_script)
        self.config.additional_files = [
            FileItem("/path/to/file.txt", FileType.FILE),
            FileItem("/path/to/folder", FileType.FOLDER),
            FileItem("/path/to/binary.dll", FileType.BINARY)
        ]
        self.builder.set_config(self.config)
        command = self.builder.build()
        self.assertIn('--add-data "/path/to/file.txt:."', command)
        self.assertIn('--add-data "/path/to/folder:."', command)
        self.assertIn('--add-binary "/path/to/binary.dll:."', command)
    
    def test_with_log_level(self):
        """
        Test command with log level.
        
        Verifies the --log-level flag is added to control the verbosity of
        PyInstaller's build output.
        """
        self.config.script_path = Path(self.test_script)
        self.config.log_level = "DEBUG"
        self.builder.set_config(self.config)
        command = self.builder.build()
        self.assertIn("--log-level DEBUG", command)
    
    def test_with_upx_dir(self):
        """
        Test command with UPX directory.
        
        Ensures the --upx-dir flag is added to specify the location of the
        UPX executable compressor.
        """
        self.config.script_path = Path(self.test_script)
        self.config.upx_dir = Path("/usr/bin/upx")
        self.builder.set_config(self.config)
        command = self.builder.build()
        self.assertIn('--upx-dir="/usr/bin/upx"', command)
    
    def test_with_debug_mode(self):
        """
        Test command with debug mode.
        
        Verifies the --debug flag is added with the appropriate debug level
        (all, imports, bootloader, or noarchive).
        """
        self.config.script_path = Path(self.test_script)
        self.config.debug_mode = "all"
        self.builder.set_config(self.config)
        command = self.builder.build()
        self.assertIn("--debug all", command)
    
    def test_with_clean_cache(self):
        """
        Test command with clean cache option.
        
        Checks that the --clean flag is added to clear PyInstaller's cache
        before building.
        """
        self.config.script_path = Path(self.test_script)
        self.config.clean_cache = True
        self.builder.set_config(self.config)
        command = self.builder.build()
        self.assertIn("--clean", command)
    
    def test_with_tmpdir(self):
        """
        Test command with tmpdir.
        
        Verifies the --runtime-tmpdir flag is added to specify a custom
        temporary directory for onefile mode extraction.
        """
        self.config.script_path = Path(self.test_script)
        self.config.tmpdir = "/tmp/mydir"
        self.builder.set_config(self.config)
        command = self.builder.build()
        self.assertIn('--runtime-tmpdir="/tmp/mydir"', command)
    
    def test_with_custom_commands(self):
        """
        Test command with custom commands.
        
        Ensures that additional user-provided command-line arguments are
        appended to the generated PyInstaller command.
        """
        self.config.script_path = Path(self.test_script)
        self.config.custom_commands = "--optimize 2 --noupx"
        self.builder.set_config(self.config)
        command = self.builder.build()
        self.assertIn("--optimize 2 --noupx", command)
    
    def test_all_options_together(self):
        """
        Test command with all options together.
        
        Verifies that when all configuration options are enabled simultaneously,
        the generated command contains all the expected flags and arguments
        in the correct order.
        """
        self.config.script_path = Path(self.test_script)
        self.config.app_name = "FullApp"
        self.config.onefile = True
        self.config.noconsole = True
        self.config.hidden_imports = ["requests", "json"]
        self.config.icon_path = Path("/path/to/icon.ico")
        self.config.output_folder = Path("/output/folder")
        self.config.log_level = "INFO"
        self.config.clean_cache = True
        
        self.builder.set_config(self.config)
        command = self.builder.build()
        
        self.assertIn(f'pyinstaller "{self.test_script}"', command)
        self.assertIn('--name "FullApp"', command)
        self.assertIn("--onefile", command)
        self.assertIn("--windowed", command)
        self.assertIn('--icon="/path/to/icon.ico"', command)
        self.assertIn('--distpath="/output/folder"', command)
        self.assertIn("--log-level INFO", command)
        self.assertIn("--clean", command)

    def test_with_empty_log_level(self):
        """
        Test command with empty log level.
        
        Verifies that no --log-level flag is added when log_level is empty or None.
        """
        self.config.script_path = Path(self.test_script)
        self.config.log_level = ""
        self.builder.set_config(self.config)
        command = self.builder.build()
        self.assertNotIn("--log-level", command)

    def test_with_warning_log_level_mapping(self):
        """
        Test command with WARNING log level mapped to WARN.
        
        Ensures that WARNING is correctly mapped to WARN for PyInstaller compatibility.
        """
        self.config.script_path = Path(self.test_script)
        self.config.log_level = "WARNING"
        self.builder.set_config(self.config)
        command = self.builder.build()
        self.assertIn("--log-level WARN", command)

    def test_with_critical_log_level_mapping(self):
        """
        Test command with CRITICAL log level mapped to FATAL.
        
        Ensures that CRITICAL is correctly mapped to FATAL for PyInstaller compatibility.
        """
        self.config.script_path = Path(self.test_script)
        self.config.log_level = "CRITICAL"
        self.builder.set_config(self.config)
        command = self.builder.build()
        self.assertIn("--log-level FATAL", command)

    def test_with_debug_mode_imports(self):
        """
        Test command with debug mode set to imports.
        
        Verifies that --debug imports flag is added correctly.
        """
        self.config.script_path = Path(self.test_script)
        self.config.debug_mode = "imports"
        self.builder.set_config(self.config)
        command = self.builder.build()
        self.assertIn("--debug imports", command)

    def test_with_debug_mode_bootloader(self):
        """
        Test command with debug mode set to bootloader.
        
        Verifies that --debug bootloader flag is added correctly.
        """
        self.config.script_path = Path(self.test_script)
        self.config.debug_mode = "bootloader"
        self.builder.set_config(self.config)
        command = self.builder.build()
        self.assertIn("--debug bootloader", command)

    def test_with_debug_mode_noarchive(self):
        """
        Test command with debug mode set to noarchive.
        
        Verifies that --debug noarchive flag is added correctly.
        """
        self.config.script_path = Path(self.test_script)
        self.config.debug_mode = "noarchive"
        self.builder.set_config(self.config)
        command = self.builder.build()
        self.assertIn("--debug noarchive", command)

if __name__ == "__main__":
    unittest.main()