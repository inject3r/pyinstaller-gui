import sys
from PyQt6.QtWidgets import QApplication
from .gui import PyInstallerGUI


def run():
    """
    Run the PyInstaller GUI application.
    
    Creates the QApplication instance, sets application metadata,
    initializes the main window, and starts the event loop.
    
    The application will exit when the main window is closed.
    """
    app = QApplication(sys.argv)
    app.setApplicationName("PyInstaller GUI")
    app.setOrganizationName("PyInstallerGUI")
    
    window = PyInstallerGUI()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    run()