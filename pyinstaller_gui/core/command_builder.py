"""PyInstaller command builder module."""

import platform
from typing import List, Optional

from ..models.build_config import BuildConfig
from ..models.file_item import FileType


def _data_separator() -> str:
    """
    Return the separator PyInstaller expects between source and destination
    in ``--add-data``/``--add-binary`` values for the current platform.
    
    PyInstaller documents this as "SOURCE:DEST" on POSIX systems, but on
    Windows the colon collides with drive letters (e.g. ``C:\\...``), so the
    bootloader/CLI expects a semicolon there instead. Building the command on
    one OS and running it on another is not supported by PyInstaller anyway
    (it never cross-compiles), so it is always correct to use the separator
    for the platform this code is currently running on.
    
    Returns:
        ";" on Windows, ":" everywhere else.
    """
    return ";" if platform.system() == "Windows" else ":"


class CommandBuilder:
    """
    Builds PyInstaller command line arguments.
    
    This class takes a BuildConfig object and generates either a
    human-readable PyInstaller command line string (for preview/copying) or
    a properly separated argument list (for safe, cross-platform execution
    without going through a shell).
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
    
    def validate(self) -> Optional[str]:
        """
        Validate the current configuration.
        
        Returns:
            An error message string if the configuration is invalid,
            otherwise None.
        """
        if not self.config or not self.config.script_path:
            return "No script selected!"
        return None
    
    # ------------------------------------------------------------------
    # Human readable command preview
    # ------------------------------------------------------------------
    def build(self) -> str:
        """
        Build a human-readable PyInstaller command line for preview/copying.
        
        Processes the configuration and constructs a PyInstaller command
        line with all enabled options, flags, and arguments.
        
        Returns:
            The complete PyInstaller command string, or an error message
            if no valid script path is configured.
        """
        error = self.validate()
        if error:
            return f"Error: {error}"
        
        cfg = self.config
        sep = _data_separator()
        script = str(cfg.script_path)
        command = f'pyinstaller "{script}"'
        
        # Basic options
        if cfg.app_name:
            command += f' --name "{cfg.app_name}"'
        
        if cfg.onefile:
            command += " --onefile"
        
        if cfg.noconsole:
            command += " --windowed"
        elif cfg.console_explicit:
            command += " --console"
        
        # Hidden imports
        for imp in cfg.hidden_imports:
            command += f' --hidden-import {imp}'
        
        # Search paths
        for p in cfg.search_paths:
            command += f' --paths "{p}"'
        
        # Excluded modules
        for mod in cfg.exclude_modules:
            command += f' --exclude-module {mod}'
        
        # Collect helpers
        for pkg in cfg.collect_all:
            command += f' --collect-all {pkg}'
        for pkg in cfg.collect_submodules:
            command += f' --collect-submodules {pkg}'
        for pkg in cfg.collect_data:
            command += f' --collect-data {pkg}'
        for pkg in cfg.collect_binaries:
            command += f' --collect-binaries {pkg}'
        for pkg in cfg.copy_metadata:
            command += f' --copy-metadata {pkg}'
        for pkg in cfg.recursive_copy_metadata:
            command += f' --recursive-copy-metadata {pkg}'
        
        if cfg.additional_hooks_dir:
            command += f' --additional-hooks-dir "{cfg.additional_hooks_dir}"'
        
        for hook in cfg.runtime_hooks:
            command += f' --runtime-hook "{hook}"'
        
        if cfg.splash_image:
            command += f' --splash "{cfg.splash_image}"'
        
        # Icon
        if cfg.icon_path:
            command += f' --icon="{cfg.icon_path}"'
        
        # Output folder
        if cfg.output_folder:
            command += f' --distpath="{cfg.output_folder}"'
        
        # Additional files (platform-correct SOURCE<sep>DEST format)
        for item in cfg.additional_files:
            dest = item.dest or "."
            if item.file_type in (FileType.FILE, FileType.FOLDER):
                command += f' --add-data "{item.path}{sep}{dest}"'
            elif item.file_type == FileType.BINARY:
                command += f' --add-binary "{item.path}{sep}{dest}"'
        
        # Log level - MUST be uppercase and valid values: TRACE, DEBUG, INFO, WARN, DEPRECATION, ERROR, FATAL
        if cfg.log_level:
            log_level = self._normalize_log_level(cfg.log_level)
            command += f" --log-level {log_level}"
        
        # UPX
        if cfg.noupx:
            command += " --noupx"
        elif cfg.upx_dir:
            command += f' --upx-dir="{cfg.upx_dir}"'
        for f in cfg.upx_exclude:
            command += f' --upx-exclude "{f}"'
        
        # Debug mode - valid values: all, imports, bootloader, noarchive
        if cfg.debug_mode and cfg.debug_mode != "none":
            debug_value = cfg.debug_mode.lower()
            if debug_value in ("all", "imports", "bootloader", "noarchive"):
                command += f" --debug {debug_value}"
        
        # Optimization / stripping
        if cfg.optimize_level:
            command += f" --optimize {cfg.optimize_level}"
        if cfg.strip:
            command += " --strip"
        for opt in cfg.python_options:
            command += f' --python-option "{opt}"'
        
        # Clean cache / confirm
        if cfg.clean_cache:
            command += " --clean"
        if cfg.noconfirm:
            command += " --noconfirm"
        
        # Layout / working dirs
        if cfg.contents_directory:
            command += f' --contents-directory "{cfg.contents_directory}"'
        if cfg.specpath:
            command += f' --specpath "{cfg.specpath}"'
        if cfg.workpath:
            command += f' --workpath "{cfg.workpath}"'
        
        # Runtime tmpdir
        if cfg.tmpdir:
            command += f' --runtime-tmpdir="{cfg.tmpdir}"'
        
        # Windows-only options
        if cfg.hide_console and cfg.hide_console != "none":
            command += f" --hide-console {cfg.hide_console}"
        if cfg.disable_windowed_traceback:
            command += " --disable-windowed-traceback"
        if cfg.version_file:
            command += f' --version-file "{cfg.version_file}"'
        if cfg.manifest_file:
            command += f' --manifest "{cfg.manifest_file}"'
        if cfg.uac_admin:
            command += " --uac-admin"
        if cfg.uac_uiaccess:
            command += " --uac-uiaccess"
        
        # macOS-only options
        if cfg.argv_emulation:
            command += " --argv-emulation"
        if cfg.osx_bundle_identifier:
            command += f' --osx-bundle-identifier "{cfg.osx_bundle_identifier}"'
        if cfg.target_arch:
            command += f" --target-architecture {cfg.target_arch}"
        if cfg.codesign_identity:
            command += f' --codesign-identity "{cfg.codesign_identity}"'
        if cfg.osx_entitlements_file:
            command += f' --osx-entitlements-file "{cfg.osx_entitlements_file}"'
        
        # Rarely used special options
        if cfg.bootloader_ignore_signals:
            command += " --bootloader-ignore-signals"
        
        # Custom commands (always last so users can append/override anything)
        if cfg.custom_commands:
            command += f" {cfg.custom_commands}"
        
        return command
    
    # ------------------------------------------------------------------
    # Safe argument list for execution (no shell involved)
    # ------------------------------------------------------------------
    def build_args(self) -> List[str]:
        """
        Build the PyInstaller arguments as a list, suitable for passing
        directly to ``subprocess`` (e.g. after ``[sys.executable, "-m",
        "PyInstaller"]``) without invoking a shell.
        
        Returns:
            List of argument strings. Raises ValueError if the
            configuration is invalid (no script selected).
        """
        error = self.validate()
        if error:
            raise ValueError(error)
        
        cfg = self.config
        sep = _data_separator()
        args: List[str] = [str(cfg.script_path)]
        
        if cfg.app_name:
            args += ["--name", cfg.app_name]
        
        if cfg.onefile:
            args.append("--onefile")
        
        if cfg.noconsole:
            args.append("--windowed")
        elif cfg.console_explicit:
            args.append("--console")
        
        for imp in cfg.hidden_imports:
            args += ["--hidden-import", imp]
        
        for p in cfg.search_paths:
            args += ["--paths", p]
        
        for mod in cfg.exclude_modules:
            args += ["--exclude-module", mod]
        
        for pkg in cfg.collect_all:
            args += ["--collect-all", pkg]
        for pkg in cfg.collect_submodules:
            args += ["--collect-submodules", pkg]
        for pkg in cfg.collect_data:
            args += ["--collect-data", pkg]
        for pkg in cfg.collect_binaries:
            args += ["--collect-binaries", pkg]
        for pkg in cfg.copy_metadata:
            args += ["--copy-metadata", pkg]
        for pkg in cfg.recursive_copy_metadata:
            args += ["--recursive-copy-metadata", pkg]
        
        if cfg.additional_hooks_dir:
            args += ["--additional-hooks-dir", cfg.additional_hooks_dir]
        
        for hook in cfg.runtime_hooks:
            args += ["--runtime-hook", hook]
        
        if cfg.splash_image:
            args += ["--splash", cfg.splash_image]
        
        if cfg.icon_path:
            args += ["--icon", str(cfg.icon_path)]
        
        if cfg.output_folder:
            args += ["--distpath", str(cfg.output_folder)]
        
        for item in cfg.additional_files:
            dest = item.dest or "."
            value = f"{item.path}{sep}{dest}"
            if item.file_type in (FileType.FILE, FileType.FOLDER):
                args += ["--add-data", value]
            elif item.file_type == FileType.BINARY:
                args += ["--add-binary", value]
        
        if cfg.log_level:
            args += ["--log-level", self._normalize_log_level(cfg.log_level)]
        
        if cfg.noupx:
            args.append("--noupx")
        elif cfg.upx_dir:
            args += ["--upx-dir", str(cfg.upx_dir)]
        for f in cfg.upx_exclude:
            args += ["--upx-exclude", f]
        
        if cfg.debug_mode and cfg.debug_mode.lower() in ("all", "imports", "bootloader", "noarchive"):
            args += ["--debug", cfg.debug_mode.lower()]
        
        if cfg.optimize_level:
            args += ["--optimize", cfg.optimize_level]
        if cfg.strip:
            args.append("--strip")
        for opt in cfg.python_options:
            args += ["--python-option", opt]
        
        if cfg.clean_cache:
            args.append("--clean")
        if cfg.noconfirm:
            args.append("--noconfirm")
        
        if cfg.contents_directory:
            args += ["--contents-directory", cfg.contents_directory]
        if cfg.specpath:
            args += ["--specpath", cfg.specpath]
        if cfg.workpath:
            args += ["--workpath", cfg.workpath]
        
        if cfg.tmpdir:
            args += ["--runtime-tmpdir", cfg.tmpdir]
        
        if cfg.hide_console and cfg.hide_console != "none":
            args += ["--hide-console", cfg.hide_console]
        if cfg.disable_windowed_traceback:
            args.append("--disable-windowed-traceback")
        if cfg.version_file:
            args += ["--version-file", cfg.version_file]
        if cfg.manifest_file:
            args += ["--manifest", cfg.manifest_file]
        if cfg.uac_admin:
            args.append("--uac-admin")
        if cfg.uac_uiaccess:
            args.append("--uac-uiaccess")
        
        if cfg.argv_emulation:
            args.append("--argv-emulation")
        if cfg.osx_bundle_identifier:
            args += ["--osx-bundle-identifier", cfg.osx_bundle_identifier]
        if cfg.target_arch:
            args += ["--target-architecture", cfg.target_arch]
        if cfg.codesign_identity:
            args += ["--codesign-identity", cfg.codesign_identity]
        if cfg.osx_entitlements_file:
            args += ["--osx-entitlements-file", cfg.osx_entitlements_file]
        
        if cfg.bootloader_ignore_signals:
            args.append("--bootloader-ignore-signals")
        
        if cfg.custom_commands:
            # Best-effort split so custom commands still work as separate
            # argv entries instead of one bogus combined token.
            import shlex
            try:
                args += shlex.split(cfg.custom_commands, posix=(platform.system() != "Windows"))
            except ValueError:
                args.append(cfg.custom_commands)
        
        return args
    
    @staticmethod
    def _normalize_log_level(log_level: str) -> str:
        """
        Normalize a log level string to a value PyInstaller accepts.
        
        Args:
            log_level: Raw log level string (case-insensitive).
        
        Returns:
            Uppercase log level, with common aliases (WARNING -> WARN,
            CRITICAL -> FATAL) mapped to PyInstaller's expected values.
        """
        level = log_level.upper()
        if level == "WARNING":
            level = "WARN"
        elif level == "CRITICAL":
            level = "FATAL"
        return level
