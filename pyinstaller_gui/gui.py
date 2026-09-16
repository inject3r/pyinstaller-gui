import webbrowser
import os
from pathlib import Path

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QTabWidget, QHBoxLayout,
    QMessageBox
)
from PyQt6.QtGui import QIcon, QPainter, QColor, QPixmap
from PyQt6.QtCore import Qt

from .core.config_manager import ConfigManager
from .core.command_builder import CommandBuilder
from .core.version_checker import VersionChecker
from .models.build_config import BuildConfig
from .models.file_item import FileItem, FileType
from .workers.pyinstaller_worker import PyInstallerWorker
from .widgets.header_widget import HeaderWidget
from .widgets.output_widget import OutputWidget
from .widgets.version_widget import VersionWidget
from .tabs.general_tab import GeneralTab
from .tabs.files_tab import FilesTab
from .tabs.imports_tab import ImportsTab
from .tabs.advanced_tab import AdvancedTab
from .tabs.settings_tab import SettingsTab
from .tabs.config_tab import ConfigTab
from .styles.themes import get_stylesheet


class PyInstallerGUI(QWidget):
    """
    Main GUI window for PyInstaller wrapper.
    
    This is the main application window that integrates all tabs and widgets.
    It manages the build configuration, coordinates between different UI
    components, and handles the PyInstaller execution process.
    
    The window consists of:
    - Header: Title, version, theme toggle, and GitHub button
    - Tab widget: General, Additional Files, Imports & Hooks, Advanced,
      Settings, and Config tabs
    - Output widget: Command preview and build console output
    - Version widget: Python and PyInstaller version display
    - Run/Stop buttons: Start or cancel the build process
    """
    
    def __init__(self):
        """Initialize the main GUI window."""
        super().__init__()
        self.config_manager = ConfigManager()
        self.command_builder = CommandBuilder()
        self.version_checker = VersionChecker()
        self.build_config = BuildConfig()
        self.worker = None
        
        self.setWindowTitle("PyInstaller GUI")
        
        # Load window icon from app.png in the same directory
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.png")
        if os.path.exists(icon_path):
            pixmap = QPixmap(icon_path)
            if not pixmap.isNull():
                self.setWindowIcon(QIcon(pixmap))
        
        self.setGeometry(100, 100, 950, 750)
        
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(10)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        
        self.setup_ui()
        self.setup_connections()
        self.display_versions()
        self.apply_theme()
    
    def setup_ui(self):
        """Setup the user interface by creating and arranging all widgets."""
        self.header = HeaderWidget()
        
        self.tabs = QTabWidget()
        
        self.general_tab = GeneralTab()
        self.files_tab = FilesTab()
        self.imports_tab = ImportsTab()
        self.advanced_tab = AdvancedTab()
        self.settings_tab = SettingsTab()
        self.config_tab = ConfigTab()
        
        self.tabs.addTab(self.general_tab, "General")
        self.tabs.addTab(self.files_tab, "Additional Files")
        self.tabs.addTab(self.imports_tab, "Imports && Hooks")
        self.tabs.addTab(self.advanced_tab, "Advanced")
        self.tabs.addTab(self.settings_tab, "Settings")
        self.tabs.addTab(self.config_tab, "Config")
        
        self.output_widget = OutputWidget()
        self.version_widget = VersionWidget()
        
        run_row = QWidget()
        run_row_layout = QHBoxLayout(run_row)
        run_row_layout.setContentsMargins(0, 0, 0, 0)
        run_row_layout.setSpacing(10)
        
        self.run_button = QPushButton("Run PyInstaller")
        self.run_button.setFixedHeight(40)
        
        self.stop_button = QPushButton("Stop")
        self.stop_button.setFixedHeight(40)
        self.stop_button.setEnabled(False)
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: #DC3545;
            }
            QPushButton:hover {
                background-color: #C82333;
            }
            QPushButton:disabled {
                background-color: #808080;
            }
        """)
        
        run_row_layout.addWidget(self.run_button, 3)
        run_row_layout.addWidget(self.stop_button, 1)
        
        self.main_layout.addWidget(self.header)
        self.main_layout.addWidget(self.tabs)
        self.main_layout.addWidget(self.output_widget)
        self.main_layout.addWidget(self.version_widget)
        self.main_layout.addWidget(run_row)
        
        self.setLayout(self.main_layout)
    
    def setup_connections(self):
        """Setup all signal/slot connections between widgets."""
        # Header connections
        self.header.theme_toggled.connect(self.toggle_theme)
        self.header.github_clicked.connect(self.open_github)
        
        # General tab connections
        self.general_tab.script_changed.connect(self.on_script_changed)
        self.general_tab.app_name_changed.connect(self.on_app_name_changed)
        self.general_tab.onefile_changed.connect(self.on_onefile_changed)
        self.general_tab.noconsole_changed.connect(self.on_noconsole_changed)
        self.general_tab.hidden_imports_changed.connect(self.on_hidden_imports_changed)
        
        # Files tab connection
        self.files_tab.files_changed.connect(self.on_files_changed)
        
        # Imports & Hooks tab connections
        self.imports_tab.search_paths_changed.connect(self.on_search_paths_changed)
        self.imports_tab.exclude_modules_changed.connect(self.on_exclude_modules_changed)
        self.imports_tab.collect_all_changed.connect(self.on_collect_all_changed)
        self.imports_tab.collect_submodules_changed.connect(self.on_collect_submodules_changed)
        self.imports_tab.collect_data_changed.connect(self.on_collect_data_changed)
        self.imports_tab.collect_binaries_changed.connect(self.on_collect_binaries_changed)
        self.imports_tab.copy_metadata_changed.connect(self.on_copy_metadata_changed)
        self.imports_tab.recursive_copy_metadata_changed.connect(self.on_recursive_copy_metadata_changed)
        self.imports_tab.additional_hooks_dir_changed.connect(self.on_additional_hooks_dir_changed)
        self.imports_tab.runtime_hooks_changed.connect(self.on_runtime_hooks_changed)
        self.imports_tab.splash_image_changed.connect(self.on_splash_image_changed)
        
        # Settings tab connections
        self.settings_tab.output_folder_changed.connect(self.on_output_folder_changed)
        self.settings_tab.custom_commands_changed.connect(self.on_custom_commands_changed)
        self.settings_tab.icon_path_changed.connect(self.on_icon_path_changed)
        self.settings_tab.tmpdir_changed.connect(self.on_tmpdir_changed)
        self.settings_tab.specpath_changed.connect(self.on_specpath_changed)
        self.settings_tab.workpath_changed.connect(self.on_workpath_changed)
        self.settings_tab.console_explicit_changed.connect(self.on_console_explicit_changed)
        self.settings_tab.hide_console_changed.connect(self.on_hide_console_changed)
        self.settings_tab.disable_windowed_traceback_changed.connect(self.on_disable_windowed_traceback_changed)
        self.settings_tab.version_file_changed.connect(self.on_version_file_changed)
        self.settings_tab.manifest_file_changed.connect(self.on_manifest_file_changed)
        self.settings_tab.uac_admin_changed.connect(self.on_uac_admin_changed)
        self.settings_tab.uac_uiaccess_changed.connect(self.on_uac_uiaccess_changed)
        self.settings_tab.argv_emulation_changed.connect(self.on_argv_emulation_changed)
        self.settings_tab.osx_bundle_identifier_changed.connect(self.on_osx_bundle_identifier_changed)
        self.settings_tab.target_arch_changed.connect(self.on_target_arch_changed)
        self.settings_tab.codesign_identity_changed.connect(self.on_codesign_identity_changed)
        self.settings_tab.osx_entitlements_file_changed.connect(self.on_osx_entitlements_file_changed)
        
        # Advanced tab connections
        self.advanced_tab.log_level_changed.connect(self.on_log_level_changed)
        self.advanced_tab.upx_dir_changed.connect(self.on_upx_dir_changed)
        self.advanced_tab.debug_mode_changed.connect(self.on_debug_mode_changed)
        self.advanced_tab.clean_changed.connect(self.on_clean_changed)
        self.advanced_tab.noupx_changed.connect(self.on_noupx_changed)
        self.advanced_tab.upx_exclude_changed.connect(self.on_upx_exclude_changed)
        self.advanced_tab.optimize_level_changed.connect(self.on_optimize_level_changed)
        self.advanced_tab.strip_changed.connect(self.on_strip_changed)
        self.advanced_tab.python_options_changed.connect(self.on_python_options_changed)
        self.advanced_tab.noconfirm_changed.connect(self.on_noconfirm_changed)
        self.advanced_tab.contents_directory_changed.connect(self.on_contents_directory_changed)
        self.advanced_tab.bootloader_ignore_signals_changed.connect(self.on_bootloader_ignore_signals_changed)
        
        # Config tab connections
        self.config_tab.config_imported.connect(self.on_config_imported)
        
        # Run/Stop button connections
        self.run_button.clicked.connect(self.run_pyinstaller)
        self.stop_button.clicked.connect(self.stop_pyinstaller)
    
    # ------------------------------------------------------------------
    # Config dictionary <-> BuildConfig helpers
    # ------------------------------------------------------------------
    def get_current_config_dict(self) -> dict:
        """
        Get current configuration as dictionary.
        
        Converts the current BuildConfig object into a serializable dictionary
        suitable for JSON export.
        
        Returns:
            Dictionary containing all current build configuration settings.
        """
        cfg = self.build_config
        config = {
            "script_path": str(cfg.script_path) if cfg.script_path else "",
            "app_name": cfg.app_name,
            "onefile": cfg.onefile,
            "noconsole": cfg.noconsole,
            "hidden_imports": cfg.hidden_imports,
            "icon_path": str(cfg.icon_path) if cfg.icon_path else "",
            "output_folder": str(cfg.output_folder) if cfg.output_folder else "",
            "additional_files": [
                {"path": item.path, "type": str(item.file_type), "dest": item.dest}
                for item in cfg.additional_files
            ],
            "log_level": cfg.log_level,
            "upx_dir": str(cfg.upx_dir) if cfg.upx_dir else "",
            "debug_mode": cfg.debug_mode,
            "clean_cache": cfg.clean_cache,
            "tmpdir": cfg.tmpdir,
            "custom_commands": cfg.custom_commands,
            # Imports & Hooks
            "search_paths": cfg.search_paths,
            "exclude_modules": cfg.exclude_modules,
            "collect_all": cfg.collect_all,
            "collect_submodules": cfg.collect_submodules,
            "collect_data": cfg.collect_data,
            "collect_binaries": cfg.collect_binaries,
            "copy_metadata": cfg.copy_metadata,
            "recursive_copy_metadata": cfg.recursive_copy_metadata,
            "additional_hooks_dir": cfg.additional_hooks_dir,
            "runtime_hooks": cfg.runtime_hooks,
            "splash_image": cfg.splash_image,
            # Build behavior
            "noconfirm": cfg.noconfirm,
            "strip": cfg.strip,
            "noupx": cfg.noupx,
            "upx_exclude": cfg.upx_exclude,
            "optimize_level": cfg.optimize_level,
            "python_options": cfg.python_options,
            "contents_directory": cfg.contents_directory,
            "specpath": cfg.specpath,
            "workpath": cfg.workpath,
            "bootloader_ignore_signals": cfg.bootloader_ignore_signals,
            # Windows / macOS
            "console_explicit": cfg.console_explicit,
            "hide_console": cfg.hide_console,
            "disable_windowed_traceback": cfg.disable_windowed_traceback,
            "version_file": cfg.version_file,
            "manifest_file": cfg.manifest_file,
            "uac_admin": cfg.uac_admin,
            "uac_uiaccess": cfg.uac_uiaccess,
            "argv_emulation": cfg.argv_emulation,
            "osx_bundle_identifier": cfg.osx_bundle_identifier,
            "target_arch": cfg.target_arch,
            "codesign_identity": cfg.codesign_identity,
            "osx_entitlements_file": cfg.osx_entitlements_file,
        }
        return config
    
    def update_config_preview(self, *args):
        """
        Update the config preview in Config tab.
        
        Called whenever any configuration setting changes to keep the
        preview in sync with the current state.
        """
        config_dict = self.get_current_config_dict()
        self.config_tab.update_config_preview(config_dict)
    
    def on_config_imported(self, config: dict):
        """
        Handle imported configuration.
        
        Applies all settings from an imported configuration dictionary
        to the respective UI elements. Every field is optional so that
        older configuration files (missing newer keys) still import
        cleanly with sensible defaults.
        
        Args:
            config: Configuration dictionary to apply.
        """
        try:
            # General settings
            if config.get("script_path"):
                self.general_tab.script_path.setText(config["script_path"])
            
            if config.get("app_name"):
                self.general_tab.app_name_input.setText(config["app_name"])
            
            self.general_tab.onefile_checkbox.setChecked(config.get("onefile", False))
            self.general_tab.noconsole_checkbox.setChecked(config.get("noconsole", False))
            
            if config.get("hidden_imports"):
                self.general_tab.hidden_imports.setText(", ".join(config["hidden_imports"]))
            
            # File settings
            if config.get("additional_files"):
                for file_item in config["additional_files"]:
                    path = file_item.get("path", "")
                    file_type_str = file_item.get("type", "FILE")
                    dest = file_item.get("dest", ".")
                    
                    if "FILE" in file_type_str.upper():
                        self.files_tab.file_tree.add_file(path, FileType.FILE, dest)
                    elif "FOLDER" in file_type_str.upper():
                        self.files_tab.file_tree.add_file(path, FileType.FOLDER, dest)
                    elif "BINARY" in file_type_str.upper():
                        self.files_tab.file_tree.add_file(path, FileType.BINARY, dest)
            
            # Imports & Hooks settings
            self.imports_tab.search_paths_input.setText(", ".join(config.get("search_paths", [])))
            self.imports_tab.exclude_modules_input.setText(", ".join(config.get("exclude_modules", [])))
            self.imports_tab.collect_all_input.setText(", ".join(config.get("collect_all", [])))
            self.imports_tab.collect_submodules_input.setText(", ".join(config.get("collect_submodules", [])))
            self.imports_tab.collect_data_input.setText(", ".join(config.get("collect_data", [])))
            self.imports_tab.collect_binaries_input.setText(", ".join(config.get("collect_binaries", [])))
            self.imports_tab.copy_metadata_input.setText(", ".join(config.get("copy_metadata", [])))
            self.imports_tab.recursive_copy_metadata_input.setText(", ".join(config.get("recursive_copy_metadata", [])))
            if config.get("additional_hooks_dir"):
                self.imports_tab.hooks_dir_input.setText(config["additional_hooks_dir"])
            if config.get("runtime_hooks"):
                self.imports_tab.runtime_hooks_input.setText(", ".join(config["runtime_hooks"]))
            if config.get("splash_image"):
                self.imports_tab.splash_input.setText(config["splash_image"])
            
            # Output settings
            if config.get("output_folder"):
                self.settings_tab.output_folder_path.setText(config["output_folder"])
            
            if config.get("icon_path"):
                self.settings_tab.icon_path.setText(config["icon_path"])
            
            if config.get("tmpdir"):
                self.settings_tab.tmpdir_input.setText(config["tmpdir"])
            
            if config.get("specpath"):
                self.settings_tab.specpath_input.setText(config["specpath"])
            if config.get("workpath"):
                self.settings_tab.workpath_input.setText(config["workpath"])
            
            self.settings_tab.console_mode_combo.setCurrentIndex(1 if config.get("console_explicit") else 0)
            if config.get("hide_console"):
                index = self.settings_tab.hide_console_combo.findText(config["hide_console"])
                if index >= 0:
                    self.settings_tab.hide_console_combo.setCurrentIndex(index)
            self.settings_tab.cmd_disable_traceback.setChecked(config.get("disable_windowed_traceback", False))
            if config.get("version_file"):
                self.settings_tab.version_file_input.setText(config["version_file"])
            if config.get("manifest_file"):
                self.settings_tab.manifest_input.setText(config["manifest_file"])
            self.settings_tab.cmd_uac_admin.setChecked(config.get("uac_admin", False))
            self.settings_tab.cmd_uac_uiaccess.setChecked(config.get("uac_uiaccess", False))
            
            self.settings_tab.cmd_argv_emulation.setChecked(config.get("argv_emulation", False))
            if config.get("osx_bundle_identifier"):
                self.settings_tab.bundle_id_input.setText(config["osx_bundle_identifier"])
            if config.get("target_arch"):
                index = self.settings_tab.target_arch_combo.findText(config["target_arch"])
                if index >= 0:
                    self.settings_tab.target_arch_combo.setCurrentIndex(index)
            if config.get("codesign_identity"):
                self.settings_tab.codesign_identity_input.setText(config["codesign_identity"])
            if config.get("osx_entitlements_file"):
                self.settings_tab.entitlements_input.setText(config["osx_entitlements_file"])
            
            if config.get("custom_commands"):
                self.settings_tab.custom_commands.setText(config["custom_commands"])
            
            # Advanced settings
            if config.get("log_level"):
                index = self.advanced_tab.log_level_combo.findText(config["log_level"].upper())
                if index >= 0:
                    self.advanced_tab.log_level_combo.setCurrentIndex(index)
            
            self.advanced_tab.cmd_noupx.setChecked(config.get("noupx", False))
            if config.get("upx_dir"):
                self.advanced_tab.upx_path.setText(config["upx_dir"])
            if config.get("upx_exclude"):
                self.advanced_tab.upx_exclude_input.setText(", ".join(config["upx_exclude"]))
            
            if config.get("debug_mode"):
                index = self.advanced_tab.debug_combo.findText(config["debug_mode"].lower())
                if index >= 0:
                    self.advanced_tab.debug_combo.setCurrentIndex(index)
            
            if config.get("optimize_level"):
                index = self.advanced_tab.optimize_combo.findText(config["optimize_level"])
                if index >= 0:
                    self.advanced_tab.optimize_combo.setCurrentIndex(index)
            self.advanced_tab.cmd_strip.setChecked(config.get("strip", False))
            if config.get("python_options"):
                self.advanced_tab.python_options_input.setText(", ".join(config["python_options"]))
            
            self.advanced_tab.cmd_clean.setChecked(config.get("clean_cache", False))
            self.advanced_tab.cmd_noconfirm.setChecked(config.get("noconfirm", False))
            self.advanced_tab.cmd_bootloader_ignore_signals.setChecked(config.get("bootloader_ignore_signals", False))
            if config.get("contents_directory"):
                self.advanced_tab.contents_dir_input.setText(config["contents_directory"])
            
            QMessageBox.information(
                self, "Import Complete",
                "Configuration has been applied successfully."
            )
            
        except Exception as e:
            QMessageBox.critical(
                self, "Import Error",
                f"Error applying configuration:\n{str(e)}"
            )
    
    # ------------------------------------------------------------------
    # General tab handlers
    # ------------------------------------------------------------------
    def on_script_changed(self, path: str):
        """Handle script path change."""
        self.build_config.script_path = Path(path) if path else None
        self.update_command()
    
    def on_app_name_changed(self, name: str):
        """Handle app name change."""
        self.build_config.app_name = name
        self.update_command()
    
    def on_onefile_changed(self, checked: bool):
        """Handle onefile option change."""
        self.build_config.onefile = checked
        self.update_command()
    
    def on_noconsole_changed(self, checked: bool):
        """Handle noconsole option change."""
        self.build_config.noconsole = checked
        self.update_command()
    
    def on_hidden_imports_changed(self, imports: str):
        """Handle hidden imports change."""
        self.build_config.hidden_imports = self._split(imports)
        self.update_command()
    
    def on_files_changed(self, items: list):
        """Handle additional files change."""
        self.build_config.additional_files = items
        self.update_command()
    
    # ------------------------------------------------------------------
    # Imports & Hooks tab handlers
    # ------------------------------------------------------------------
    def on_search_paths_changed(self, value: str):
        self.build_config.search_paths = self._split(value)
        self.update_command()
    
    def on_exclude_modules_changed(self, value: str):
        self.build_config.exclude_modules = self._split(value)
        self.update_command()
    
    def on_collect_all_changed(self, value: str):
        self.build_config.collect_all = self._split(value)
        self.update_command()
    
    def on_collect_submodules_changed(self, value: str):
        self.build_config.collect_submodules = self._split(value)
        self.update_command()
    
    def on_collect_data_changed(self, value: str):
        self.build_config.collect_data = self._split(value)
        self.update_command()
    
    def on_collect_binaries_changed(self, value: str):
        self.build_config.collect_binaries = self._split(value)
        self.update_command()
    
    def on_copy_metadata_changed(self, value: str):
        self.build_config.copy_metadata = self._split(value)
        self.update_command()
    
    def on_recursive_copy_metadata_changed(self, value: str):
        self.build_config.recursive_copy_metadata = self._split(value)
        self.update_command()
    
    def on_additional_hooks_dir_changed(self, value: str):
        self.build_config.additional_hooks_dir = value
        self.update_command()
    
    def on_runtime_hooks_changed(self, value: str):
        self.build_config.runtime_hooks = self._split(value)
        self.update_command()
    
    def on_splash_image_changed(self, value: str):
        self.build_config.splash_image = value
        self.update_command()
    
    # ------------------------------------------------------------------
    # Settings tab handlers
    # ------------------------------------------------------------------
    def on_output_folder_changed(self, folder: str):
        """Handle output folder change."""
        self.build_config.output_folder = Path(folder) if folder else None
        self.update_command()
    
    def on_custom_commands_changed(self, commands: str):
        """Handle custom commands change."""
        self.build_config.custom_commands = commands
        self.update_command()
    
    def on_icon_path_changed(self, path: str):
        """Handle icon path change."""
        self.build_config.icon_path = Path(path) if path else None
        self.update_command()
    
    def on_tmpdir_changed(self, tmpdir: str):
        """Handle tmpdir change."""
        self.build_config.tmpdir = tmpdir
        self.update_command()
    
    def on_specpath_changed(self, value: str):
        self.build_config.specpath = value
        self.update_command()
    
    def on_workpath_changed(self, value: str):
        self.build_config.workpath = value
        self.update_command()
    
    def on_console_explicit_changed(self, checked: bool):
        self.build_config.console_explicit = checked
        self.update_command()
    
    def on_hide_console_changed(self, value: str):
        self.build_config.hide_console = value
        self.update_command()
    
    def on_disable_windowed_traceback_changed(self, checked: bool):
        self.build_config.disable_windowed_traceback = checked
        self.update_command()
    
    def on_version_file_changed(self, value: str):
        self.build_config.version_file = value
        self.update_command()
    
    def on_manifest_file_changed(self, value: str):
        self.build_config.manifest_file = value
        self.update_command()
    
    def on_uac_admin_changed(self, checked: bool):
        self.build_config.uac_admin = checked
        self.update_command()
    
    def on_uac_uiaccess_changed(self, checked: bool):
        self.build_config.uac_uiaccess = checked
        self.update_command()
    
    def on_argv_emulation_changed(self, checked: bool):
        self.build_config.argv_emulation = checked
        self.update_command()
    
    def on_osx_bundle_identifier_changed(self, value: str):
        self.build_config.osx_bundle_identifier = value
        self.update_command()
    
    def on_target_arch_changed(self, value: str):
        self.build_config.target_arch = value
        self.update_command()
    
    def on_codesign_identity_changed(self, value: str):
        self.build_config.codesign_identity = value
        self.update_command()
    
    def on_osx_entitlements_file_changed(self, value: str):
        self.build_config.osx_entitlements_file = value
        self.update_command()
    
    # ------------------------------------------------------------------
    # Advanced tab handlers
    # ------------------------------------------------------------------
    def on_log_level_changed(self, level: str):
        """Handle log level change."""
        self.build_config.log_level = level
        self.update_command()
    
    def on_upx_dir_changed(self, path: str):
        """Handle UPX directory change."""
        self.build_config.upx_dir = Path(path) if path else None
        self.update_command()
    
    def on_debug_mode_changed(self, mode: str):
        """Handle debug mode change."""
        self.build_config.debug_mode = mode.lower()
        self.update_command()
    
    def on_clean_changed(self, checked: bool):
        """Handle clean cache option change."""
        self.build_config.clean_cache = checked
        self.update_command()
    
    def on_noupx_changed(self, checked: bool):
        self.build_config.noupx = checked
        self.update_command()
    
    def on_upx_exclude_changed(self, value: str):
        self.build_config.upx_exclude = self._split(value)
        self.update_command()
    
    def on_optimize_level_changed(self, value: str):
        self.build_config.optimize_level = value
        self.update_command()
    
    def on_strip_changed(self, checked: bool):
        self.build_config.strip = checked
        self.update_command()
    
    def on_python_options_changed(self, value: str):
        self.build_config.python_options = self._split(value)
        self.update_command()
    
    def on_noconfirm_changed(self, checked: bool):
        self.build_config.noconfirm = checked
        self.update_command()
    
    def on_contents_directory_changed(self, value: str):
        self.build_config.contents_directory = value
        self.update_command()
    
    def on_bootloader_ignore_signals_changed(self, checked: bool):
        self.build_config.bootloader_ignore_signals = checked
        self.update_command()
    
    @staticmethod
    def _split(text: str) -> list:
        """
        Split a comma-separated string into a clean list.
        
        Args:
            text: Raw comma-separated text from a QLineEdit.
        
        Returns:
            List of trimmed, non-empty strings.
        """
        if not text:
            return []
        return [item.strip() for item in text.split(",") if item.strip()]
    
    def update_command(self):
        """
        Update the command preview.
        
        Rebuilds the PyInstaller command based on current configuration
        and updates the output widget display, and refreshes the
        Config tab's live preview at the same time.
        """
        if not self.build_config.script_path:
            self.output_widget.set_command_text("Error: No script selected!")
        else:
            self.command_builder.set_config(self.build_config)
            command = self.command_builder.build()
            self.output_widget.set_command_text(command)
        
        self.update_config_preview()
    
    def recolor_icon(self, icon_path: str, color: QColor) -> QIcon:
        """
        Recolor an icon to the specified color.
        
        Args:
            icon_path: Path to the source icon file.
            color: Target color for recoloring.
            
        Returns:
            Recolored QIcon object.
        """
        icon = QIcon(icon_path)
        pixmap = icon.pixmap(16, 16)
        painter = QPainter(pixmap)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), color)
        painter.end()
        return QIcon(pixmap)
    
    def apply_theme(self):
        """Apply the current theme to the entire application."""
        theme_setting = self.config_manager.get('theme', 'system')
        
        if theme_setting == 'system':
            is_dark = self.config_manager.get_effective_theme() == 'dark'
            icon_name = "system.svg"
        elif theme_setting == 'dark':
            is_dark = True
            icon_name = "light.svg"
        else:
            is_dark = False
            icon_name = "dark.svg"
        
        self.setStyleSheet(get_stylesheet(is_dark))
        
        base_path = os.path.dirname(os.path.abspath(__file__))
        icons_path = os.path.join(base_path, "icons")
        
        icon_path = os.path.join(icons_path, icon_name)
        
        if icon_name == "system.svg":
            if is_dark:
                icon = self.recolor_icon(icon_path, QColor(255, 255, 255))
            else:
                icon = self.recolor_icon(icon_path, QColor(0, 0, 0))
        else:
            icon = QIcon(icon_path)
        
        self.header.set_theme_icon(icon)
    
    def toggle_theme(self):
        """
        Toggle between theme modes.
        
        Cycles through: system -> light -> dark -> system
        """
        current = self.config_manager.get('theme', 'system')
        if current == 'system':
            self.config_manager.set('theme', 'light')
        elif current == 'light':
            self.config_manager.set('theme', 'dark')
        else:
            self.config_manager.set('theme', 'system')
        self.apply_theme()
    
    def open_github(self):
        """Open GitHub repository in the default web browser."""
        webbrowser.open("https://github.com/inject3r/pyinstaller-gui")
    
    def run_pyinstaller(self):
        """
        Run PyInstaller with the current configuration.
        
        Builds the argument list directly from the current BuildConfig
        (rather than re-parsing the displayed preview text) and runs it
        through PyInstallerWorker, which invokes
        ``<sys.executable> -m PyInstaller`` without a shell. While a build
        is running, the Run button is disabled and the Stop button becomes
        active so the user can cancel it.
        """
        self.command_builder.set_config(self.build_config)
        try:
            args = self.command_builder.build_args()
        except ValueError as exc:
            QMessageBox.warning(self, "Cannot Start Build", str(exc))
            return
        
        self.output_widget.clear_output()
        self.run_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        
        self.worker = PyInstallerWorker(args)
        self.worker.output_signal.connect(self.output_widget.append_output)
        self.worker.finished_signal.connect(self.on_build_finished)
        self.worker.start()
    
    def stop_pyinstaller(self):
        """Cancel the currently running PyInstaller build, if any."""
        if self.worker is not None:
            self.stop_button.setEnabled(False)
            self.worker.stop()
    
    def on_build_finished(self, return_code: int):
        """
        Handle completion of a PyInstaller build.
        
        Re-enables the Run button, disables Stop, and shows a brief
        success/failure notification. On success, offers to open the
        output folder.
        
        Args:
            return_code: The PyInstaller process exit code (0 on success,
                -1 if it failed to start or was cancelled by the user).
        """
        self.run_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        
        if return_code == 0:
            reply = QMessageBox.question(
                self, "Build Succeeded",
                "PyInstaller finished successfully.\n\nOpen the output folder now?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.open_output_folder()
        elif return_code != -1:
            QMessageBox.warning(
                self, "Build Failed",
                f"PyInstaller exited with code {return_code}.\n"
                "Check the output above for details."
            )
    
    def open_output_folder(self):
        """
        Open the configured (or default) dist folder in the system file browser.
        
        Falls back to PyInstaller's default "./dist" directory when no
        custom output folder has been set.
        """
        folder = self.build_config.output_folder or Path("dist")
        folder = Path(folder)
        if not folder.exists():
            QMessageBox.information(
                self, "Folder Not Found",
                f"Could not find the output folder:\n{folder}"
            )
            return
        
        try:
            if os.name == "nt":
                os.startfile(str(folder))  # noqa: S606 - user-initiated, trusted local path
            elif os.uname().sysname == "Darwin":
                import subprocess
                subprocess.Popen(["open", str(folder)])
            else:
                import subprocess
                subprocess.Popen(["xdg-open", str(folder)])
        except OSError as exc:
            QMessageBox.warning(self, "Could Not Open Folder", str(exc))
    
    def display_versions(self):
        """
        Display Python and PyInstaller versions.
        
        Retrieves version information and updates the version widget.
        """
        python_version = self.version_checker.get_python_version()
        pyinstaller_version = self.version_checker.get_pyinstaller_version()
        
        self.version_widget.set_python_version(python_version)
        self.version_widget.set_pyinstaller_version(pyinstaller_version)
