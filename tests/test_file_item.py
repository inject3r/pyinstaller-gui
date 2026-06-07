"""Tests for file item model."""

import unittest

from pyinstaller_gui.models.file_item import FileItem, FileType


class TestFileItem(unittest.TestCase):
    """Test cases for FileItem and FileType classes."""
    
    def test_file_type_values(self):
        """
        Test FileType enum values.
        
        Verifies that the FileType enum contains the expected members with
        correct names: FILE, FOLDER, and BINARY.
        """
        self.assertEqual(FileType.FILE.name, "FILE")
        self.assertEqual(FileType.FOLDER.name, "FOLDER")
        self.assertEqual(FileType.BINARY.name, "BINARY")
    
    def test_file_type_string_conversion(self):
        """
        Test FileType string conversion.
        
        Ensures that converting FileType enum values to strings returns
        human-readable capitalized names: "File", "Folder", "Binary".
        """
        self.assertEqual(str(FileType.FILE), "File")
        self.assertEqual(str(FileType.FOLDER), "Folder")
        self.assertEqual(str(FileType.BINARY), "Binary")
    
    def test_file_item_creation(self):
        """
        Test creating FileItem instance.
        
        Verifies that a FileItem can be instantiated with a path and file type,
        and that both attributes are correctly stored.
        """
        item = FileItem("/path/to/file.txt", FileType.FILE)
        self.assertEqual(item.path, "/path/to/file.txt")
        self.assertEqual(item.file_type, FileType.FILE)
    
    def test_file_item_equality_same(self):
        """
        Test FileItem equality with same values.
        
        Checks that two FileItem instances with identical path and file type
        are considered equal.
        """
        item1 = FileItem("/path/to/file.txt", FileType.FILE)
        item2 = FileItem("/path/to/file.txt", FileType.FILE)
        self.assertEqual(item1, item2)
    
    def test_file_item_equality_different_path(self):
        """
        Test FileItem equality with different paths.
        
        Verifies that FileItem instances with different paths are considered
        not equal, even if they have the same file type.
        """
        item1 = FileItem("/path/to/file1.txt", FileType.FILE)
        item2 = FileItem("/path/to/file2.txt", FileType.FILE)
        self.assertNotEqual(item1, item2)
    
    def test_file_item_equality_different_type(self):
        """
        Test FileItem equality with different types.
        
        Ensures that FileItem instances with the same path but different
        file types are considered not equal.
        """
        item1 = FileItem("/path/to/item", FileType.FILE)
        item2 = FileItem("/path/to/item", FileType.FOLDER)
        self.assertNotEqual(item1, item2)
    
    def test_file_item_hash(self):
        """
        Test FileItem hashing.
        
        Verifies that two FileItem instances with identical attributes produce
        the same hash value, enabling their use as dictionary keys or set
        members.
        """
        item1 = FileItem("/path/to/file.txt", FileType.FILE)
        item2 = FileItem("/path/to/file.txt", FileType.FILE)
        self.assertEqual(hash(item1), hash(item2))
    
    def test_file_item_in_set(self):
        """
        Test FileItem can be used in set.
        
        Checks that duplicate FileItem instances (with same path and type)
        are treated as a single element when added to a Python set, thanks to
        proper equality and hashing implementation.
        """
        item1 = FileItem("/path/to/file.txt", FileType.FILE)
        item2 = FileItem("/path/to/file.txt", FileType.FILE)
        item_set = {item1, item2}
        self.assertEqual(len(item_set), 1)
    
    def test_file_item_with_folder_type(self):
        """
        Test FileItem with folder type.
        
        Verifies that a FileItem can represent a folder/directory by using
        the FOLDER file type.
        """
        item = FileItem("/path/to/folder", FileType.FOLDER)
        self.assertEqual(item.path, "/path/to/folder")
        self.assertEqual(item.file_type, FileType.FOLDER)
    
    def test_file_item_with_binary_type(self):
        """
        Test FileItem with binary type.
        
        Ensures that a FileItem can represent binary files (DLLs, SO files,
        executables) using the BINARY file type.
        """
        item = FileItem("/path/to/binary.dll", FileType.BINARY)
        self.assertEqual(item.path, "/path/to/binary.dll")
        self.assertEqual(item.file_type, FileType.BINARY)

    def test_file_item_repr(self):
        """
        Test FileItem string representation.
        
        Verifies that FileItem has a proper string representation.
        """
        item = FileItem("/path/to/file.txt", FileType.FILE)
        self.assertIsNotNone(repr(item))

if __name__ == "__main__":
    unittest.main()