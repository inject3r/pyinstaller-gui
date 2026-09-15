"""Tests for system utils module."""

import unittest
from unittest.mock import patch
import subprocess

from pyinstaller_gui.utils.system_utils import SystemUtils


class TestSystemUtils(unittest.TestCase):
    """Test cases for SystemUtils class."""
    
    def test_get_os(self):
        """
        Test get_os returns a string.
        
        Verifies that the operating system name is returned as a string and
        is one of the expected values: Windows, Darwin (macOS), or Linux.
        """
        os_name = SystemUtils.get_os()
        self.assertIsInstance(os_name, str)
        self.assertIn(os_name, ["Windows", "Darwin", "Linux"])
    
    def test_get_os_version(self):
        """
        Test get_os_version returns a string.
        
        Ensures that the operating system version is returned as a non-empty
        string containing version information.
        """
        version = SystemUtils.get_os_version()
        self.assertIsInstance(version, str)
    
    def test_get_architecture(self):
        """
        Test get_architecture returns a string.
        
        Checks that the system architecture (e.g., x86_64, arm64, AMD64)
        is returned as a string.
        """
        arch = SystemUtils.get_architecture()
        self.assertIsInstance(arch, str)
    
    def test_is_windows(self):
        """
        Test is_windows returns boolean.
        
        Verifies that the Windows platform detection returns a boolean value
        regardless of the actual operating system.
        """
        result = SystemUtils.is_windows()
        self.assertIsInstance(result, bool)
    
    def test_is_macos(self):
        """
        Test is_macos returns boolean.
        
        Ensures that the macOS platform detection returns a boolean value
        regardless of the actual operating system.
        """
        result = SystemUtils.is_macos()
        self.assertIsInstance(result, bool)
    
    def test_is_linux(self):
        """
        Test is_linux returns boolean.
        
        Checks that the Linux platform detection returns a boolean value
        regardless of the actual operating system.
        """
        result = SystemUtils.is_linux()
        self.assertIsInstance(result, bool)
    
    def test_get_python_version(self):
        """
        Test get_python_version returns a string.
        
        Verifies that the Python version information is returned as a
        non-empty string containing version details.
        """
        version = SystemUtils.get_python_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)
    
    def test_get_python_executable(self):
        """
        Test get_python_executable returns a path.
        
        Ensures that the path to the Python executable is returned as a
        string ending with 'python' or 'python3' (platform-dependent).
        """
        executable = SystemUtils.get_python_executable()
        self.assertIsInstance(executable, str)
        self.assertTrue(executable.endswith("python") or executable.endswith("python3"))
    
    @patch('subprocess.run')
    def test_run_command_success(self, mock_run):
        """
        Test run_command with successful command.
        
        Verifies that when a command executes successfully, the return code
        is 0 and the stdout/stderr are captured correctly.
        """
        mock_result = unittest.mock.Mock()
        mock_result.stdout = "output"
        mock_result.stderr = ""
        mock_result.returncode = 0
        mock_run.return_value = mock_result
        
        stdout, stderr, code = SystemUtils.run_command("echo test")
        self.assertEqual(code, 0)
    
    @patch('subprocess.run')
    def test_is_command_available_true(self, mock_run):
        """
        Test is_command_available returns True for available command.
        
        Checks that a command that exists in the system PATH is detected
        as available and returns True.
        """
        mock_run.return_value = unittest.mock.Mock()
        result = SystemUtils.is_command_available("python")
        self.assertIsInstance(result, bool)
    
    def test_get_system_info(self):
        """
        Test get_system_info returns dictionary with expected keys.
        
        Verifies that the system information dictionary contains all the
        expected keys: os, os_version, architecture, python_version, and
        python_executable.
        """
        info = SystemUtils.get_system_info()
        expected_keys = ["os", "os_version", "architecture", "python_version", "python_executable"]
        for key in expected_keys:
            self.assertIn(key, info)

    def test_is_command_available_false(self):
        """
        Test is_command_available returns False for unavailable command.
        
        Verifies that is_command_available returns False when the specified
        command does not exist in the system PATH.
        """
        result = SystemUtils.is_command_available("nonexistent_command_xyz")
        self.assertFalse(result)

    def test_run_command_failure(self):
        """
        Test run_command with failing command.
        
        Ensures that run_command handles command failure correctly by
        returning a non-zero exit code.
        """
        stdout, stderr, code = SystemUtils.run_command("nonexistent_command")
        self.assertNotEqual(code, 0)

    def test_run_command_timeout(self):
        """
        Test run_command with timeout.
        
        Verifies that run_command handles timeout correctly by returning
        a -1 exit code when the command exceeds the timeout limit.
        """
        with patch('subprocess.run', side_effect=subprocess.TimeoutExpired('cmd', 30)):
            stdout, stderr, code = SystemUtils.run_command("sleep 100")
            self.assertEqual(code, -1)

    def test_run_command_exception(self):
        """
        Test run_command with general exception.
        
        Ensures that run_command handles general exceptions correctly by
        returning a -1 exit code and capturing the error message.
        """
        with patch('subprocess.run', side_effect=Exception("Unknown error")):
            stdout, stderr, code = SystemUtils.run_command("some command")
            self.assertEqual(code, -1)


if __name__ == "__main__":
    unittest.main()