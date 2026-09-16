"""Base tab widget for all tabs."""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea


class BaseTab(QWidget):
    """
    Base class for all tab widgets.
    
    This class provides a common foundation for all tab widgets in the
    application. Content is placed inside a scroll area so tabs with many
    options remain fully usable even in a smaller window, instead of
    clipping or squeezing widgets together.
    
    Subclasses should override the init_ui() method to add their specific
    UI components to self.main_layout (the layout of the scrollable inner
    widget), exactly as before this scroll-area wrapper was introduced.
    """
    
    def __init__(self, parent=None):
        """
        Initialize the base tab widget.
        
        Args:
            parent: Parent widget (default: None).
        """
        super().__init__(parent)
        
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)
        
        content = QWidget()
        self.main_layout = QVBoxLayout(content)
        self.main_layout.setSpacing(10)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        
        scroll_area.setWidget(content)
        outer_layout.addWidget(scroll_area)
    
    def init_ui(self):
        """
        Initialize the user interface.
        
        This method should be overridden by subclasses to add their
        specific UI components to the main_layout. The base implementation
        does nothing.
        """
        pass
