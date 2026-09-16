"""Tests for the FileItem destination ('dest') field."""

import unittest

from pyinstaller_gui.models.file_item import FileItem, FileType


class TestFileItemDestination(unittest.TestCase):
    """Test cases for FileItem's bundle-destination support."""

    def test_default_destination_is_root(self):
        """Without an explicit destination, items should target the bundle root."""
        item = FileItem("/path/to/file.txt", FileType.FILE)
        self.assertEqual(item.dest, ".")

    def test_custom_destination_is_preserved(self):
        """An explicit destination should be stored as given."""
        item = FileItem("/path/to/file.txt", FileType.FILE, dest="assets/images")
        self.assertEqual(item.dest, "assets/images")

    def test_blank_destination_normalizes_to_root(self):
        """A blank/whitespace-only destination should normalize to '.'."""
        self.assertEqual(FileItem("/p", FileType.FILE, dest="").dest, ".")
        self.assertEqual(FileItem("/p", FileType.FILE, dest="   ").dest, ".")

    def test_equality_considers_destination(self):
        """Two items with the same path/type but different dest are not equal."""
        item1 = FileItem("/path/to/file.txt", FileType.FILE, dest="a")
        item2 = FileItem("/path/to/file.txt", FileType.FILE, dest="b")
        item3 = FileItem("/path/to/file.txt", FileType.FILE, dest="a")
        self.assertNotEqual(item1, item2)
        self.assertEqual(item1, item3)

    def test_hash_considers_destination(self):
        """Items with different destinations should (almost always) hash differently
        and, more importantly, behave correctly when used in a set."""
        item1 = FileItem("/path/to/file.txt", FileType.FILE, dest="a")
        item2 = FileItem("/path/to/file.txt", FileType.FILE, dest="b")
        item_set = {item1, item2}
        self.assertEqual(len(item_set), 2)


if __name__ == "__main__":
    unittest.main()
