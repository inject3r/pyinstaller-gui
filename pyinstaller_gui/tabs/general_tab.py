"""General configuration tab."""

from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QCheckBox, 
    QFileDialog, QMessageBox, QMenu
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QAction, QDragEnterEvent, QDropEvent


class CustomLineEdit(QLineEdit):
    """
    Custom QLineEdit that accepts drag and drop.
    
    This widget allows users to drag and drop files directly onto
    the script path field for easier script selection.
    """
    
    def __init__(self, parent=None):
        """
        Initialize the custom line edit with drag and drop support.
        
        Args:
            parent: Parent widget (default: None).
        """
        super().__init__(parent)
        self.setAcceptDrops(True)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """
        Handle drag enter event.
        
        Accepts the drag operation if the dragged data contains URLs
        (file paths).
        
        Args:
            event: The drag enter event.
        """
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
    
    def dropEvent(self, event: QDropEvent):
        """
        Handle drop event.
        
        Extracts the file path from the dropped URL and sets it as the
        text of the line edit if the file has a .py extension.
        
        Args:
            event: The drop event.
        """
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if files and files[0].lower().endswith('.py'):
            self.setText(files[0])
            event.accept()
        else:
            event.ignore()


class GeneralTab(QWidget):
    """
    Tab for general PyInstaller configuration.
    
    This tab allows users to configure the basic build settings:
    - Select Python script (with drag & drop support)
    - Recent files list for quick access
    - Application name
    - OneFile mode (-F)
    - No Console mode (-w) for GUI applications
    - Hidden imports for dynamic module loading
    """
    
    script_changed = pyqtSignal(str)
    app_name_changed = pyqtSignal(str)
    onefile_changed = pyqtSignal(bool)
    noconsole_changed = pyqtSignal(bool)
    hidden_imports_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        """
        Initialize the general tab.
        
        Args:
            parent: Parent widget (default: None).
        """
        super().__init__(parent)
        self.recent_files = []
        self.max_recent_files = 10
        self.init_ui()
        self.load_recent_files()
    
    def init_ui(self):
        """
        Initialize the user interface.
        
        Creates the header with help button, script selection area with
        browse and recent buttons, application name input, option checkboxes,
        and hidden imports input in a vertical layout.
        """
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Help button in header
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 5)
        
        header_label = QLabel("General Settings")
        header_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        
        self.general_help_button = QPushButton("?")
        self.general_help_button.setFixedSize(24, 24)
        self.general_help_button.setToolTip("Show help for General settings")
        self.general_help_button.setStyleSheet("""
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
        header_layout.addWidget(self.general_help_button)
        
        main_layout.addWidget(header_widget)
        
        # Script selection
        self.script_label = QLabel("Select script:")
        self.script_label.setToolTip("Path to the main Python script you want to convert to executable\n\nDrag & drop a .py file here")
        
        self.script_path = CustomLineEdit()
        self.script_path.setPlaceholderText("Enter script location or drag & drop a .py file...")
        self.script_path.setToolTip("Select the main Python file (e.g., main.py)\nYou can also drag & drop a .py file here")
        
        self.browse_button = QPushButton("Browse")
        self.browse_button.setToolTip("Open file browser to select Python script")
        
        self.recent_button = QPushButton("Recent")
        self.recent_button.setToolTip("Select from recently used scripts")
        self.recent_button.setEnabled(False)
        
        self.recent_menu = QMenu()
        self.recent_button.setMenu(self.recent_menu)
        
        file_layout = QHBoxLayout()
        file_layout.addWidget(self.script_path)
        file_layout.addWidget(self.browse_button)
        file_layout.addWidget(self.recent_button)
        
        # Info label for drag & drop
        drag_drop_info = QLabel("💡 Tip: You can drag & drop a .py file directly into the script field")
        drag_drop_info.setStyleSheet("color: #7A8089; font-size: 11px; margin-left: 5px;")
        drag_drop_info.setWordWrap(True)
        
        # Application name
        self.app_name_label = QLabel("Application name:")
        self.app_name_label.setToolTip("Name of the output executable file (without extension)")
        
        self.app_name_input = QLineEdit()
        self.app_name_input.setPlaceholderText("Application name (Default name of the first script)")
        self.app_name_input.setToolTip("If empty, uses the script filename as the application name")
        
        # Options
        self.onefile_checkbox = QCheckBox("OneFile (-F)")
        self.onefile_checkbox.setToolTip(
            "Create a single executable file instead of a folder with multiple files.\n"
            "One-file bundles are easier to distribute but take longer to start."
        )
        
        self.noconsole_checkbox = QCheckBox("No Console (-w)")
        self.noconsole_checkbox.setToolTip(
            "Do not provide a console window (Windows only).\n"
            "Use this for GUI applications to hide the terminal window."
        )
        
        # Hidden imports
        self.hidden_imports_label = QLabel("Hidden Imports:")
        self.hidden_imports_label.setToolTip("Modules that are imported dynamically in your code")
        
        self.hidden_imports = QLineEdit()
        self.hidden_imports.setPlaceholderText("Comma-separated list of hidden imports")
        self.hidden_imports.setToolTip(
            "Example: requests,json,datetime\n"
            "PyInstaller may not automatically detect these imports."
        )
        
        # Add to layout
        main_layout.addWidget(self.script_label)
        main_layout.addLayout(file_layout)
        main_layout.addWidget(drag_drop_info)
        main_layout.addWidget(self.app_name_label)
        main_layout.addWidget(self.app_name_input)
        main_layout.addWidget(self.onefile_checkbox)
        main_layout.addWidget(self.noconsole_checkbox)
        main_layout.addWidget(self.hidden_imports_label)
        main_layout.addWidget(self.hidden_imports)
        main_layout.addStretch()
        
        self.setLayout(main_layout)
        
        # Store main_layout as instance variable for base class compatibility
        self.main_layout = main_layout
        
        # Connect signals
        self.browse_button.clicked.connect(self.browse_script)
        self.script_path.textChanged.connect(self.on_script_path_changed)
        self.general_help_button.clicked.connect(self.show_help)
        self.script_path.textChanged.connect(self.script_changed.emit)
        self.app_name_input.textChanged.connect(self.app_name_changed.emit)
        self.onefile_checkbox.toggled.connect(self.onefile_changed.emit)
        self.noconsole_checkbox.toggled.connect(self.noconsole_changed.emit)
        self.hidden_imports.textChanged.connect(self.hidden_imports_changed.emit)
    
    def browse_script(self):
        """
        Open file dialog to select a Python script.
        
        Opens a file dialog filtered for .py files and updates the
        script path field with the selected file. Adds the selection
        to the recent files list.
        """
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Python Script", "", "Python Files (*.py)"
        )
        if file_name:
            self.script_path.setText(file_name)
            self.add_to_recent_files(file_name)
    
    def on_script_path_changed(self, path: str):
        """
        Handle script path change and update recent files.
        
        Args:
            path: The new script path.
        """
        if path and path.strip():
            self.add_to_recent_files(path)
    
    def add_to_recent_files(self, file_path: str):
        """
        Add a file to the recent files list.
        
        Maintains a list of up to max_recent_files (10) items, with
        the most recently used file at the beginning. Duplicates are
        removed before insertion.
        
        Args:
            file_path: The file path to add to recent files.
        """
        if not file_path or not file_path.strip():
            return
        
        # Remove if already exists
        if file_path in self.recent_files:
            self.recent_files.remove(file_path)
        
        # Add to beginning
        self.recent_files.insert(0, file_path)
        
        # Keep only max_recent_files
        self.recent_files = self.recent_files[:self.max_recent_files]
        
        # Save to config
        self.save_recent_files()
        
        # Update menu
        self.update_recent_menu()
    
    def load_recent_files(self):
        """
        Load recent files from config manager.
        
        Retrieves the list of recently used files from persistent storage.
        Initializes with an empty list if none exist.
        """
        try:
            from ..core.config_manager import ConfigManager
            config_manager = ConfigManager()
            self.recent_files = config_manager.get("recent_files", [])
            if not isinstance(self.recent_files, list):
                self.recent_files = []
            self.update_recent_menu()
        except Exception:
            self.recent_files = []
    
    def save_recent_files(self):
        """
        Save recent files to config manager.
        
        Persists the list of recently used files to storage for
        restoration on next application launch.
        """
        try:
            from ..core.config_manager import ConfigManager
            config_manager = ConfigManager()
            config_manager.set("recent_files", self.recent_files)
        except Exception:
            pass
    
    def update_recent_menu(self):
        """
        Update the recent files menu.
        
        Populates the menu with recent file entries. Shows "No recent files"
        message and disables the button if the list is empty. Adds a separator
        and a "Clear Recent Files" action when files are present.
        """
        self.recent_menu.clear()
        
        if not self.recent_files:
            no_recent_action = QAction("No recent files", self)
            no_recent_action.setEnabled(False)
            self.recent_menu.addAction(no_recent_action)
            self.recent_button.setEnabled(False)
        else:
            self.recent_button.setEnabled(True)
            for file_path in self.recent_files:
                action = QAction(file_path, self)
                action.setToolTip(file_path)
                action.triggered.connect(lambda checked, path=file_path: self.select_recent_file(path))
                self.recent_menu.addAction(action)
            
            self.recent_menu.addSeparator()
            clear_action = QAction("Clear Recent Files", self)
            clear_action.triggered.connect(self.clear_recent_files)
            self.recent_menu.addAction(clear_action)
    
    def select_recent_file(self, file_path: str):
        """
        Select a recent file.
        
        Validates that the file still exists before loading it.
        If the file is invalid, removes it from the recent files list
        and shows a warning message.
        
        Args:
            file_path: The path of the recent file to select.
        """
        if file_path and self.is_valid_script(file_path):
            self.script_path.setText(file_path)
            # Move to top of recent list
            self.add_to_recent_files(file_path)
        else:
            QMessageBox.warning(
                self, "File Not Found",
                f"The file no longer exists:\n{file_path}\n\nIt will be removed from recent files."
            )
            # Remove invalid file from recent list
            if file_path in self.recent_files:
                self.recent_files.remove(file_path)
                self.save_recent_files()
                self.update_recent_menu()
    
    def clear_recent_files(self):
        """
        Clear all recent files.
        
        Shows a confirmation dialog before clearing the entire
        recent files list.
        """
        reply = QMessageBox.question(
            self, "Clear Recent Files",
            "Are you sure you want to clear all recent files?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.recent_files = []
            self.save_recent_files()
            self.update_recent_menu()
            QMessageBox.information(self, "Cleared", "Recent files list has been cleared.")
    
    def is_valid_script(self, file_path: str) -> bool:
        """
        Check if a file is a valid Python script.
        
        Args:
            file_path: The path to check.
            
        Returns:
            True if the file exists and has a .py extension, False otherwise.
        """
        import os
        return os.path.isfile(file_path) and file_path.lower().endswith('.py')
    
    def show_help(self):
        """
        Show help dialog for General tab.
        
        Displays a message box with detailed explanations of:
        - Script selection with drag & drop tip
        - Recent files functionality
        - Application name usage
        - OneFile mode
        - No Console mode for GUI applications
        - Hidden imports for dynamic modules
        """
        help_text = """
        <h3>General Settings Help</h3>
        
        <b>Select script:</b><br>
        The main Python file you want to convert to an executable.<br>
        This file will be the entry point of your application.<br>
        <b>Tip:</b> You can drag & drop a .py file directly into the script field!<br><br>
        
        <b>Recent Files:</b><br>
        Shows a list of recently used Python scripts.<br>
        Click on any item to quickly load a previous script.<br>
        Use the menu to clear the list.<br><br>
        
        <b>Application name:</b><br>
        The name of the output executable file.<br>
        If left empty, the script filename will be used.<br><br>
        
        <b>OneFile (-F):</b><br>
        Creates a single executable file instead of a folder with multiple files.<br>
        One-file bundles are easier to distribute but take longer to start.<br><br>
        
        <b>No Console (-w):</b><br>
        Hides the console window (Windows only).<br>
        Use this for GUI applications like PyQt, Tkinter, etc.<br><br>
        
        <b>Hidden Imports:</b><br>
        Modules that are imported dynamically in your code.<br>
        PyInstaller may not detect these automatically.<br>
        Example: requests, json, datetime
        """
        
        QMessageBox.information(self, "General Settings Help", help_text)