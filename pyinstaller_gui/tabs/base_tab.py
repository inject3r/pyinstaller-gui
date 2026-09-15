"""Base tab widget for all tabs."""

from PyQt6.QtWidgets import QWidget, QVBoxLayout


class BaseTab(QWidget):
    """
    Base class for all tab widgets.
    
    This class provides a common foundation for all tab widgets in the
    application. It sets up a standard vertical layout with consistent
    spacing and margins that can be inherited by all specific tab
    implementations.
    
    Subclasses should override the init_ui() method to add their specific
    UI components to the main_layout.
    """
    
    def __init__(self, parent=None):
        """
        Initialize the base tab widget.
        
        Args:
            parent: Parent widget (default: None).
        """
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(10)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
    
    def init_ui(self):
        """
        Initialize the user interface.
        
        This method should be overridden by subclasses to add their
        specific UI components to the main_layout. The base implementation
        does nothing.
        """
        pass