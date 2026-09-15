"""File tree widget for managing additional files."""

from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal

from ..models.file_item import FileItem, FileType


class FileTreeWidget(QTreeWidget):
    """
    Tree widget for displaying and managing additional files.
    
    This widget provides a hierarchical view of files, folders, and binaries
    that will be bundled with the executable. Each item has:
    - Name column: The file/folder path
    - Type column: File, Folder, or Binary
    - Action column: A delete button to remove the item
    
    The widget supports extended selection mode for selecting multiple items.
    """
    
    files_changed = pyqtSignal()
    
    def __init__(self, parent=None):
        """
        Initialize the file tree widget.
        
        Args:
            parent: Parent widget (default: None).
        """
        super().__init__(parent)
        self.setHeaderLabels(["Name", "Type", "Action"])
        self.setColumnWidth(0, 350)
        self.setColumnWidth(1, 100)
        self.setColumnWidth(2, 80)
        self.setRootIsDecorated(False)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QTreeWidget.SelectionMode.ExtendedSelection)
    
    def add_file(self, path: str, file_type: FileType):
        """
        Add a file or folder to the tree.
        
        Creates a new tree item with the specified path and type, stores
        the FileItem in the item's user data, and adds a delete button
        in the action column.
        
        Args:
            path: The file system path of the item.
            file_type: The type of item (FILE, FOLDER, or BINARY).
        """
        item = QTreeWidgetItem(self)
        item.setText(0, path)
        item.setText(1, str(file_type))
        item.setData(0, Qt.ItemDataRole.UserRole, FileItem(path, file_type))
        
        delete_button = QPushButton("Delete")
        delete_button.setToolTip(f"Remove {path}")
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: #DC3545;
                padding: 4px;
            }
            QPushButton:hover {
                background-color: #C82333;
            }
        """)
        delete_button.clicked.connect(lambda: self.remove_item(item))
        self.setItemWidget(item, 2, delete_button)
        
        self.files_changed.emit()
    
    def remove_item(self, item: QTreeWidgetItem):
        """
        Remove an item from the tree.
        
        Args:
            item: The tree item to remove.
        """
        index = self.indexOfTopLevelItem(item)
        if index != -1:
            self.takeTopLevelItem(index)
            self.files_changed.emit()
    
    def get_items(self) -> list:
        """
        Get all file items from the tree.
        
        Returns:
            A list of FileItem objects representing all items currently
            in the tree, extracted from the user data of each row.
        """
        items = []
        for i in range(self.topLevelItemCount()):
            item = self.topLevelItem(i)
            file_item = item.data(0, Qt.ItemDataRole.UserRole)
            if file_item:
                items.append(file_item)
        return items
    
    def clear_items(self):
        """Clear all items from the tree and emit the files_changed signal."""
        self.clear()
        self.files_changed.emit()