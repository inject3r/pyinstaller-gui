"""Advanced configuration tab."""

from PyQt6.QtWidgets import (
    QWidget, QLabel, QComboBox, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, 
    QCheckBox, QFileDialog, QMessageBox, QGroupBox, QFormLayout
)
from PyQt6.QtCore import pyqtSignal

from .base_tab import BaseTab


class AdvancedTab(BaseTab):
    """
    Tab for advanced PyInstaller configuration.
    
    This tab provides advanced build options including:
    - Log level control for build output verbosity
    - UPX compression: enable/disable, custom directory, and per-file excludes
    - Debug mode options for troubleshooting
    - Bytecode optimization level and extra interpreter options
    - Clean cache / no-confirm and other build-behavior toggles
    """
    
    log_level_changed = pyqtSignal(str)
    upx_dir_changed = pyqtSignal(str)
    debug_mode_changed = pyqtSignal(str)
    clean_changed = pyqtSignal(bool)
    noupx_changed = pyqtSignal(bool)
    upx_exclude_changed = pyqtSignal(str)
    optimize_level_changed = pyqtSignal(str)
    strip_changed = pyqtSignal(bool)
    python_options_changed = pyqtSignal(str)
    noconfirm_changed = pyqtSignal(bool)
    contents_directory_changed = pyqtSignal(str)
    bootloader_ignore_signals_changed = pyqtSignal(bool)
    
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
        
        Creates the header with help button, then arranges build-output
        controls (log level, debug mode, clean/no-confirm), a UPX
        compression group, and a bytecode/runtime options group.
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
        
        self.main_layout.addWidget(self.log_level_label)
        self.main_layout.addWidget(self.log_level_combo)
        self.main_layout.addWidget(self.debug_label)
        self.main_layout.addWidget(self.debug_combo)
        
        # --- UPX compression ---
        upx_group = QGroupBox("UPX Compression")
        upx_layout = QVBoxLayout()
        
        self.cmd_noupx = QCheckBox("Disable UPX (--noupx)")
        self.cmd_noupx.setToolTip(
            "Do not use UPX even if it is available.\n"
            "When enabled, the UPX directory below is ignored."
        )
        upx_layout.addWidget(self.cmd_noupx)
        
        self.upx_label = QLabel("UPX Directory:")
        self.upx_label.setToolTip("Path to UPX utility for compressing binaries")
        
        self.upx_path = QLineEdit()
        self.upx_path.setPlaceholderText("Set the UPX path to compress binary files")
        self.upx_path.setToolTip("UPX (Ultimate Packer for eXecutables) reduces file size")
        
        self.upx_button = QPushButton("Browse")
        self.upx_button.setToolTip("Browse for UPX installation directory")
        
        upx_dir_row = QHBoxLayout()
        upx_dir_row.addWidget(self.upx_path)
        upx_dir_row.addWidget(self.upx_button)
        upx_layout.addWidget(self.upx_label)
        upx_layout.addLayout(upx_dir_row)
        
        self.upx_exclude_label = QLabel("UPX Exclude (filenames):")
        self.upx_exclude_input = QLineEdit()
        self.upx_exclude_input.setPlaceholderText("Comma-separated binary filenames to skip during UPX compression")
        self.upx_exclude_input.setToolTip(
            "Equivalent to --upx-exclude. Use this if UPX corrupts a\n"
            "specific binary during compression, e.g.: vcruntime140.dll"
        )
        upx_layout.addWidget(self.upx_exclude_label)
        upx_layout.addWidget(self.upx_exclude_input)
        
        upx_group.setLayout(upx_layout)
        self.main_layout.addWidget(upx_group)
        
        # --- Bytecode / runtime options ---
        runtime_group = QGroupBox("Bytecode && Runtime Options")
        runtime_form = QFormLayout()
        
        self.optimize_combo = QComboBox()
        self.optimize_combo.addItems(["(default)", "0", "1", "2"])
        self.optimize_combo.setToolTip(
            "Equivalent to --optimize. Bytecode optimization level for\n"
            "collected modules, similar to Python's own -O/-OO flags."
        )
        runtime_form.addRow("Optimize Level:", self.optimize_combo)
        
        self.cmd_strip = QCheckBox("Strip symbols (--strip)")
        self.cmd_strip.setToolTip(
            "Apply a symbol-table strip to the executable and shared libs.\n"
            "Not recommended on Windows."
        )
        runtime_form.addRow("", self.cmd_strip)
        
        self.python_options_input = QLineEdit()
        self.python_options_input.setPlaceholderText("Comma-separated, e.g.: v, W default, X no_debug_ranges")
        self.python_options_input.setToolTip(
            "Equivalent to --python-option (used once per entry).\n"
            "Supported values: v, u, W <control>, X <xoption>, hash_seed=<value>"
        )
        runtime_form.addRow("Python Options:", self.python_options_input)
        
        runtime_group.setLayout(runtime_form)
        self.main_layout.addWidget(runtime_group)
        
        # --- Build behavior ---
        behavior_group = QGroupBox("Build Behavior")
        behavior_layout = QVBoxLayout()
        
        self.cmd_clean = QCheckBox("--clean (Clear PyInstaller cache and temp files before building.)")
        self.cmd_clean.setToolTip(
            "Cleans the PyInstaller cache and removes temporary files\n"
            "Use this if you encounter build issues"
        )
        behavior_layout.addWidget(self.cmd_clean)
        
        self.cmd_noconfirm = QCheckBox("--noconfirm (Replace output directory without asking)")
        self.cmd_noconfirm.setToolTip("Skips the confirmation prompt when the dist folder already exists.")
        behavior_layout.addWidget(self.cmd_noconfirm)
        
        self.cmd_bootloader_ignore_signals = QCheckBox("--bootloader-ignore-signals")
        self.cmd_bootloader_ignore_signals.setToolTip(
            "Tell the bootloader to ignore signals rather than forwarding them\n"
            "to the child process. Rarely needed - see PyInstaller docs."
        )
        behavior_layout.addWidget(self.cmd_bootloader_ignore_signals)
        
        contents_row = QHBoxLayout()
        self.contents_dir_label = QLabel("Contents Directory (onedir):")
        self.contents_dir_input = QLineEdit()
        self.contents_dir_input.setPlaceholderText('Default is "_internal". Use "." for the legacy flat layout')
        self.contents_dir_input.setToolTip("Equivalent to --contents-directory (onedir builds only).")
        contents_row.addWidget(self.contents_dir_input)
        behavior_layout.addWidget(self.contents_dir_label)
        behavior_layout.addLayout(contents_row)
        
        behavior_group.setLayout(behavior_layout)
        self.main_layout.addWidget(behavior_group)
        
        self.main_layout.addStretch()
        
        # Connect signals
        self.log_level_combo.currentTextChanged.connect(self.log_level_changed.emit)
        self.upx_button.clicked.connect(self.select_upx_dir)
        self.upx_path.textChanged.connect(self.upx_dir_changed.emit)
        self.cmd_noupx.toggled.connect(self._on_noupx_toggled)
        self.upx_exclude_input.textChanged.connect(self.upx_exclude_changed.emit)
        self.debug_combo.currentTextChanged.connect(self.debug_mode_changed.emit)
        self.optimize_combo.currentTextChanged.connect(self._on_optimize_changed)
        self.cmd_strip.toggled.connect(self.strip_changed.emit)
        self.python_options_input.textChanged.connect(self.python_options_changed.emit)
        self.cmd_clean.toggled.connect(self.clean_changed.emit)
        self.cmd_noconfirm.toggled.connect(self.noconfirm_changed.emit)
        self.cmd_bootloader_ignore_signals.toggled.connect(self.bootloader_ignore_signals_changed.emit)
        self.contents_dir_input.textChanged.connect(self.contents_directory_changed.emit)
        self.advanced_help_button.clicked.connect(self.show_help)
    
    def _on_noupx_toggled(self, checked: bool):
        """
        Handle the "Disable UPX" checkbox.
        
        Greys out the UPX directory controls (they would be ignored anyway
        once UPX is disabled) and forwards the new state.
        
        Args:
            checked: True if UPX compression should be disabled.
        """
        self.upx_path.setEnabled(not checked)
        self.upx_button.setEnabled(not checked)
        self.noupx_changed.emit(checked)
    
    def _on_optimize_changed(self, text: str):
        """
        Forward the selected optimize level, translating the placeholder.
        
        Args:
            text: The combo box text ("(default)", "0", "1", or "2").
        """
        self.optimize_level_changed.emit("" if text == "(default)" else text)
    
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
        
        Displays a message box with detailed explanations of every option
        in this tab, including the newer UPX, optimization, and
        build-behavior controls.
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
        
        <b>Debug Mode:</b><br>
        Helps diagnose issues with your frozen application:<br>
        - imports: Shows module initialization messages<br>
        - bootloader: Shows bootloader progress<br>
        - all: Enables all debug options<br>
        - noarchive: Stores files separately (easier to debug)<br><br>
        
        <b>UPX Compression:</b><br>
        UPX (Ultimate Packer for eXecutables) can shrink the final
        executable. Disable it entirely with the checkbox, or point at a
        custom UPX install directory. Use UPX Exclude to skip specific
        binaries that don't compress cleanly.
        Download UPX from: https://upx.github.io/<br><br>
        
        <b>Optimize Level / Python Options:</b><br>
        Optimize Level maps to Python's own bytecode optimization
        (like -O/-OO). Python Options passes extra flags straight to the
        embedded interpreter at runtime (e.g. "W default" to show warnings).<br><br>
        
        <b>Strip Symbols:</b><br>
        Removes debug symbol tables to reduce size. Not recommended on
        Windows executables.<br><br>
        
        <b>Clean Cache / No Confirm:</b><br>
        Clean clears PyInstaller's cache before building - useful after
        strange build errors. No Confirm skips the "overwrite dist folder?"
        prompt, handy for unattended/CI builds.<br><br>
        
        <b>Contents Directory:</b><br>
        For onedir builds, controls the name of the folder holding all
        supporting files next to the executable. Use "." to restore
        PyInstaller's legacy flat onedir layout.
        """
        
        QMessageBox.information(self, "Advanced Settings Help", help_text)
