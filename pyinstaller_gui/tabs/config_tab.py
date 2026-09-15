"""Configuration import/export tab."""

import json
from datetime import datetime
from pathlib import Path

from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, 
    QMessageBox, QGroupBox, QTextEdit, QScrollArea
)
from PyQt6.QtCore import pyqtSignal, Qt

from .base_tab import BaseTab


class ConfigTab(BaseTab):
    """
    Tab for exporting and importing configuration.
    
    This tab allows users to save their current build configuration to a JSON
    file and load previously saved configurations. This is useful for:
    - Saving different configurations for different projects
    - Sharing build settings with team members
    - Backing up settings before major changes
    - Creating configuration templates
    
    The tab includes a live preview of the current configuration in a
    scrollable text area for easy review before exporting.
    """
    
    config_exported = pyqtSignal(dict)
    config_imported = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        """
        Initialize the configuration tab.
        
        Args:
            parent: Parent widget (default: None).
        """
        super().__init__(parent)
        self.current_config = {}
        self.init_ui()
    
    def init_ui(self):
        """
        Initialize the user interface.
        
        Creates the header with help button, export and import sections,
        and a scrollable preview area showing the current configuration
        in a human-readable format.
        """
        # Help button in header
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 5)
        
        header_label = QLabel("Configuration Management")
        header_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        
        self.config_help_button = QPushButton("?")
        self.config_help_button.setFixedSize(24, 24)
        self.config_help_button.setToolTip("Show help for Configuration management")
        self.config_help_button.setStyleSheet("""
            QPushButton {
                background-color: #2D8FBA;
                color: white;
                border-radius: 12px;
                font-weight: bold;
                font-size: 14px;
                padding: 0px;
                margin: 0px;
            }
            QPushButton:hover {
                background-color: #1A5C7E;
            }
        """)
        
        header_layout.addWidget(header_label)
        header_layout.addStretch()
        header_layout.addWidget(self.config_help_button)
        
        self.main_layout.addWidget(header_widget)
        
        # Export section
        export_group = QGroupBox("Export Configuration")
        export_layout = QVBoxLayout()
        
        export_desc = QLabel(
            "Export current build configuration to a JSON file.\n"
            "This will save all settings including script path, application name, "
            "additional files, and advanced options."
        )
        export_desc.setWordWrap(True)
        export_desc.setStyleSheet("color: #7A8089;")
        
        self.export_button = QPushButton("Export Configuration")
        self.export_button.setFixedHeight(35)
        self.export_button.setToolTip("Save current settings to a JSON file")
        
        export_layout.addWidget(export_desc)
        export_layout.addWidget(self.export_button)
        export_group.setLayout(export_layout)
        
        # Import section
        import_group = QGroupBox("Import Configuration")
        import_layout = QVBoxLayout()
        
        import_desc = QLabel(
            "Import a previously exported configuration file.\n"
            "This will load all settings from the selected JSON file."
        )
        import_desc.setWordWrap(True)
        import_desc.setStyleSheet("color: #7A8089;")
        
        self.import_button = QPushButton("Import Configuration")
        self.import_button.setFixedHeight(35)
        self.import_button.setToolTip("Load settings from a JSON file")
        
        import_layout.addWidget(import_desc)
        import_layout.addWidget(self.import_button)
        import_group.setLayout(import_layout)
        
        # Current config preview with scroll area
        preview_group = QGroupBox("Current Configuration Preview")
        preview_layout = QVBoxLayout()
        
        # Create scroll area for config preview
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedHeight(100)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setToolTip("Preview of current configuration (scrollable)")
        
        # Create text edit widget
        self.config_preview = QTextEdit()
        self.config_preview.setReadOnly(True)
        self.config_preview.setPlaceholderText("No configuration loaded...")
        self.config_preview.setStyleSheet("""
            QTextEdit {
                border-radius: 6px;
                padding: 8px;
                font-family: 'Courier New', monospace;
                font-size: 11px;
            }
        """)
        
        # Add text edit to scroll area
        self.scroll_area.setWidget(self.config_preview)
        
        preview_layout.addWidget(self.scroll_area)
        preview_group.setLayout(preview_layout)
        
        # Buttons layout
        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(buttons_widget)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(20)
        buttons_layout.addWidget(export_group)
        buttons_layout.addWidget(import_group)
        
        # Add to main layout
        self.main_layout.addWidget(buttons_widget)
        self.main_layout.addWidget(preview_group)
        self.main_layout.addStretch()
        
        # Connect signals
        self.export_button.clicked.connect(self.export_config)
        self.import_button.clicked.connect(self.import_config)
        self.config_help_button.clicked.connect(self.show_help)
    
    def update_config_preview(self, config: dict):
        """
        Update the configuration preview text.
        
        Args:
            config: The configuration dictionary to display in the preview area.
        """
        self.current_config = config
        if config:
            preview = self._format_config_for_preview(config)
            self.config_preview.setText(preview)
            self.config_preview.moveCursor(self.config_preview.textCursor().MoveOperation.Start)
        else:
            self.config_preview.clear()
            self.config_preview.setPlaceholderText("No configuration loaded...")
    
    def _format_config_for_preview(self, config: dict) -> str:
        """
        Format configuration for preview display.
        
        Converts the configuration dictionary into a human-readable text format
        with categorized sections and indentation.
        
        Args:
            config: The configuration dictionary to format.
            
        Returns:
            Formatted string containing a readable representation of the config.
        """
        lines = []
        lines.append("=" * 50)
        lines.append("PYINSTALLER GUI CONFIGURATION")
        lines.append("=" * 50)
        lines.append(f"Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        
        # General settings
        lines.append("【GENERAL SETTINGS】")
        lines.append(f"  Script Path: {config.get('script_path', 'Not set')}")
        lines.append(f"  Application Name: {config.get('app_name', 'Not set')}")
        lines.append(f"  OneFile: {config.get('onefile', False)}")
        lines.append(f"  No Console: {config.get('noconsole', False)}")
        lines.append(f"  Hidden Imports: {', '.join(config.get('hidden_imports', [])) or 'None'}")
        lines.append("")
        
        # File settings
        lines.append("【ADDITIONAL FILES】")
        files = config.get('additional_files', [])
        if files:
            for i, file_item in enumerate(files, 1):
                lines.append(f"  {i}. {file_item.get('path', 'Unknown')} ({file_item.get('type', 'Unknown')})")
        else:
            lines.append("  No additional files")
        lines.append("")
        
        # Advanced settings
        lines.append("【ADVANCED SETTINGS】")
        lines.append(f"  Log Level: {config.get('log_level', 'INFO')}")
        lines.append(f"  UPX Directory: {config.get('upx_dir', 'Not set')}")
        lines.append(f"  Debug Mode: {config.get('debug_mode', 'none')}")
        lines.append(f"  Clean Cache: {config.get('clean_cache', False)}")
        lines.append("")
        
        # Output settings
        lines.append("【OUTPUT SETTINGS】")
        lines.append(f"  Output Folder: {config.get('output_folder', 'Not set')}")
        lines.append(f"  Icon Path: {config.get('icon_path', 'Not set')}")
        lines.append(f"  Runtime Tmpdir: {config.get('tmpdir', 'Not set')}")
        lines.append("")
        
        # Custom commands
        if config.get('custom_commands'):
            lines.append("【CUSTOM COMMANDS】")
            lines.append(f"  {config.get('custom_commands')}")
            lines.append("")
        
        lines.append("=" * 50)
        
        return "\n".join(lines)
    
    def export_config(self):
        """
        Export current configuration to JSON file.
        
        Opens a file save dialog with a timestamped default filename,
        exports the current configuration with metadata including version
        and export date. Shows success or error message dialog.
        """
        if not self.current_config:
            QMessageBox.warning(
                self, "No Configuration",
                "No configuration to export. Please configure the build settings first."
            )
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Configuration",
            f"pyinstaller_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            "JSON Files (*.json)"
        )
        
        if file_path:
            try:
                export_data = {
                    "version": "1.0",
                    "export_date": datetime.now().isoformat(),
                    "config": self.current_config
                }
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=4, ensure_ascii=False)
                
                QMessageBox.information(
                    self, "Export Successful",
                    f"Configuration successfully exported to:\n{file_path}"
                )
            except Exception as e:
                QMessageBox.critical(
                    self, "Export Failed",
                    f"Failed to export configuration:\n{str(e)}"
                )
    
    def import_config(self):
        """
        Import configuration from JSON file.
        
        Opens a file open dialog, validates the JSON structure, and emits
        the config_imported signal with the loaded configuration. Handles
        both new format (with metadata wrapper) and old format (config only).
        Shows appropriate error dialogs for invalid files.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Import Configuration",
            "",
            "JSON Files (*.json)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if "config" in data:
                    config = data["config"]
                else:
                    config = data
                
                if "script_path" not in config:
                    raise ValueError("Invalid configuration file: missing 'script_path'")
                
                self.config_imported.emit(config)
                
                QMessageBox.information(
                    self, "Import Successful",
                    f"Configuration successfully imported from:\n{file_path}\n\n"
                    "Settings have been applied."
                )
            except json.JSONDecodeError as e:
                QMessageBox.critical(
                    self, "Import Failed",
                    f"Invalid JSON file:\n{str(e)}"
                )
            except Exception as e:
                QMessageBox.critical(
                    self, "Import Failed",
                    f"Failed to import configuration:\n{str(e)}"
                )
    
    def get_current_config_dict(self) -> dict:
        """
        Get current configuration as dictionary.
        
        Returns:
            The current configuration dictionary.
        """
        return self.current_config
    
    def set_current_config(self, config: dict):
        """
        Set current configuration from dictionary.
        
        Args:
            config: The configuration dictionary to set.
        """
        self.current_config = config
        self.update_config_preview(config)
    
    def show_help(self):
        """
        Show help dialog for Config tab.
        
        Displays a message box with detailed explanations of:
        - Export configuration functionality and use cases
        - Import configuration functionality and validation
        - Configuration preview scrolling
        - Common use cases (project templates, team sharing, backups)
        """
        help_text = """
        <h3>Configuration Management Help</h3>
        
        <b>Export Configuration:</b><br>
        Saves all your current settings (script path, options, additional files, etc.)<br>
        to a JSON file. This allows you to reuse the same configuration later.<br><br>
        
        <b>Import Configuration:</b><br>
        Loads a previously exported JSON file and applies all settings.<br>
        This is useful for sharing build configurations between projects or users.<br><br>
        
        <b>Configuration Preview:</b><br>
        Shows a human-readable summary of the current configuration.<br>
        Scroll to see all settings when there are many additional files.<br><br>
        
        <b>Use Cases:</b><br>
        - Save different configurations for different projects<br>
        - Share build settings with team members<br>
        - Backup your settings before making major changes<br>
        - Create configuration templates
        """
        
        QMessageBox.information(self, "Configuration Management Help", help_text)