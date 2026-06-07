import subprocess
import webbrowser
import os
from pathlib import Path

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QTabWidget, QHBoxLayout,
    QTextEdit, QLabel, QMessageBox
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
    - Tab widget: General, Additional Files, Advanced, Settings, Config tabs
    - Output widget: Command preview and build console output
    - Version widget: Python and PyInstaller version display
    - Run button: Triggers the build process
    """
    
    def __init__(self):
        """Initialize the main GUI window."""
        super().__init__()
        self.config_manager = ConfigManager()
        self.command_builder = CommandBuilder()
        self.version_checker = VersionChecker()
        self.build_config = BuildConfig()
        
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
        self.advanced_tab = AdvancedTab()
        self.settings_tab = SettingsTab()
        self.config_tab = ConfigTab()
        
        self.tabs.addTab(self.general_tab, "General")
        self.tabs.addTab(self.files_tab, "Additional Files")
        self.tabs.addTab(self.advanced_tab, "Advanced")
        self.tabs.addTab(self.settings_tab, "Settings")
        self.tabs.addTab(self.config_tab, "Config")
        
        self.output_widget = OutputWidget()
        self.version_widget = VersionWidget()
        
        self.run_button = QPushButton("Run PyInstaller")
        self.run_button.setFixedHeight(40)
        
        self.main_layout.addWidget(self.header)
        self.main_layout.addWidget(self.tabs)
        self.main_layout.addWidget(self.output_widget)
        self.main_layout.addWidget(self.version_widget)
        self.main_layout.addWidget(self.run_button)
        
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
        
        # Settings tab connections
        self.settings_tab.output_folder_changed.connect(self.on_output_folder_changed)
        self.settings_tab.custom_commands_changed.connect(self.on_custom_commands_changed)
        self.settings_tab.icon_path_changed.connect(self.on_icon_path_changed)
        self.settings_tab.tmpdir_changed.connect(self.on_tmpdir_changed)
        
        # Advanced tab connections
        self.advanced_tab.log_level_changed.connect(self.on_log_level_changed)
        self.advanced_tab.upx_dir_changed.connect(self.on_upx_dir_changed)
        self.advanced_tab.debug_mode_changed.connect(self.on_debug_mode_changed)
        self.advanced_tab.clean_changed.connect(self.on_clean_changed)
        
        # Config tab connections
        self.config_tab.config_imported.connect(self.on_config_imported)
        
        # Update config preview when any setting changes (for live preview)
        self.general_tab.script_changed.connect(self.update_config_preview)
        self.general_tab.app_name_changed.connect(self.update_config_preview)
        self.general_tab.onefile_changed.connect(self.update_config_preview)
        self.general_tab.noconsole_changed.connect(self.update_config_preview)
        self.general_tab.hidden_imports_changed.connect(self.update_config_preview)
        self.files_tab.files_changed.connect(self.update_config_preview)
        self.settings_tab.output_folder_changed.connect(self.update_config_preview)
        self.settings_tab.custom_commands_changed.connect(self.update_config_preview)
        self.settings_tab.icon_path_changed.connect(self.update_config_preview)
        self.settings_tab.tmpdir_changed.connect(self.update_config_preview)
        self.advanced_tab.log_level_changed.connect(self.update_config_preview)
        self.advanced_tab.upx_dir_changed.connect(self.update_config_preview)
        self.advanced_tab.debug_mode_changed.connect(self.update_config_preview)
        self.advanced_tab.clean_changed.connect(self.update_config_preview)
        
        # Run button connection
        self.run_button.clicked.connect(self.run_pyinstaller)
    
    def get_current_config_dict(self) -> dict:
        """
        Get current configuration as dictionary.
        
        Converts the current BuildConfig object into a serializable dictionary
        suitable for JSON export.
        
        Returns:
            Dictionary containing all current build configuration settings.
        """
        config = {
            "script_path": str(self.build_config.script_path) if self.build_config.script_path else "",
            "app_name": self.build_config.app_name,
            "onefile": self.build_config.onefile,
            "noconsole": self.build_config.noconsole,
            "hidden_imports": self.build_config.hidden_imports,
            "icon_path": str(self.build_config.icon_path) if self.build_config.icon_path else "",
            "output_folder": str(self.build_config.output_folder) if self.build_config.output_folder else "",
            "additional_files": [
                {"path": item.path, "type": str(item.file_type)} 
                for item in self.build_config.additional_files
            ],
            "log_level": self.build_config.log_level,
            "upx_dir": str(self.build_config.upx_dir) if self.build_config.upx_dir else "",
            "debug_mode": self.build_config.debug_mode,
            "clean_cache": self.build_config.clean_cache,
            "tmpdir": self.build_config.tmpdir,
            "custom_commands": self.build_config.custom_commands
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
        to the respective UI elements.
        
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
                    
                    if "FILE" in file_type_str.upper():
                        self.files_tab.file_tree.add_file(path, FileType.FILE)
                    elif "FOLDER" in file_type_str.upper():
                        self.files_tab.file_tree.add_file(path, FileType.FOLDER)
                    elif "BINARY" in file_type_str.upper():
                        self.files_tab.file_tree.add_file(path, FileType.BINARY)
            
            # Output settings
            if config.get("output_folder"):
                self.settings_tab.output_folder_path.setText(config["output_folder"])
            
            if config.get("icon_path"):
                self.settings_tab.icon_path.setText(config["icon_path"])
            
            if config.get("tmpdir"):
                self.settings_tab.tmpdir_input.setText(config["tmpdir"])
            
            if config.get("custom_commands"):
                self.settings_tab.custom_commands.setText(config["custom_commands"])
            
            # Advanced settings
            if config.get("log_level"):
                index = self.advanced_tab.log_level_combo.findText(config["log_level"].upper())
                if index >= 0:
                    self.advanced_tab.log_level_combo.setCurrentIndex(index)
            
            if config.get("upx_dir"):
                self.advanced_tab.upx_path.setText(config["upx_dir"])
            
            if config.get("debug_mode"):
                index = self.advanced_tab.debug_combo.findText(config["debug_mode"].lower())
                if index >= 0:
                    self.advanced_tab.debug_combo.setCurrentIndex(index)
            
            self.advanced_tab.cmd_clean.setChecked(config.get("clean_cache", False))
            
            QMessageBox.information(
                self, "Import Complete",
                "Configuration has been applied successfully."
            )
            
        except Exception as e:
            QMessageBox.critical(
                self, "Import Error",
                f"Error applying configuration:\n{str(e)}"
            )
    
    def on_script_changed(self, path: str):
        """
        Handle script path change.
        
        Args:
            path: New script path.
        """
        self.build_config.script_path = Path(path) if path else None
        self.update_command()
    
    def on_app_name_changed(self, name: str):
        """
        Handle app name change.
        
        Args:
            name: New application name.
        """
        self.build_config.app_name = name
        self.update_command()
    
    def on_onefile_changed(self, checked: bool):
        """
        Handle onefile option change.
        
        Args:
            checked: True if onefile mode is enabled.
        """
        self.build_config.onefile = checked
        self.update_command()
    
    def on_noconsole_changed(self, checked: bool):
        """
        Handle noconsole option change.
        
        Args:
            checked: True if console window should be hidden.
        """
        self.build_config.noconsole = checked
        self.update_command()
    
    def on_hidden_imports_changed(self, imports: str):
        """
        Handle hidden imports change.
        
        Parses comma-separated string into a list of module names.
        
        Args:
            imports: Comma-separated list of hidden imports.
        """
        if imports:
            self.build_config.hidden_imports = [imp.strip() for imp in imports.split(',') if imp.strip()]
        else:
            self.build_config.hidden_imports = []
        self.update_command()
    
    def on_files_changed(self, items: list):
        """
        Handle additional files change.
        
        Args:
            items: List of FileItem objects.
        """
        self.build_config.additional_files = items
        self.update_command()
    
    def on_output_folder_changed(self, folder: str):
        """
        Handle output folder change.
        
        Args:
            folder: New output folder path.
        """
        self.build_config.output_folder = Path(folder) if folder else None
        self.update_command()
    
    def on_custom_commands_changed(self, commands: str):
        """
        Handle custom commands change.
        
        Args:
            commands: Additional PyInstaller command-line arguments.
        """
        self.build_config.custom_commands = commands
        self.update_command()
    
    def on_icon_path_changed(self, path: str):
        """
        Handle icon path change.
        
        Args:
            path: Path to the icon file.
        """
        self.build_config.icon_path = Path(path) if path else None
        self.update_command()
    
    def on_tmpdir_changed(self, tmpdir: str):
        """
        Handle tmpdir change.
        
        Args:
            tmpdir: Custom temporary directory path.
        """
        self.build_config.tmpdir = tmpdir
        self.update_command()
    
    def on_log_level_changed(self, level: str):
        """
        Handle log level change.
        
        Args:
            level: Log level string (INFO, DEBUG, WARN, etc.).
        """
        self.build_config.log_level = level
        self.update_command()
    
    def on_upx_dir_changed(self, path: str):
        """
        Handle UPX directory change.
        
        Args:
            path: Path to UPX installation directory.
        """
        self.build_config.upx_dir = Path(path) if path else None
        self.update_command()
    
    def on_debug_mode_changed(self, mode: str):
        """
        Handle debug mode change.
        
        Args:
            mode: Debug mode (none, all, imports, bootloader, noarchive).
        """
        self.build_config.debug_mode = mode.lower()
        self.update_command()
    
    def on_clean_changed(self, checked: bool):
        """
        Handle clean cache option change.
        
        Args:
            checked: True if clean cache is enabled.
        """
        self.build_config.clean_cache = checked
        self.update_command()
    
    def update_command(self):
        """
        Update the command preview.
        
        Rebuilds the PyInstaller command based on current configuration
        and updates the output widget display.
        """
        if not self.build_config.script_path:
            self.output_widget.set_command_text("Error: No script selected!")
            return
        
        self.command_builder.set_config(self.build_config)
        command = self.command_builder.build()
        self.output_widget.set_command_text(command)
    
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
        Run PyInstaller with current configuration.
        
        Starts a worker thread to execute PyInstaller command, preventing
        GUI freezing during the build process.
        """
        command = self.output_widget.get_command_text()
        if command.startswith("Error"):
            return
        
        self.output_widget.clear_output()
        self.worker = PyInstallerWorker(command)
        self.worker.output_signal.connect(self.output_widget.append_output)
        self.worker.start()
    
    def display_versions(self):
        """
        Display Python and PyInstaller versions.
        
        Retrieves version information and updates the version widget.
        """
        python_version = self.version_checker.get_python_version()
        pyinstaller_version = self.version_checker.get_pyinstaller_version()
        
        self.version_widget.set_python_version(python_version)
        self.version_widget.set_pyinstaller_version(pyinstaller_version)