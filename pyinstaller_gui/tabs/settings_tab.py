"""Settings configuration tab."""

from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, 
    QFileDialog, QMessageBox
)
from PyQt6.QtCore import pyqtSignal

from .base_tab import BaseTab


class SettingsTab(BaseTab):
    """
    Tab for general settings configuration.
    
    This tab allows users to configure output-related settings including:
    - Output folder location for the built executable
    - Custom icon file for the executable
    - Runtime temporary directory for onefile mode extraction
    - Additional custom PyInstaller command-line arguments
    """
    
    output_folder_changed = pyqtSignal(str)
    custom_commands_changed = pyqtSignal(str)
    icon_path_changed = pyqtSignal(str)
    tmpdir_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        """
        Initialize the settings tab.
        
        Args:
            parent: Parent widget (default: None).
        """
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """
        Initialize the user interface.
        
        Creates the header with help button, then arranges the output folder
        selection, icon file selection, runtime temporary directory input,
        and custom commands input in a vertical layout.
        """
        # Help button in header
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 5)
        
        header_label = QLabel("Output Settings")
        header_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        
        self.settings_help_button = QPushButton("?")
        self.settings_help_button.setFixedSize(24, 24)
        self.settings_help_button.setToolTip("Show help for Output settings")
        self.settings_help_button.setStyleSheet("""
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
        header_layout.addWidget(self.settings_help_button)
        
        self.main_layout.addWidget(header_widget)
        
        # Output folder
        self.output_folder_label = QLabel("Select Output Folder:")
        self.output_folder_label.setToolTip("Where the built executable will be saved")
        
        self.output_folder_path = QLineEdit()
        self.output_folder_path.setPlaceholderText("Setting the program output location")
        self.output_folder_path.setToolTip("Default: ./dist folder in the current directory")
        
        self.output_folder_button = QPushButton("Browse Output Folder")
        self.output_folder_button.setToolTip("Select directory for the output executable")
        
        folder_layout = QHBoxLayout()
        folder_layout.addWidget(self.output_folder_path)
        folder_layout.addWidget(self.output_folder_button)
        
        # Icon
        self.icon_label = QLabel("Icon File:")
        self.icon_label.setToolTip("Custom icon for your executable file")
        
        self.icon_path = QLineEdit()
        self.icon_path.setPlaceholderText("Icon File (.ico for Windows, .icns for Mac)")
        self.icon_path.setToolTip(
            "Windows: .ico file\n"
            "macOS: .icns file\n"
            "Leave empty for default PyInstaller icon"
        )
        
        self.browse_icon_button = QPushButton("Browse Icon")
        self.browse_icon_button.setToolTip("Select icon file")
        
        icon_layout = QHBoxLayout()
        icon_layout.addWidget(self.icon_path)
        icon_layout.addWidget(self.browse_icon_button)
        
        # Temporary directory
        self.tmpdir_label = QLabel("Runtime Tmpdir:")
        self.tmpdir_label.setToolTip("Custom temporary directory for onefile mode")
        
        self.tmpdir_input = QLineEdit()
        self.tmpdir_input.setPlaceholderText("Specify a temp directory to boost performance")
        self.tmpdir_input.setToolTip(
            "For onefile mode, files are extracted to this directory.\n"
            "Use a RAM disk for faster performance."
        )
        
        # Custom commands
        self.custom_commands_label = QLabel("Custom Commands:")
        self.custom_commands_label.setToolTip("Additional PyInstaller arguments")
        
        self.custom_commands = QLineEdit()
        self.custom_commands.setPlaceholderText("Enter additional commands here")
        self.custom_commands.setToolTip(
            "Example: --optimize 2 --noupx\n"
            "Add any PyInstaller option not covered by the GUI"
        )
        
        # Add to layout
        self.main_layout.addWidget(self.output_folder_label)
        self.main_layout.addLayout(folder_layout)
        self.main_layout.addWidget(self.icon_label)
        self.main_layout.addLayout(icon_layout)
        self.main_layout.addWidget(self.tmpdir_label)
        self.main_layout.addWidget(self.tmpdir_input)
        self.main_layout.addWidget(self.custom_commands_label)
        self.main_layout.addWidget(self.custom_commands)
        self.main_layout.addStretch()
        
        # Connect signals
        self.output_folder_button.clicked.connect(self.browse_output_folder)
        self.output_folder_path.textChanged.connect(self.output_folder_changed.emit)
        self.browse_icon_button.clicked.connect(self.browse_icon)
        self.icon_path.textChanged.connect(self.icon_path_changed.emit)
        self.tmpdir_input.textChanged.connect(self.tmpdir_changed.emit)
        self.custom_commands.textChanged.connect(self.custom_commands_changed.emit)
        self.settings_help_button.clicked.connect(self.show_help)
    
    def browse_output_folder(self):
        """
        Open directory dialog to select output folder.
        
        Updates the output folder path field with the selected directory.
        """
        folder_name = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder_name:
            self.output_folder_path.setText(folder_name)
    
    def browse_icon(self):
        """
        Open file dialog to select icon file.
        
        Filters for .ico (Windows) and .icns (macOS) icon files.
        Updates the icon path field with the selected file.
        """
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Icon", "", "Icon Files (*.ico *.icns)"
        )
        if file_name:
            self.icon_path.setText(file_name)
    
    def show_help(self):
        """
        Show help dialog for Settings tab.
        
        Displays a message box with detailed explanations of each setting:
        - Output folder location
        - Icon file format requirements by platform
        - Runtime tmpdir usage and performance tips
        - Custom commands examples
        """
        help_text = """
        <h3>Output Settings Help</h3>
        
        <b>Output Folder:</b><br>
        Directory where the built executable will be saved.<br>
        Default is the 'dist' folder in the current directory.<br><br>
        
        <b>Icon File:</b><br>
        Custom icon for your executable.<br>
        - Windows: Use .ico files<br>
        - macOS: Use .icns files<br>
        - Linux: Icon support varies by desktop environment<br><br>
        
        <b>Runtime Tmpdir:</b><br>
        For onefile mode, the bootloader extracts files to this directory.<br>
        Using a RAM disk (e.g., /dev/shm on Linux) can improve performance.<br><br>
        
        <b>Custom Commands:</b><br>
        Add any PyInstaller option not covered by the GUI.<br>
        Example: --optimize 2 --noupx --noconfirm
        """
        
        QMessageBox.information(self, "Output Settings Help", help_text)