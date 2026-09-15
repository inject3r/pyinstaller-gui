"""Version checking module."""

import subprocess
import sys


class VersionChecker:
    """
    Check Python and PyInstaller versions.
    
    This utility class provides static methods to retrieve the current
    versions of Python and PyInstaller as seen by the interpreter that is
    running this application (``sys.executable``). Using ``sys.executable``
    instead of a bare "python"/"pyinstaller" command name makes this work
    correctly and identically on Windows, macOS, and Linux, and also inside
    virtual environments, where a generic "python" command may not exist on
    PATH (many Linux distributions only ship "python3") or may resolve to a
    different interpreter than the one actually running the GUI.
    
    It handles various error cases gracefully and returns user-friendly
    messages instead of raising exceptions.
    """
    
    @staticmethod
    def get_python_version() -> str:
        """
        Get the Python version of the interpreter running this application.
        
        Executes ``<sys.executable> --version`` and returns the output.
        
        Returns:
            A string containing the Python version information, or
            "Python Version: Not Found" if the command fails, times out,
            or the interpreter can't be located.
        """
        try:
            result = subprocess.check_output(
                [sys.executable, "--version"],
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=5,
            )
            return result.strip()
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError, OSError):
            return "Python Version: Not Found"
    
    @staticmethod
    def get_pyinstaller_version() -> str:
        """
        Get the PyInstaller version available to this application.
        
        Runs PyInstaller as a module of the current interpreter
        (``<sys.executable> -m PyInstaller --version``) rather than relying
        on a "pyinstaller" script being present on PATH. This is more
        reliable across platforms and works correctly inside virtual
        environments.
        
        Returns:
            A string containing "PyInstaller Version: X.X.X", or
            "PyInstaller Version: Not Found" if the command fails, times out,
            or PyInstaller is not installed.
        """
        try:
            result = subprocess.check_output(
                [sys.executable, "-m", "PyInstaller", "--version"],
                text=True,
                stderr=subprocess.STDOUT,
                encoding="utf-8",
                errors="replace",
                timeout=15,
            )
            return f"PyInstaller Version: {result.strip()}"
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError, OSError):
            return "PyInstaller Version: Not Found"
