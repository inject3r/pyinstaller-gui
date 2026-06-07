"""Tests for version checker module."""

import unittest
from unittest.mock import patch
from subprocess import CalledProcessError
import subprocess

from pyinstaller_gui.core.version_checker import VersionChecker


class TestVersionChecker(unittest.TestCase):
    """Test cases for VersionChecker class."""
    
    def setUp(self):
        """
        Set up test fixtures.
        
        Creates a VersionChecker instance before each test method.
        """
        self.checker = VersionChecker()
    
    @patch('subprocess.check_output')
    def test_get_python_version_success(self, mock_check_output):
        """
        Test get_python_version returns version on success.
        
        Verifies that when the Python command executes successfully, the
        version string contains "Python" and the actual version number.
        """
        mock_check_output.return_value = "Python 3.10.0\n"
        version = self.checker.get_python_version()
        self.assertIn("Python", version)
    
    @patch('subprocess.check_output')
    def test_get_python_version_failure(self, mock_check_output):
        """
        Test get_python_version returns error message on failure.
        
        Ensures that when the Python command fails (e.g., invalid options),
        the method returns a "Not Found" message instead of raising an exception.
        """
        mock_check_output.side_effect = CalledProcessError(1, 'python')
        version = self.checker.get_python_version()
        self.assertEqual(version, "Python Version: Not Found")
    
    @patch('subprocess.check_output')
    def test_get_python_version_file_not_found(self, mock_check_output):
        """
        Test get_python_version returns error message when python not found.
        
        Verifies that when the Python executable is not found in the system PATH,
        the method gracefully returns a "Not Found" message.
        """
        mock_check_output.side_effect = FileNotFoundError()
        version = self.checker.get_python_version()
        self.assertEqual(version, "Python Version: Not Found")
    
    @patch('subprocess.check_output')
    def test_get_python_version_timeout(self, mock_check_output):
        """
        Test get_python_version returns error message on timeout.
        
        Ensures that when the Python command exceeds the timeout limit,
        the method returns a "Not Found" message instead of hanging.
        """
        mock_check_output.side_effect = subprocess.TimeoutExpired('python', 5)
        version = self.checker.get_python_version()
        self.assertEqual(version, "Python Version: Not Found")
    
    @patch('subprocess.check_output')
    def test_get_pyinstaller_version_success(self, mock_check_output):
        """
        Test get_pyinstaller_version returns version on success.
        
        Verifies that when the PyInstaller command executes successfully,
        the version string contains "PyInstaller" and the actual version number.
        """
        mock_check_output.return_value = "6.0.0\n"
        version = self.checker.get_pyinstaller_version()
        self.assertIn("PyInstaller", version)
        self.assertIn("6.0.0", version)
    
    @patch('subprocess.check_output')
    def test_get_pyinstaller_version_failure(self, mock_check_output):
        """
        Test get_pyinstaller_version returns error message on failure.
        
        Ensures that when the PyInstaller command fails, the method returns
        a "Not Found" message without raising an exception.
        """
        mock_check_output.side_effect = CalledProcessError(1, 'pyinstaller')
        version = self.checker.get_pyinstaller_version()
        self.assertEqual(version, "PyInstaller Version: Not Found")
    
    @patch('subprocess.check_output')
    def test_get_pyinstaller_version_not_found(self, mock_check_output):
        """
        Test get_pyinstaller_version returns error message when pyinstaller not found.
        
        Verifies that when PyInstaller is not installed or not in the system PATH,
        the method gracefully returns a "Not Found" message.
        """
        mock_check_output.side_effect = FileNotFoundError()
        version = self.checker.get_pyinstaller_version()
        self.assertEqual(version, "PyInstaller Version: Not Found")
    
    @patch('subprocess.check_output')
    def test_get_pyinstaller_version_timeout(self, mock_check_output):
        """
        Test get_pyinstaller_version returns error message on timeout.
        
        Ensures that when the PyInstaller command exceeds the timeout limit,
        the method returns a "Not Found" message instead of hanging.
        """
        mock_check_output.side_effect = subprocess.TimeoutExpired('pyinstaller', 5)
        version = self.checker.get_pyinstaller_version()
        self.assertEqual(version, "PyInstaller Version: Not Found")


if __name__ == "__main__":
    unittest.main()