"""System utility functions."""

import platform
import subprocess
import sys
from typing import Optional, Tuple


class SystemUtils:
    """Utility class for system operations."""
    
    @staticmethod
    def get_os() -> str:
        """
        Get operating system name.
        
        Returns:
            Operating system name: 'Windows', 'Darwin' (macOS), or 'Linux'.
        """
        return platform.system()
    
    @staticmethod
    def get_os_version() -> str:
        """
        Get operating system version.
        
        Returns:
            Operating system version string (platform-dependent format).
        """
        return platform.version()
    
    @staticmethod
    def get_architecture() -> str:
        """
        Get system architecture.
        
        Returns:
            Machine architecture (e.g., 'x86_64', 'AMD64', 'arm64').
        """
        return platform.machine()
    
    @staticmethod
    def is_windows() -> bool:
        """
        Check if running on Windows.
        
        Returns:
            True if the operating system is Windows, False otherwise.
        """
        return platform.system() == "Windows"
    
    @staticmethod
    def is_macos() -> bool:
        """
        Check if running on macOS.
        
        Returns:
            True if the operating system is macOS (Darwin), False otherwise.
        """
        return platform.system() == "Darwin"
    
    @staticmethod
    def is_linux() -> bool:
        """
        Check if running on Linux.
        
        Returns:
            True if the operating system is Linux, False otherwise.
        """
        return platform.system() == "Linux"
    
    @staticmethod
    def get_python_version() -> str:
        """
        Get Python version.
        
        Returns:
            Full Python version string including build information.
        """
        return sys.version
    
    @staticmethod
    def get_python_executable() -> str:
        """
        Get Python executable path.
        
        Returns:
            Absolute path to the Python interpreter executable.
        """
        return sys.executable
    
    @staticmethod
    def run_command(command: str) -> Tuple[str, str, int]:
        """
        Run a command and return stdout, stderr, and return code.
        
        Executes the specified command with a 30-second timeout.
        Captures both stdout and stderr output.
        
        Args:
            command: The command string to execute (supports shell syntax).
            
        Returns:
            A tuple containing (stdout, stderr, return_code). The return code
            is -1 if the command times out or encounters an exception.
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout, result.stderr, result.returncode
        except subprocess.TimeoutExpired:
            return "", "Command timed out", -1
        except Exception as e:
            return "", str(e), -1
    
    @staticmethod
    def is_command_available(command: str) -> bool:
        """
        Check if a command is available in PATH.
        
        Attempts to run the command with the --version flag to verify its
        existence without requiring successful execution.
        
        Args:
            command: The command name to check (e.g., 'python', 'git').
            
        Returns:
            True if the command exists and can be executed, False otherwise.
        """
        try:
            subprocess.run(
                [command, "--version"],
                capture_output=True,
                check=False
            )
            return True
        except FileNotFoundError:
            return False
    
    @staticmethod
    def get_system_info() -> dict:
        """
        Get system information.
        
        Returns a dictionary containing comprehensive system information
        including OS name, version, architecture, Python version, and
        Python executable path.
        
        Returns:
            Dictionary with keys: 'os', 'os_version', 'architecture',
            'python_version', 'python_executable'.
        """
        return {
            "os": SystemUtils.get_os(),
            "os_version": SystemUtils.get_os_version(),
            "architecture": SystemUtils.get_architecture(),
            "python_version": SystemUtils.get_python_version(),
            "python_executable": SystemUtils.get_python_executable(),
        }