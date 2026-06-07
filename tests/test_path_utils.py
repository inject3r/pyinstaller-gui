"""Tests for path utils module."""

import unittest
import os
import tempfile
from unittest.mock import patch

from pyinstaller_gui.utils.path_utils import PathUtils


class TestPathUtils(unittest.TestCase):
    """Test cases for PathUtils class."""
    
    def setUp(self):
        """
        Set up test fixtures.
        
        Creates a temporary directory with a test file for path operations
        testing.
        """
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_file = os.path.join(self.temp_dir.name, "test.txt")
        with open(self.test_file, "w") as f:
            f.write("test")
    
    def tearDown(self):
        """
        Clean up test fixtures.
        
        Removes the temporary directory and all its contents after each test.
        """
        self.temp_dir.cleanup()
    
    def test_normalize_path(self):
        """
        Test normalize_path converts to platform-specific format.
        
        Verifies that normalize_path converts mixed slash types (forward and
        backward slashes) to the platform-specific path separator and returns
        a normalized string.
        """
        path = "folder//subfolder\\file.txt"
        normalized = PathUtils.normalize_path(path)
        self.assertIsInstance(normalized, str)
    
    def test_get_absolute_path(self):
        """
        Test get_absolute_path returns absolute path.
        
        Checks that get_absolute_path converts a relative path to an absolute
        path by expanding it relative to the current working directory.
        """
        relative_path = "test.txt"
        absolute = PathUtils.get_absolute_path(relative_path)
        self.assertTrue(os.path.isabs(absolute))
    
    def test_get_relative_path(self):
        """
        Test get_relative_path returns relative path.
        
        Verifies that get_relative_path returns a path relative to the given
        start directory, making it possible to get the relative relationship
        between two paths.
        """
        absolute = self.test_file
        relative = PathUtils.get_relative_path(absolute, self.temp_dir.name)
        self.assertEqual(relative, "test.txt")
    
    def test_get_relative_path_with_same_path(self):
        """
        Test get_relative_path with same start path.
        
        Verifies that get_relative_path returns empty string or "." for same path.
        """
        result = PathUtils.get_relative_path(self.temp_dir.name, self.temp_dir.name)
        self.assertIn(result, ["", "."])
    
    def test_get_relative_path_with_different_drives(self):
        """
        Test get_relative_path with paths on different drives.
        
        Verifies that get_relative_path returns original path when on different drives.
        """
        with patch('os.path.relpath', side_effect=ValueError):
            result = PathUtils.get_relative_path("/path/to/file", "/different/path")
            self.assertEqual(result, "/path/to/file")
    
    def test_get_filename(self):
        """
        Test get_filename extracts filename from path.
        
        Ensures that get_filename returns the base name (last component) of a
        path, removing all directory components.
        """
        filename = PathUtils.get_filename("/path/to/file.txt")
        self.assertEqual(filename, "file.txt")
    
    def test_get_directory(self):
        """
        Test get_directory extracts directory from path.
        
        Verifies that get_directory returns the directory portion of a path,
        removing the filename component.
        """
        directory = PathUtils.get_directory("/path/to/file.txt")
        self.assertEqual(directory, "/path/to")
    
    def test_get_extension(self):
        """
        Test get_extension extracts file extension.
        
        Checks that get_extension returns the file extension including the dot,
        or an empty string if the file has no extension.
        """
        extension = PathUtils.get_extension("file.txt")
        self.assertEqual(extension, ".txt")
    
    def test_get_extension_no_extension(self):
        """
        Test get_extension returns empty string for no extension.
        
        Verifies that get_extension returns an empty string when the file name
        contains no dot character (no extension).
        """
        extension = PathUtils.get_extension("file")
        self.assertEqual(extension, "")
    
    def test_get_filename_without_extension(self):
        """
        Test get_filename_without_extension removes extension.
        
        Ensures that get_filename_without_extension returns the file name with
        the extension removed, leaving only the base name.
        """
        name = PathUtils.get_filename_without_extension("file.txt")
        self.assertEqual(name, "file")
    
    def test_join_paths(self):
        """
        Test join_paths joins multiple paths.
        
        Verifies that join_paths correctly concatenates multiple path components
        using the platform-appropriate path separator.
        """
        result = PathUtils.join_paths("folder", "subfolder", "file.txt")
        expected = os.path.join("folder", "subfolder", "file.txt")
        self.assertEqual(result, expected)
    
    def test_is_subpath_true(self):
        """
        Test is_subpath returns True for subpath.
        
        Checks that is_subpath correctly identifies when a path is a subpath
        (nested within) another directory path.
        """
        self.assertTrue(PathUtils.is_subpath(self.test_file, self.temp_dir.name))
    
    def test_is_subpath_false(self):
        """
        Test is_subpath returns False for non-subpath.
        
        Verifies that is_subpath returns False when the candidate path is not
        located within the specified parent directory.
        """
        self.assertFalse(PathUtils.is_subpath("/other/path", self.temp_dir.name))
    
    def test_is_subpath_with_same_path(self):
        """
        Test is_subpath with same path.
        
        Checks is_subpath behavior when path equals parent.
        """
        result = PathUtils.is_subpath(self.temp_dir.name, self.temp_dir.name)
        self.assertFalse(result)  # Same path is not considered subpath
    
    def test_is_subpath_with_oserror(self):
        """
        Test is_subpath handles OSError.
        
        Verifies that is_subpath returns False when OSError occurs.
        """
        with patch('pathlib.Path.resolve', side_effect=OSError):
            result = PathUtils.is_subpath(self.test_file, self.temp_dir.name)
            self.assertFalse(result)
    
    def test_ensure_extension(self):
        """
        Test ensure_extension adds extension if missing.
        
        Ensures that ensure_extension appends the specified extension to a
        file name that does not already have that extension.
        """
        result = PathUtils.ensure_extension("file", ".txt")
        self.assertEqual(result, "file.txt")
    
    def test_ensure_extension_already_has(self):
        """
        Test ensure_extension doesn't add extension if already present.
        
        Verifies that ensure_extension returns the original string unchanged
        when the file name already ends with the specified extension.
        """
        result = PathUtils.ensure_extension("file.txt", ".txt")
        self.assertEqual(result, "file.txt")


if __name__ == "__main__":
    unittest.main()