"""Imports, hooks, and data-collection configuration tab."""

from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox,
    QFileDialog, QGroupBox, QVBoxLayout, QFormLayout
)
from PyQt6.QtCore import pyqtSignal

from .base_tab import BaseTab


def _split_list(text: str) -> list:
    """
    Split a comma-separated field into a clean list of non-empty items.
    
    Args:
        text: Raw comma-separated text from a QLineEdit.
    
    Returns:
        List of trimmed, non-empty strings.
    """
    if not text:
        return []
    return [item.strip() for item in text.split(",") if item.strip()]


class ImportsTab(BaseTab):
    """
    Tab for fine-tuning what PyInstaller discovers and bundles.
    
    Covers the "What to bundle, where to search" section of PyInstaller's
    own CLI: extra import search paths, module exclusion, the various
    ``--collect-*`` helpers for packages that PyInstaller's static analysis
    misses (a very common source of "ModuleNotFoundError" at runtime),
    package metadata copying, custom hook directories/runtime hooks, and
    an optional startup splash screen image.
    """
    
    search_paths_changed = pyqtSignal(str)
    exclude_modules_changed = pyqtSignal(str)
    collect_all_changed = pyqtSignal(str)
    collect_submodules_changed = pyqtSignal(str)
    collect_data_changed = pyqtSignal(str)
    collect_binaries_changed = pyqtSignal(str)
    copy_metadata_changed = pyqtSignal(str)
    recursive_copy_metadata_changed = pyqtSignal(str)
    additional_hooks_dir_changed = pyqtSignal(str)
    runtime_hooks_changed = pyqtSignal(str)
    splash_image_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        """
        Initialize the Imports & Hooks tab.
        
        Args:
            parent: Parent widget (default: None).
        """
        super().__init__(parent)
        self.init_ui()
    
    def _help_header(self, title: str, tooltip: str, slot) -> QWidget:
        """
        Build the standard "title + (?) help button" header row used by
        every tab in the application.
        
        Args:
            title: The header label text.
            tooltip: Tooltip text for the help button.
            slot: Callable to invoke when the help button is clicked.
        
        Returns:
            A QWidget containing the assembled header row.
        """
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 5)
        
        header_label = QLabel(title)
        header_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        
        help_button = QPushButton("?")
        help_button.setFixedSize(24, 24)
        help_button.setToolTip(tooltip)
        help_button.setStyleSheet("""
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
        help_button.clicked.connect(slot)
        
        header_layout.addWidget(header_label)
        header_layout.addStretch()
        header_layout.addWidget(help_button)
        return header_widget
    
    def init_ui(self):
        """
        Initialize the user interface.
        
        Builds three group boxes: import discovery (paths/excludes),
        data collection helpers (collect-*/metadata), and hooks/splash.
        """
        self.main_layout.addWidget(
            self._help_header("Imports & Hooks", "Show help for Imports & Hooks settings", self.show_help)
        )
        
        # --- Import discovery ---
        discovery_group = QGroupBox("Import Discovery")
        discovery_form = QFormLayout()
        
        self.search_paths_input = QLineEdit()
        self.search_paths_input.setPlaceholderText("Comma-separated extra import search paths (like PYTHONPATH)")
        self.search_paths_input.setToolTip("Equivalent to -p/--paths. Example: ./libs, ../shared")
        discovery_form.addRow("Search Paths:", self.search_paths_input)
        
        self.exclude_modules_input = QLineEdit()
        self.exclude_modules_input.setPlaceholderText("Comma-separated modules to exclude from the build")
        self.exclude_modules_input.setToolTip("Equivalent to --exclude-module. Example: tkinter, unittest")
        discovery_form.addRow("Exclude Modules:", self.exclude_modules_input)
        
        discovery_group.setLayout(discovery_form)
        self.main_layout.addWidget(discovery_group)
        
        # --- Data collection helpers ---
        collect_group = QGroupBox("Package Data Collection")
        collect_form = QFormLayout()
        
        self.collect_all_input = QLineEdit()
        self.collect_all_input.setPlaceholderText("Comma-separated packages")
        self.collect_all_input.setToolTip(
            "Equivalent to --collect-all. Collects all submodules, data files,\n"
            "and binaries for the given package(s). Use this first if a package\n"
            "misbehaves at runtime - it's the broadest, safest fix."
        )
        collect_form.addRow("Collect All:", self.collect_all_input)
        
        self.collect_submodules_input = QLineEdit()
        self.collect_submodules_input.setPlaceholderText("Comma-separated packages")
        self.collect_submodules_input.setToolTip("Equivalent to --collect-submodules.")
        collect_form.addRow("Collect Submodules:", self.collect_submodules_input)
        
        self.collect_data_input = QLineEdit()
        self.collect_data_input.setPlaceholderText("Comma-separated packages")
        self.collect_data_input.setToolTip("Equivalent to --collect-data.")
        collect_form.addRow("Collect Data:", self.collect_data_input)
        
        self.collect_binaries_input = QLineEdit()
        self.collect_binaries_input.setPlaceholderText("Comma-separated packages")
        self.collect_binaries_input.setToolTip("Equivalent to --collect-binaries.")
        collect_form.addRow("Collect Binaries:", self.collect_binaries_input)
        
        self.copy_metadata_input = QLineEdit()
        self.copy_metadata_input.setPlaceholderText("Comma-separated packages")
        self.copy_metadata_input.setToolTip(
            "Equivalent to --copy-metadata.\n"
            "Needed for packages that check importlib.metadata at runtime."
        )
        collect_form.addRow("Copy Metadata:", self.copy_metadata_input)
        
        self.recursive_copy_metadata_input = QLineEdit()
        self.recursive_copy_metadata_input.setPlaceholderText("Comma-separated packages")
        self.recursive_copy_metadata_input.setToolTip(
            "Equivalent to --recursive-copy-metadata.\n"
            "Same as Copy Metadata, but also for all of the package's dependencies."
        )
        collect_form.addRow("Recursive Copy Metadata:", self.recursive_copy_metadata_input)
        
        collect_group.setLayout(collect_form)
        self.main_layout.addWidget(collect_group)
        
        # --- Hooks & splash ---
        hooks_group = QGroupBox("Hooks && Splash Screen")
        hooks_layout = QVBoxLayout()
        
        self.hooks_dir_label = QLabel("Additional Hooks Directory:")
        self.hooks_dir_input = QLineEdit()
        self.hooks_dir_input.setPlaceholderText("Extra folder PyInstaller should search for hook files")
        self.hooks_dir_input.setToolTip("Equivalent to --additional-hooks-dir")
        self.hooks_dir_button = QPushButton("Browse")
        hooks_dir_row = QHBoxLayout()
        hooks_dir_row.addWidget(self.hooks_dir_input)
        hooks_dir_row.addWidget(self.hooks_dir_button)
        
        self.runtime_hooks_label = QLabel("Runtime Hook Scripts:")
        self.runtime_hooks_input = QLineEdit()
        self.runtime_hooks_input.setPlaceholderText("Comma-separated paths to runtime hook .py scripts")
        self.runtime_hooks_input.setToolTip("Equivalent to --runtime-hook (used once per script).")
        
        self.splash_label = QLabel("Splash Screen Image:")
        self.splash_input = QLineEdit()
        self.splash_input.setPlaceholderText("Image shown while a onefile build is unpacking (experimental)")
        self.splash_input.setToolTip("Equivalent to --splash. PyInstaller notes this feature as experimental.")
        self.splash_button = QPushButton("Browse")
        splash_row = QHBoxLayout()
        splash_row.addWidget(self.splash_input)
        splash_row.addWidget(self.splash_button)
        
        hooks_layout.addWidget(self.hooks_dir_label)
        hooks_layout.addLayout(hooks_dir_row)
        hooks_layout.addWidget(self.runtime_hooks_label)
        hooks_layout.addWidget(self.runtime_hooks_input)
        hooks_layout.addWidget(self.splash_label)
        hooks_layout.addLayout(splash_row)
        
        hooks_group.setLayout(hooks_layout)
        self.main_layout.addWidget(hooks_group)
        
        self.main_layout.addStretch()
        
        # Connect signals
        self.search_paths_input.textChanged.connect(self.search_paths_changed.emit)
        self.exclude_modules_input.textChanged.connect(self.exclude_modules_changed.emit)
        self.collect_all_input.textChanged.connect(self.collect_all_changed.emit)
        self.collect_submodules_input.textChanged.connect(self.collect_submodules_changed.emit)
        self.collect_data_input.textChanged.connect(self.collect_data_changed.emit)
        self.collect_binaries_input.textChanged.connect(self.collect_binaries_changed.emit)
        self.copy_metadata_input.textChanged.connect(self.copy_metadata_changed.emit)
        self.recursive_copy_metadata_input.textChanged.connect(self.recursive_copy_metadata_changed.emit)
        self.hooks_dir_input.textChanged.connect(self.additional_hooks_dir_changed.emit)
        self.hooks_dir_button.clicked.connect(self.browse_hooks_dir)
        self.runtime_hooks_input.textChanged.connect(self.runtime_hooks_changed.emit)
        self.splash_input.textChanged.connect(self.splash_image_changed.emit)
        self.splash_button.clicked.connect(self.browse_splash_image)
    
    def browse_hooks_dir(self):
        """Open a directory dialog to select the additional hooks folder."""
        dir_path = QFileDialog.getExistingDirectory(self, "Select Hooks Directory")
        if dir_path:
            self.hooks_dir_input.setText(dir_path)
    
    def browse_splash_image(self):
        """Open a file dialog to select the splash screen image."""
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Splash Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif);;All Files (*)"
        )
        if file_name:
            self.splash_input.setText(file_name)
    
    @staticmethod
    def parse_list(text: str) -> list:
        """
        Parse a comma-separated QLineEdit value into a list.
        
        Args:
            text: Raw field text.
        
        Returns:
            List of trimmed, non-empty strings.
        """
        return _split_list(text)
    
    def show_help(self):
        """Show help dialog for the Imports & Hooks tab."""
        help_text = """
        <h3>Imports & Hooks Help</h3>
        
        <b>Search Paths:</b><br>
        Extra directories PyInstaller should search when resolving imports,
        similar to setting PYTHONPATH.<br><br>
        
        <b>Exclude Modules:</b><br>
        Modules or packages to leave out of the build entirely (as if they
        were not installed). Useful for trimming size or working around
        modules that don't play well with freezing.<br><br>
        
        <b>Collect All / Submodules / Data / Binaries:</b><br>
        PyInstaller's static analysis can miss plugins, data files, or
        binaries a package loads dynamically. These options force PyInstaller
        to grab everything it can find for the named package(s).
        <b>Collect All</b> is the broadest and usually the first thing to try
        when a frozen app works differently than running it from source.<br><br>
        
        <b>Copy Metadata / Recursive Copy Metadata:</b><br>
        Some packages call <code>importlib.metadata</code> at runtime to
        check their own version or entry points; if that metadata isn't
        bundled you'll see a <code>PackageNotFoundError</code>. These options
        copy that metadata into the build.<br><br>
        
        <b>Additional Hooks Directory:</b><br>
        A folder containing custom PyInstaller hook files
        (<code>hook-&lt;module&gt;.py</code>) for packages that need special handling.<br><br>
        
        <b>Runtime Hook Scripts:</b><br>
        Plain Python scripts bundled with the app and executed before your
        own code runs, useful for environment setup at startup.<br><br>
        
        <b>Splash Screen Image:</b><br>
        Shows an image while a onefile build extracts itself on startup.
        PyInstaller marks this feature as experimental.
        """
        QMessageBox.information(self, "Imports & Hooks Help", help_text)
