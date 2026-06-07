"""Version checking module."""

import subprocess


class VersionChecker:
    """
    Check Python and PyInstaller versions.
    
    This utility class provides static methods to retrieve the current
    versions of Python and PyInstaller installed on the system. It handles
    various error cases gracefully and returns user-friendly messages
    instead of raising exceptions.
    """
    
    @staticmethod
    def get_python_version() -> str:
        """
        Get Python version.
        
        Executes the 'python --version' command and returns the output.
        
        Returns:
            A string containing the Python version information, or
            "Python Version: Not Found" if the command fails, times out,
            or Python is not installed.
        """
        try:
            result = subprocess.check_output(["python", "--version"], 
                                            stderr=subprocess.STDOUT,
                                            text=True,
                                            timeout=5)
            return result.strip()
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            return "Python Version: Not Found"
    
    @staticmethod
    def get_pyinstaller_version() -> str:
        """
        Get PyInstaller version.
        
        Executes the 'pyinstaller --version' command and returns the output
        formatted with a descriptive prefix.
        
        Returns:
            A string containing "PyInstaller Version: X.X.X", or
            "PyInstaller Version: Not Found" if the command fails, times out,
            or PyInstaller is not installed.
        """
        try:
            result = subprocess.check_output(["pyinstaller", "--version"],
                                            text=True,
                                            stderr=subprocess.STDOUT,
                                            timeout=5)
            return f"PyInstaller Version: {result.strip()}"
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            return "PyInstaller Version: Not Found"