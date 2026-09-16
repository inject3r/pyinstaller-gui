"""Background worker for non-blocking version detection."""

from PyQt6.QtCore import QThread, pyqtSignal

from ..core.version_checker import VersionChecker


class VersionCheckWorker(QThread):
    """
    Worker thread that fetches Python and PyInstaller version strings.
    
    VersionChecker shells out to the interpreter twice (``--version`` and
    ``-m PyInstaller --version``), which is normally fast but can still
    take a noticeable moment - especially the first time PyInstaller's
    module machinery is imported, or on a slow/loaded machine. Running
    this on the main thread at application startup would freeze the
    window for that entire time. This worker moves that work off the UI
    thread so the window appears immediately and fills in the version
    labels a moment later.
    """
    
    versions_ready = pyqtSignal(str, str)
    
    def __init__(self, parent=None):
        """
        Initialize the version check worker.
        
        Args:
            parent: Optional parent QObject.
        """
        super().__init__(parent)
        self.version_checker = VersionChecker()
    
    def run(self):
        """
        Fetch both version strings and emit them together.
        
        Emits ``versions_ready(python_version, pyinstaller_version)`` once
        both lookups have completed.
        """
        python_version = self.version_checker.get_python_version()
        pyinstaller_version = self.version_checker.get_pyinstaller_version()
        self.versions_ready.emit(python_version, pyinstaller_version)
