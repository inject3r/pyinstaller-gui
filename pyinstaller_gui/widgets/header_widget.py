"""Header widget for the main window."""

import os

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, pyqtSignal, QSize

from ..__version__ import __version__


class HeaderWidget(QWidget):
    """
    Header widget with title, version, and buttons.
    
    This widget appears at the top of the main window and contains:
    - The application title "PyInstaller GUI" with styled text
    - The current version number in a centered container
    - Theme toggle button for switching between light/dark/system themes
    - GitHub button for accessing the project repository
    """
    
    theme_toggled = pyqtSignal()
    github_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        """
        Initialize the header widget.
        
        Args:
            parent: Parent widget (default: None).
        """
        super().__init__(parent)
        self.setObjectName("HeaderWidget")
        self.init_ui()
    
    def init_ui(self):
        """
        Initialize the user interface.
        
        Creates three main sections:
        - Left section: Application title with "PyInstaller" and "GUI" parts
        - Center section: Version number in a rounded container
        - Right section: Theme toggle and GitHub buttons
        """
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 12, 20, 12)
        layout.setSpacing(15)
        
        # Left section - Title
        left_widget = QWidget()
        left_layout = QHBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(8)
        
        self.gui_label = QLabel("PyInstaller")
        self.gui_label.setContentsMargins(0, 0, -8, 0)
        self.gui_label.setStyleSheet("""
            font-size: 18px;
            font-weight: normal;
            color: #2c3e50;
            padding: 4px 0px;
        """)
        left_layout.addWidget(self.gui_label)
        
        self.pyinstaller_label = QLabel("GUI")
        self.pyinstaller_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            background: #2D8FBA;
            color: white;
            padding: 4px 0px;
            border-radius: 4px;
        """)
        left_layout.addWidget(self.pyinstaller_label)
        
        layout.addWidget(left_widget)
        
        # Center section - Version
        center_widget = QWidget()
        center_layout = QHBoxLayout(center_widget)
        center_layout.setContentsMargins(0, 0, 0, 0)
        
        version_container = QWidget()
        version_container.setObjectName("VersionContainer")
        version_container.setStyleSheet("""
            QWidget#VersionContainer {
                background-color: rgba(100, 100, 100, 0.1);
                border-radius: 12px;
                padding: 4px 12px;
            }
        """)
        version_layout = QHBoxLayout(version_container)
        version_layout.setContentsMargins(8, 4, 8, 4)
        
        self.version_label = QLabel(f"Version {__version__}")
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.version_label.setStyleSheet("background: transparent;")
        version_layout.addWidget(self.version_label)
        
        center_layout.addStretch()
        center_layout.addWidget(version_container)
        center_layout.addStretch()
        
        layout.addWidget(center_widget, stretch=1)
        
        # Right section - Buttons
        right_widget = QWidget()
        right_layout = QHBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(12)
        
        self.theme_toggle = QPushButton()
        self.theme_toggle.setFixedSize(28, 28)
        self.theme_toggle.setIconSize(QSize(16, 16))
        self.theme_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.theme_toggle.setObjectName("ThemeToggle")
        self.theme_toggle.setToolTip("Toggle theme (System/Light/Dark)")
        self.theme_toggle.setStyleSheet("""
            QPushButton#ThemeToggle {
                border-radius: 14px;
                background-color: rgba(0, 0, 0, 0.05);
            }
            QPushButton#ThemeToggle:hover {
                background-color: rgba(0, 0, 0, 0.1);
            }
        """)
        self.theme_toggle.clicked.connect(self.theme_toggled.emit)
        right_layout.addWidget(self.theme_toggle)
        
        self.github_button = QPushButton(" GitHub")
        self.github_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.github_button.setObjectName("GitHubButton")
        self.github_button.setIconSize(QSize(16, 16))
        self.github_button.setFixedHeight(32)
        self.github_button.setToolTip("Visit our GitHub repository")
        self.github_button.setStyleSheet("""
            QPushButton#GitHubButton {
                padding: 5px 12px;
                border-radius: 6px;
                background-color: #24292e;
                color: white;
                font-weight: 500;
            }
            QPushButton#GitHubButton:hover {
                background-color: #2c3136;
            }
        """)
        
        # Load GitHub icon from file
        github_icon = self._load_github_icon()
        if github_icon:
            self.github_button.setIcon(github_icon)
        
        self.github_button.clicked.connect(self.github_clicked.emit)
        right_layout.addWidget(self.github_button)
        
        layout.addWidget(right_widget)
        
        self.setStyleSheet("""
            QWidget#HeaderWidget {
                border-bottom: 1px solid rgba(0, 0, 0, 0.1);
                background-color: rgba(0, 0, 0, 0.02);
                border-radius: 10px;
            }
        """)
    
    def _load_github_icon(self) -> QIcon:
        """
        Load the GitHub icon from the icons directory.
        
        Returns:
            QIcon object if the icon file exists, otherwise an empty QIcon.
        """
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_path, "icons", "github.svg")
        
        if os.path.exists(icon_path):
            return QIcon(icon_path)
        return QIcon()
    
    def set_theme_icon(self, icon: QIcon):
        """
        Set the theme toggle button icon.
        
        Args:
            icon: The QIcon to display on the theme toggle button.
                  Changes based on current theme (dark, light, or system).
        """
        self.theme_toggle.setIcon(icon)