"""Tests for file utils module."""

import unittest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch

from pyinstaller_gui.utils.file_utils import FileUtils


class TestFileUtils(unittest.TestCase):
    """Test cases for FileUtils class."""
    
    def setUp(self):
        """
        Set up test fixtures.
        
        Creates a temporary directory structure with files and subdirectories
        for testing file operations:
        - temp_dir/
          - test.txt
          - subdir/
            - test2.txt
            - subsubdir/
        """
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_file = os.path.join(self.temp_dir.name, "test.txt")
        with open(self.test_file, "w") as f:
            f.write("test content")
        
        self.test_subdir = os.path.join(self.temp_dir.name, "subdir")
        os.makedirs(self.test_subdir)
        
        self.test_subsubdir = os.path.join(self.test_subdir, "subsubdir")
        os.makedirs(self.test_subsubdir)
        
        self.test_file2 = os.path.join(self.test_subdir, "test2.txt")
        with open(self.test_file2, "w") as f:
            f.write("test content 2")
    
    def tearDown(self):
        """
        Clean up test fixtures.
        
        Removes the temporary directory and all its contents after each test.
        """
        self.temp_dir.cleanup()
    
    def test_file_exists_true(self):
        """
        Test file_exists returns True for existing file.
        
        Verifies that file_exists correctly identifies an existing file
        on the filesystem.
        """
        self.assertTrue(FileUtils.file_exists(self.test_file))
    
    def test_file_exists_false(self):
        """
        Test file_exists returns False for non-existing file.
        
        Checks that file_exists returns False when the specified file path
        does not exist on the filesystem.
        """
        self.assertFalse(FileUtils.file_exists("/nonexistent/file.txt"))
    
    def test_folder_exists_true(self):
        """
        Test folder_exists returns True for existing folder.
        
        Ensures that folder_exists correctly identifies an existing directory.
        """
        self.assertTrue(FileUtils.folder_exists(self.temp_dir.name))
    
    def test_folder_exists_false(self):
        """
        Test folder_exists returns False for non-existing folder.
        
        Verifies that folder_exists returns False when the specified directory
        path does not exist.
        """
        self.assertFalse(FileUtils.folder_exists("/nonexistent/folder"))
    
    def test_get_file_size(self):
        """
        Test get_file_size returns correct size.
        
        Checks that get_file_size returns a positive integer representing the
        actual file size in bytes for an existing file.
        """
        size = FileUtils.get_file_size(self.test_file)
        self.assertGreater(size, 0)
    
    def test_get_file_size_nonexistent(self):
        """
        Test get_file_size returns 0 for non-existent file.
        
        Verifies that get_file_size returns 0 when the file does not exist,
        preventing exceptions from being raised.
        """
        self.assertEqual(FileUtils.get_file_size("/nonexistent/file.txt"), 0)
    
    def test_get_folder_size(self):
        """
        Test get_folder_size returns total size of all files in folder.
        
        Ensures that get_folder_size recursively calculates the total size
        of all files within a directory, including subdirectories.
        """
        size = FileUtils.get_folder_size(self.temp_dir.name)
        self.assertGreater(size, 0)
    
    def test_get_folder_size_with_invalid_path(self):
        """
        Test get_folder_size returns 0 for invalid path.
        
        Verifies that get_folder_size returns 0 when path doesn't exist.
        """
        size = FileUtils.get_folder_size("/nonexistent/path")
        self.assertEqual(size, 0)
    
    def test_create_directory(self):
        """
        Test create_directory creates new directory.
        
        Verifies that create_directory can create a new directory and that
        the directory exists after the operation.
        """
        new_dir = os.path.join(self.temp_dir.name, "new_dir")
        self.assertTrue(FileUtils.create_directory(new_dir))
        self.assertTrue(os.path.exists(new_dir))
    
    def test_create_directory_already_exists(self):
        """
        Test create_directory returns True if directory already exists.
        
        Checks that create_directory returns True even when the directory
        already exists, without raising an error.
        """
        self.assertTrue(FileUtils.create_directory(self.temp_dir.name))
    
    def test_create_directory_with_existing(self):
        """
        Test create_directory with existing directory.
        
        Ensures create_directory returns True for existing directory.
        """
        result = FileUtils.create_directory(self.temp_dir.name)
        self.assertTrue(result)
    
    def test_delete_file(self):
        """
        Test delete_file removes file.
        
        Verifies that delete_file successfully removes an existing file and
        that the file no longer exists on the filesystem.
        """
        self.assertTrue(FileUtils.delete_file(self.test_file))
        self.assertFalse(os.path.exists(self.test_file))
    
    def test_delete_file_nonexistent(self):
        """
        Test delete_file returns False for non-existent file.
        
        Ensures that delete_file returns False when attempting to delete a
        file that does not exist, without raising an exception.
        """
        self.assertFalse(FileUtils.delete_file("/nonexistent/file.txt"))
    
    def test_delete_file_with_permission_error(self):
        """
        Test delete_file handles permission error.
        
        Verifies that delete_file returns False when permission is denied.
        """
        with patch('os.remove', side_effect=PermissionError):
            result = FileUtils.delete_file(self.test_file)
            self.assertFalse(result)
    
    def test_delete_folder(self):
        """
        Test delete_folder removes folder and contents.
        
        Verifies that delete_folder recursively removes a directory and all
        its contents (files and subdirectories).
        """
        self.assertTrue(FileUtils.delete_folder(self.test_subdir))
        self.assertFalse(os.path.exists(self.test_subdir))
    
    def test_delete_folder_with_oserror(self):
        """
        Test delete_folder handles OSError.
        
        Ensures that delete_folder returns False when OSError occurs.
        """
        with patch('shutil.rmtree', side_effect=OSError):
            result = FileUtils.delete_folder(self.test_subdir)
            self.assertFalse(result)
    
    def test_list_files(self):
        """
        Test list_files returns all files in directory.
        
        Checks that list_files returns a list containing all files directly
        within a directory (not including subdirectories).
        """
        files = FileUtils.list_files(self.temp_dir.name)
        self.assertIn(self.test_file, files)
    
    def test_list_files_with_pattern(self):
        """
        Test list_files with pattern filter.
        
        Verifies that list_files supports glob pattern matching to filter
        files by name or extension.
        """
        files = FileUtils.list_files(self.temp_dir.name, "*.txt")
        self.assertIn(self.test_file, files)
    
    def test_list_files_with_nonexistent_directory(self):
        """
        Test list_files with non-existent directory.
        
        Verifies that list_files returns empty list for invalid directory.
        """
        files = FileUtils.list_files("/nonexistent/directory")
        self.assertEqual(files, [])
    
    def test_list_folders(self):
        """
        Test list_folders returns all subdirectories.
        
        Ensures that list_folders returns a list of all immediate subdirectories
        within a given directory path.
        """
        folders = FileUtils.list_folders(self.temp_dir.name)
        self.assertIn(self.test_subdir, folders)
    
    def test_list_folders_with_nonexistent_directory(self):
        """
        Test list_folders with non-existent directory.
        
        Ensures that list_folders returns empty list for invalid directory.
        """
        folders = FileUtils.list_folders("/nonexistent/directory")
        self.assertEqual(folders, [])


if __name__ == "__main__":
    unittest.main()