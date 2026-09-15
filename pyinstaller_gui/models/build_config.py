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
    the GUI and are used to generate the PyInstaller command line. It
    mirrors the options exposed by modern PyInstaller releases (6.x),
    grouped roughly the same way as PyInstaller's own ``--help`` output.
    
    Attributes:
        script_path: Path to the main Python script to package.
        app_name: Name of the output executable (without extension).
        onefile: If True, create a single executable file instead of a folder.
        noconsole: If True, hide the console window (windowed/no-console mode).
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
        search_paths: Extra import search paths (``-p/--paths``).
        exclude_modules: Modules to exclude from the build (``--exclude-module``).
        collect_all: Packages to fully collect (submodules, data, binaries).
        collect_submodules: Packages to collect all submodules from.
        collect_data: Packages to collect all data files from.
        collect_binaries: Packages to collect all binaries from.
        copy_metadata: Packages whose metadata should be copied.
        recursive_copy_metadata: Packages whose metadata (and dependencies') should be copied.
        additional_hooks_dir: Extra directory to search for PyInstaller hooks.
        runtime_hooks: Custom runtime hook scripts.
        splash_image: Path to an image used for a startup splash screen.
        noconfirm: If True, replace the output directory without asking (``-y``).
        strip: If True, strip debug symbols from the executable and shared libs.
        noupx: If True, disable UPX compression even if UPX is available.
        upx_exclude: Binaries to exclude from UPX compression.
        optimize_level: Bytecode optimization level ("", "0", "1", "2").
        python_options: Extra runtime options passed to the embedded interpreter.
        contents_directory: Name of the support-files directory for onedir builds.
        specpath: Folder in which the generated .spec file is stored.
        workpath: Folder for temporary work files.
        onedir_layout_flat: If True, use ``--contents-directory .`` (legacy flat onedir layout).
        console_explicit: If True, force console mode with ``--console`` even though it's default.
        hide_console: Windows-only bootloader console visibility behavior.
        disable_windowed_traceback: Disable the windowed-mode traceback dialog.
        version_file: Path to a Windows version-info resource file.
        manifest_file: Path to a custom Windows manifest file or inline XML.
        uac_admin: Request administrator elevation on start (Windows).
        uac_uiaccess: Allow the elevated app to work with Remote Desktop (Windows).
        argv_emulation: Enable argv emulation for macOS ``.app`` bundles.
        osx_bundle_identifier: macOS bundle identifier (reverse-DNS notation).
        target_arch: macOS target architecture (x86_64, arm64, universal2).
        codesign_identity: macOS code-signing identity.
        osx_entitlements_file: macOS entitlements file used when code-signing.
        bootloader_ignore_signals: Tell the bootloader to ignore forwarded signals.
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

    # --- What to bundle, where to search ---
    search_paths: List[str] = field(default_factory=list)
    exclude_modules: List[str] = field(default_factory=list)
    collect_all: List[str] = field(default_factory=list)
    collect_submodules: List[str] = field(default_factory=list)
    collect_data: List[str] = field(default_factory=list)
    collect_binaries: List[str] = field(default_factory=list)
    copy_metadata: List[str] = field(default_factory=list)
    recursive_copy_metadata: List[str] = field(default_factory=list)
    additional_hooks_dir: str = ""
    runtime_hooks: List[str] = field(default_factory=list)
    splash_image: str = ""

    # --- How to generate ---
    noconfirm: bool = False
    strip: bool = False
    noupx: bool = False
    upx_exclude: List[str] = field(default_factory=list)
    optimize_level: str = ""
    python_options: List[str] = field(default_factory=list)
    contents_directory: str = ""
    specpath: str = ""
    workpath: str = ""

    # --- Windows & macOS specific ---
    console_explicit: bool = False
    hide_console: str = "none"
    disable_windowed_traceback: bool = False
    version_file: str = ""
    manifest_file: str = ""
    uac_admin: bool = False
    uac_uiaccess: bool = False
    argv_emulation: bool = False
    osx_bundle_identifier: str = ""
    target_arch: str = ""
    codesign_identity: str = ""
    osx_entitlements_file: str = ""

    # --- Rarely used special options ---
    bootloader_ignore_signals: bool = False
