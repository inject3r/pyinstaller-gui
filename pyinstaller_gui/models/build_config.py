"""Build configuration data model."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from .file_item import FileItem


@dataclass
class BuildConfig:
    """
    Configuration for PyInstaller build.
    
    This dataclass holds all the settings that can be configured through
    the GUI and are used to generate the PyInstaller command line.
    
    Attributes:
        script_path: Path to the main Python script to package.
        app_name: Name of the output executable (without extension).
        onefile: If True, create a single executable file instead of a folder.
        noconsole: If True, hide the console window (Windows only).
        hidden_imports: List of module names that are imported dynamically.
        icon_path: Path to custom icon file (.ico for Windows, .icns for macOS).
        output_folder: Directory where the built executable will be saved.
        additional_files: List of FileItem objects to bundle with the executable.
        log_level: Verbosity level for build output (TRACE, DEBUG, INFO, WARN, ERROR, FATAL).
        upx_dir: Directory containing UPX executable for compression.
        debug_mode: Debug options for troubleshooting (none, all, imports, bootloader, noarchive).
        clean_cache: If True, clear PyInstaller cache before building.
        tmpdir: Custom temporary directory for onefile mode extraction.
        custom_commands: Additional user-provided PyInstaller arguments.
    """
    
    script_path: Optional[Path] = None
    app_name: str = ""
    onefile: bool = False
    noconsole: bool = False
    hidden_imports: List[str] = field(default_factory=list)
    icon_path: Optional[Path] = None
    output_folder: Optional[Path] = None
    additional_files: List[FileItem] = field(default_factory=list)
    log_level: str = "INFO"
    upx_dir: Optional[Path] = None
    debug_mode: str = "none"
    clean_cache: bool = False
    tmpdir: str = ""
    custom_commands: str = ""