"""Advanced configuration tab."""

from PyQt6.QtWidgets import (
    QWidget, QLabel, QComboBox, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, 
    QCheckBox, QFileDialog, QMessageBox
)
from PyQt6.QtCore import pyqtSignal

from .base_tab import BaseTab


class AdvancedTab(BaseTab):
    """
    Tab for advanced PyInstaller configuration.
    
    This tab provides advanced build options including:
    - Log level control for build output verbosity
    - UPX directory path for executable compression
    - Debug mode options for troubleshooting
    - Clean cache option for resolving build issues
    """
    
    log_level_changed = pyqtSignal(str)
    upx_dir_changed = pyqtSignal(str)
    debug_mode_changed = pyqtSignal(str)
    clean_changed = pyqtSignal(bool)
    
    def __init__(self, parent=None):
        """
        Initialize the advanced tab.
        
        Args:
            parent: Parent widget (default: None).
        """
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """
        Initialize the user interface.
        
        Creates the header with help button, then arranges the log level
        combo box, UPX directory selection with browse button, debug mode
        combo box, and clean cache checkbox in a vertical layout.
        """
        # Help button in header
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 5)
        
        header_label = QLabel("Advanced Settings")
        header_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        
        self.advanced_help_button = QPushButton("?")
        self.advanced_help_button.setFixedSize(24, 24)
        self.advanced_help_button.setToolTip("Show help for Advanced settings")
        self.advanced_help_button.setStyleSheet("""
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
        header_layout.addWidget(self.advanced_help_button)
        
        self.main_layout.addWidget(header_widget)
        
        # Log level
        self.log_level_label = QLabel("Log Level:")
        self.log_level_label.setToolTip("Amount of detail in build-time console messages")
        
        self.log_level_combo = QComboBox()
        self.log_level_combo.addItems(["INFO", "DEBUG", "WARN", "ERROR", "TRACE", "DEPRECATION", "FATAL"])
        self.log_level_combo.setCurrentText("INFO")
        self.log_level_combo.setToolTip(
            "TRACE: Most detailed\n"
            "DEBUG: Debug information\n"
            "INFO: General information (default)\n"
            "WARN: Warnings only\n"
            "ERROR: Errors only\n"
            "FATAL: Critical errors only"
        )
        
        # UPX directory
        self.upx_label = QLabel("UPX Directory:")
        self.upx_label.setToolTip("Path to UPX utility for compressing binaries")
        
        self.upx_path = QLineEdit()
        self.upx_path.setPlaceholderText("Set the UPX path to compress binary files")
        self.upx_path.setToolTip("UPX (Ultimate Packer for eXecutables) reduces file size")
        
        self.upx_button = QPushButton("Browse")
        self.upx_button.setToolTip("Browse for UPX installation directory")
        
        upx_layout = QHBoxLayout()
        upx_layout.addWidget(self.upx_path)
        upx_layout.addWidget(self.upx_button)
        
        # Debug mode
        self.debug_label = QLabel("Debug Mode:")
        self.debug_label.setToolTip("Enable debug features for troubleshooting")
        
        self.debug_combo = QComboBox()
        self.debug_combo.addItems(["none", "all", "imports", "bootloader", "noarchive"])
        self.debug_combo.setToolTip(
            "none: No debugging (default)\n"
            "all: Enable all debug options\n"
            "imports: Show module import messages\n"
            "bootloader: Show bootloader progress\n"
            "noarchive: Store files as separate files instead of archive"
        )
        
        # Clean cache
        self.cmd_clean = QCheckBox("--clean (Clear PyInstaller cache and temp files before building.)")
        self.cmd_clean.setToolTip(
            "Cleans the PyInstaller cache and removes temporary files\n"
            "Use this if you encounter build issues"
        )
        
        # Add to layout
        self.main_layout.addWidget(self.log_level_label)
        self.main_layout.addWidget(self.log_level_combo)
        self.main_layout.addWidget(self.upx_label)
        self.main_layout.addLayout(upx_layout)
        self.main_layout.addWidget(self.debug_label)
        self.main_layout.addWidget(self.debug_combo)
        self.main_layout.addWidget(self.cmd_clean)
        self.main_layout.addStretch()
        
        # Connect signals
        self.log_level_combo.currentTextChanged.connect(self.log_level_changed.emit)
        self.upx_button.clicked.connect(self.select_upx_dir)
        self.upx_path.textChanged.connect(self.upx_dir_changed.emit)
        self.debug_combo.currentTextChanged.connect(self.debug_mode_changed.emit)
        self.cmd_clean.toggled.connect(self.clean_changed.emit)
        self.advanced_help_button.clicked.connect(self.show_help)
    
    def select_upx_dir(self):
        """
        Open directory dialog to select UPX directory.
        
        Opens a directory selection dialog and updates the UPX path field
        with the selected directory if one is chosen.
        """
        dir_path = QFileDialog.getExistingDirectory(self, "Select UPX Directory")
        if dir_path:
            self.upx_path.setText(dir_path)
    
    def show_help(self):
        """
        Show help dialog for Advanced tab.
        
        Displays a message box with detailed explanations of:
        - Log level options and their purposes
        - UPX utility and how to obtain it
        - Debug mode options for troubleshooting
        - Clean cache usage for build issue resolution
        """
        help_text = """
        <h3>Advanced Settings Help</h3>
        
        <b>Log Level:</b><br>
        Controls how much detail PyInstaller shows during the build process.<br>
        - TRACE: Most detailed (for debugging)<br>
        - DEBUG: Detailed information<br>
        - INFO: Normal output (default)<br>
        - WARN: Warnings only<br>
        - ERROR: Errors only<br>
        - FATAL: Critical errors only<br><br>
        
        <b>UPX Directory:</b><br>
        Path to UPX (Ultimate Packer for eXecutables).<br>
        UPX compresses your executable to reduce file size.<br>
        Download UPX from: https://upx.github.io/<br><br>
        
        <b>Debug Mode:</b><br>
        Helps diagnose issues with your frozen application:<br>
        - imports: Shows module initialization messages<br>
        - bootloader: Shows bootloader progress<br>
        - all: Enables all debug options<br>
        - noarchive: Stores files separately (easier to debug)<br><br>
        
        <b>Clean Cache:</b><br>
        Clears PyInstaller's cache before building.<br>
        Use this if you encounter strange build errors.
        """
        
        QMessageBox.information(self, "Advanced Settings Help", help_text)