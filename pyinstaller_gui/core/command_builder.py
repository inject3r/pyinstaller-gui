"""PyInstaller command builder module."""

from pathlib import Path
from typing import Optional

from ..models.build_config import BuildConfig
from ..models.file_item import FileType


class CommandBuilder:
    """
    Builds PyInstaller command line arguments.
    
    This class takes a BuildConfig object and generates the complete
    PyInstaller command line string with all the appropriate flags and
    arguments based on the user's configuration.
    """
    
    def __init__(self):
        """Initialize the command builder with no configuration."""
        self.config: Optional[BuildConfig] = None
    
    def set_config(self, config: BuildConfig) -> None:
        """
        Set the build configuration.
        
        Args:
            config: The BuildConfig object containing all build settings.
        """
        self.config = config
    
    def build(self) -> str:
        """
        Build the complete PyInstaller command.
        
        Processes the configuration and constructs a PyInstaller command
        line with all enabled options, flags, and arguments.
        
        Returns:
            The complete PyInstaller command string, or an error message
            if no valid script path is configured.
        """
        if not self.config or not self.config.script_path:
            return "Error: No script selected!"
        
        script = str(self.config.script_path)
        command = f'pyinstaller "{script}"'
        
        # Basic options
        if self.config.app_name:
            command += f' --name "{self.config.app_name}"'
        
        if self.config.onefile:
            command += " --onefile"
        
        if self.config.noconsole:
            command += " --windowed"
        
        # Hidden imports
        for imp in self.config.hidden_imports:
            command += f' --hidden-import {imp}'
        
        # Icon
        if self.config.icon_path:
            command += f' --icon="{self.config.icon_path}"'
        
        # Output folder
        if self.config.output_folder:
            command += f' --distpath="{self.config.output_folder}"'
        
        # Additional files
        for item in self.config.additional_files:
            if item.file_type == FileType.FILE:
                command += f' --add-data "{item.path}:."'
            elif item.file_type == FileType.FOLDER:
                command += f' --add-data "{item.path}:."'
            elif item.file_type == FileType.BINARY:
                command += f' --add-binary "{item.path}:."'
        
        # Log level - MUST be uppercase and valid values: TRACE, DEBUG, INFO, WARN, DEPRECATION, ERROR, FATAL
        if self.config.log_level:
            log_level = self.config.log_level.upper()
            # Map common values to valid PyInstaller values
            if log_level == "WARNING":
                log_level = "WARN"
            elif log_level == "CRITICAL":
                log_level = "FATAL"
            command += f" --log-level {log_level}"
        
        # UPX directory
        if self.config.upx_dir:
            command += f' --upx-dir="{self.config.upx_dir}"'
        
        # Debug mode - valid values: all, imports, bootloader, noarchive
        if self.config.debug_mode and self.config.debug_mode != "none":
            debug_value = self.config.debug_mode.lower()
            if debug_value == "all":
                command += " --debug all"
            elif debug_value == "imports":
                command += " --debug imports"
            elif debug_value == "bootloader":
                command += " --debug bootloader"
            elif debug_value == "noarchive":
                command += " --debug noarchive"
        
        # Clean cache
        if self.config.clean_cache:
            command += " --clean"
        
        # Runtime tmpdir
        if self.config.tmpdir:
            command += f' --runtime-tmpdir="{self.config.tmpdir}"'
        
        # Custom commands
        if self.config.custom_commands:
            command += f" {self.config.custom_commands}"
        
        return command