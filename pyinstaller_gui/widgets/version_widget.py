"""Version display widget."""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel


class VersionWidget(QWidget):
    """
    Widget for displaying Python and PyInstaller versions.
    
    This widget shows the currently installed versions of Python and
    PyInstaller in the main window footer for quick reference.
    """
    
    def __init__(self, parent=None):
        """
        Initialize the version display widget.
        
        Args:
            parent: Parent widget (default: None).
        """
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """
        Initialize the user interface.
        
        Creates and arranges the labels for Python and PyInstaller versions
        in a vertical layout with minimal spacing.
        """
        layout = QVBoxLayout(self)
        layout.setSpacing(2)
        
        self.python_version_label = QLabel("Python Version: --")
        self.pyinstaller_version_label = QLabel("PyInstaller Version: --")
        
        layout.addWidget(self.python_version_label)
        layout.addWidget(self.pyinstaller_version_label)
    
    def set_python_version(self, version: str):
        """
        Set the Python version text.
        
        Args:
            version: Python version string (e.g., "Python 3.10.0").
        """
        self.python_version_label.setText(version)
    
    def set_pyinstaller_version(self, version: str):
        """
        Set the PyInstaller version text.
        
        Args:
            version: PyInstaller version string (e.g., "PyInstaller Version: 6.0.0").
        """
        self.pyinstaller_version_label.setText(version)