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
    - Destination column: Where the item is placed inside the bundle
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
        self.setHeaderLabels(["Name", "Type", "Destination", "Action"])
        self.setColumnWidth(0, 300)
        self.setColumnWidth(1, 80)
        self.setColumnWidth(2, 130)
        self.setColumnWidth(3, 80)
        self.setRootIsDecorated(False)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QTreeWidget.SelectionMode.ExtendedSelection)
        # Editing is triggered explicitly (see FilesTab.on_item_double_clicked)
        # rather than automatically, so that double-clicking the Name column
        # can open a file/folder picker while the Destination column gets a
        # simple inline text editor.
        self.setEditTriggers(QTreeWidget.EditTrigger.NoEditTriggers)
        self.itemChanged.connect(self._on_item_changed)
    
    def _on_item_changed(self, item: QTreeWidgetItem, column: int):
        """
        Keep the stored FileItem in sync after an inline edit.
        
        Only the Destination column (index 2) is editable in place; any
        edit there is normalized (blank becomes ".") and written back into
        the item's stored FileItem so the command builder picks it up.
        
        Args:
            item: The tree item that changed.
            column: The column index that was edited.
        """
        if column != 2:
            return
        
        file_item = item.data(0, Qt.ItemDataRole.UserRole)
        if not isinstance(file_item, FileItem):
            return
        
        new_dest = item.text(2).strip() or "."
        if new_dest != file_item.dest:
            item.setData(0, Qt.ItemDataRole.UserRole, FileItem(file_item.path, file_item.file_type, new_dest))
            self.files_changed.emit()
        if item.text(2) != new_dest:
            # Normalize the visible text (e.g. blank -> ".") without
            # re-triggering an extra signal loop.
            self.blockSignals(True)
            item.setText(2, new_dest)
            self.blockSignals(False)
    
    def add_file(self, path: str, file_type: FileType, dest: str = "."):
        """
        Add a file or folder to the tree.
        
        Creates a new tree item with the specified path, type, and bundle
        destination, stores the FileItem in the item's user data, and adds
        a delete button in the action column.
        
        Args:
            path: The file system path of the item.
            file_type: The type of item (FILE, FOLDER, or BINARY).
            dest: Destination directory inside the bundle (default: ".",
                the top-level application directory).
        """
        dest = dest or "."
        item = QTreeWidgetItem(self)
        item.setText(0, path)
        item.setText(1, str(file_type))
        item.setText(2, dest)
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
        item.setData(0, Qt.ItemDataRole.UserRole, FileItem(path, file_type, dest))
        item.setToolTip(2, "Destination folder inside the bundled app. Double-click to edit.\nUse \".\" for the top-level application directory.")
        
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
        self.setItemWidget(item, 3, delete_button)
        
        self.files_changed.emit()
    
    def set_item_destination(self, item: QTreeWidgetItem, dest: str) -> None:
        """
        Update the bundle destination of an existing tree item.
        
        Args:
            item: The tree item to update.
            dest: The new destination directory (empty/blank normalizes to ".").
        """
        dest = dest.strip() if dest else "."
        if not dest:
            dest = "."
        
        file_item = item.data(0, Qt.ItemDataRole.UserRole)
        if isinstance(file_item, FileItem):
            item.setData(0, Qt.ItemDataRole.UserRole, FileItem(file_item.path, file_item.file_type, dest))
        item.setText(2, dest)
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
