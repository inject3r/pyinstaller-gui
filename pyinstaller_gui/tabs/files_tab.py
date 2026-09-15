"""Additional files configuration tab."""

from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QHBoxLayout, QGroupBox, QVBoxLayout, 
    QFileDialog, QMessageBox, QLineEdit, QInputDialog
)
from PyQt6.QtCore import pyqtSignal, Qt

from .base_tab import BaseTab
from ..widgets.file_tree_widget import FileTreeWidget
from ..models.file_item import FileType


class FilesTab(BaseTab):
    """
    Tab for managing additional files and folders.
    
    This tab allows users to add, edit, search, and remove files, folders,
    and binaries that will be bundled with the executable. It features:
    - Search/filter functionality for large file lists
    - Edit capability for modifying existing entries (supports double-click)
    - Remove all items with confirmation dialog
    - Counter showing total/filtered items
    - Help dialog explaining usage
    """
    
    files_changed = pyqtSignal(list)
    
    def __init__(self, parent=None):
        """
        Initialize the additional files tab.
        
        Args:
            parent: Parent widget (default: None).
        """
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """
        Initialize the user interface.
        
        Creates the header with help button, search box for filtering,
        buttons for adding files/folders/binaries, edit and remove all buttons,
        file tree widget, counter label, and info label.
        """
        # Help button in header
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 5)
        
        header_label = QLabel("Additional Files")
        header_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        
        self.files_help_button = QPushButton("?")
        self.files_help_button.setFixedSize(24, 24)
        self.files_help_button.setToolTip("Show help for Additional Files")
        self.files_help_button.setStyleSheet("""
            QPushButton {
                background-color: #2D8FBA;
                color: white;
                border-radius: 12px;
                font-weight: bold;
                font-size: 14px;
                padding: 0px;
                margin: 0px;
            }
            QPushButton:hover {
                background-color: #1A5C7E;
            }
        """)
        
        header_layout.addWidget(header_label)
        header_layout.addStretch()
        header_layout.addWidget(self.files_help_button)
        
        self.main_layout.addWidget(header_widget)
        
        # Search box
        search_widget = QWidget()
        search_layout = QHBoxLayout(search_widget)
        search_layout.setContentsMargins(0, 0, 0, 10)
        
        search_label = QLabel("Search:")
        search_label.setToolTip("Search for files in the list")
        
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search files...")
        self.search_box.setToolTip("Type to filter files by name")
        self.search_box.textChanged.connect(self.filter_files)
        self.search_box.setClearButtonEnabled(True)
        
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_box)
        
        self.main_layout.addWidget(search_widget)
        
        # Buttons widget - All buttons in one row
        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(buttons_widget)
        buttons_layout.setContentsMargins(0, 0, 0, 10)
        buttons_layout.setSpacing(10)
        
        self.add_files_button = QPushButton("Add Files")
        self.add_files_button.setToolTip("Add individual files to include with your executable")
        
        self.add_folder_button = QPushButton("Add Folder")
        self.add_folder_button.setToolTip("Add an entire folder to include with your executable")
        
        self.add_binary_button = QPushButton("Add Binary")
        self.add_binary_button.setToolTip("Add binary files (DLLs, SOs, etc.)")
        
        self.edit_button = QPushButton("Edit Selected")
        self.edit_button.setToolTip("Edit the selected file/folder path")
        self.edit_button.setEnabled(False)
        
        self.remove_all_button = QPushButton("Remove All")
        self.remove_all_button.setToolTip("Remove all files/folders from the list")
        
        buttons_layout.addWidget(self.add_files_button)
        buttons_layout.addWidget(self.add_folder_button)
        buttons_layout.addWidget(self.add_binary_button)
        buttons_layout.addWidget(self.edit_button)
        buttons_layout.addWidget(self.remove_all_button)
        buttons_layout.addStretch()
        
        # File tree
        self.file_tree = FileTreeWidget()
        self.file_tree.setToolTip("List of additional files/folders to include\nDouble-click to edit")
        self.file_tree.files_changed.connect(self.on_files_changed)
        self.file_tree.itemSelectionChanged.connect(self.on_selection_changed)
        self.file_tree.itemDoubleClicked.connect(self.edit_selected_item)
        
        # Group box
        group_box = QGroupBox("Additional Files")
        group_layout = QVBoxLayout()
        group_layout.addWidget(buttons_widget)
        group_layout.addWidget(self.file_tree)
        group_box.setLayout(group_layout)
        
        self.main_layout.addWidget(group_box)
        
        # Counter label
        self.counter_label = QLabel("Total items: 0")
        self.counter_label.setStyleSheet("color: #7A8089; font-size: 11px; margin-top: 5px;")
        
        # Info label
        info_label = QLabel("Tip: Added files will be placed in the root directory of your executable")
        info_label.setStyleSheet("color: #7A8089; font-size: 11px;")
        info_label.setWordWrap(True)
        
        self.main_layout.addWidget(self.counter_label)
        self.main_layout.addWidget(info_label)
        self.main_layout.addStretch()
        
        # Connect signals
        self.add_files_button.clicked.connect(self.add_files)
        self.add_folder_button.clicked.connect(self.add_folder)
        self.add_binary_button.clicked.connect(self.add_binary)
        self.edit_button.clicked.connect(self.edit_selected_item)
        self.remove_all_button.clicked.connect(self.remove_all_items)
        self.files_help_button.clicked.connect(self.show_help)
    
    def filter_files(self, text: str):
        """
        Filter files in the tree based on search text.
        
        Hides items that don't match the search text and updates the
        counter label to show how many items are visible.
        
        Args:
            text: The search text to filter by.
        """
        tree = self.file_tree
        text_lower = text.lower()
        visible_count = 0
        
        for i in range(tree.topLevelItemCount()):
            item = tree.topLevelItem(i)
            file_name = item.text(0).lower()
            is_visible = text_lower in file_name if text_lower else True
            item.setHidden(not is_visible)
            if is_visible:
                visible_count += 1
        
        total = tree.topLevelItemCount()
        if text and visible_count != total:
            self.counter_label.setText(f"Showing {visible_count} of {total} items (filtered)")
        else:
            self.counter_label.setText(f"Total items: {total}")
    
    def on_selection_changed(self):
        """
        Handle selection change in the tree.
        
        Enables the edit button only when exactly one item is selected.
        """
        selected_items = self.file_tree.selectedItems()
        self.edit_button.setEnabled(len(selected_items) == 1)
    
    def edit_selected_item(self):
        """
        Edit the selected file/folder path.
        
        Opens the appropriate file/folder dialog based on the item type.
        Supports File, Folder, and Binary types. Updates the item's path
        and stored FileItem data. Shows a warning if no item is selected.
        """
        selected_items = self.file_tree.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select an item to edit.")
            return
        
        item = selected_items[0]
        old_path = item.text(0)
        file_type = item.text(1)
        
        if file_type == "File":
            new_path, _ = QFileDialog.getOpenFileName(
                self, "Select New File", old_path, "All Files (*)"
            )
        elif file_type == "Folder":
            new_path = QFileDialog.getExistingDirectory(
                self, "Select New Folder", old_path
            )
        elif file_type == "Binary":
            new_path, _ = QFileDialog.getOpenFileName(
                self, "Select New Binary File", old_path, 
                "Executable Files (*.dll *.so *.dylib *.exe);;All Files (*)"
            )
        else:
            new_path, ok = QInputDialog.getText(
                self, "Edit Path", "Enter new path:", text=old_path
            )
            if not ok:
                return
        
        if new_path:
            item.setText(0, new_path)
            from ..models.file_item import FileItem
            file_type_enum = None
            if file_type == "File":
                file_type_enum = FileType.FILE
            elif file_type == "Folder":
                file_type_enum = FileType.FOLDER
            elif file_type == "Binary":
                file_type_enum = FileType.BINARY
            
            if file_type_enum:
                item.setData(0, Qt.ItemDataRole.UserRole, FileItem(new_path, file_type_enum))
            
            self.on_files_changed()
            QMessageBox.information(self, "Updated", f"Path updated to:\n{new_path}")
    
    def remove_all_items(self):
        """
        Remove all items from the tree.
        
        Shows a confirmation dialog before clearing all items to prevent
        accidental deletion. Updates the counter label and clears the search box.
        """
        if self.file_tree.topLevelItemCount() == 0:
            QMessageBox.warning(self, "Nothing to Remove", "The list is already empty.")
            return
        
        reply = QMessageBox.question(
            self, "Confirm Remove All",
            f"Are you sure you want to remove all {self.file_tree.topLevelItemCount()} items?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.file_tree.clear_items()
            self.counter_label.setText("Total items: 0")
            self.search_box.clear()
            QMessageBox.information(self, "Removed", "All items have been removed.")
    
    def add_files(self):
        """
        Add files to the tree.
        
        Opens a multi-selection file dialog and adds each selected file
        as a FileType.FILE item. Updates the counter after addition.
        """
        file_names, _ = QFileDialog.getOpenFileNames(
            self, "Select Files", "", "All Files (*)"
        )
        for file_name in file_names:
            self.file_tree.add_file(file_name, FileType.FILE)
        self.update_counter()
    
    def add_folder(self):
        """
        Add a folder to the tree.
        
        Opens a directory selection dialog and adds the selected folder
        as a FileType.FOLDER item. Updates the counter after addition.
        """
        folder_name = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_name:
            self.file_tree.add_file(folder_name, FileType.FOLDER)
        self.update_counter()
    
    def add_binary(self):
        """
        Add a binary file to the tree.
        
        Opens a file dialog filtered for executable files (DLL, SO, DYLIB, EXE)
        and adds the selected file as a FileType.BINARY item.
        Updates the counter after addition.
        """
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Binary File", "", 
            "Executable Files (*.dll *.so *.dylib *.exe);;All Files (*)"
        )
        if file_name:
            self.file_tree.add_file(file_name, FileType.BINARY)
        self.update_counter()
    
    def on_files_changed(self):
        """
        Emit signal when files change.
        
        Updates the internal file list and emits the files_changed signal
        to notify other components (like the command builder) of changes.
        """
        items = self.file_tree.get_items()
        self.files_changed.emit(items)
        self.update_counter()
    
    def update_counter(self):
        """
        Update the counter label.
        
        Shows total items or "Showing X of Y items" when search filter is active.
        """
        total = self.file_tree.topLevelItemCount()
        search_text = self.search_box.text()
        if search_text:
            visible = sum(1 for i in range(self.file_tree.topLevelItemCount()) 
                         if not self.file_tree.topLevelItem(i).isHidden())
            self.counter_label.setText(f"Showing {visible} of {total} items (filtered)")
        else:
            self.counter_label.setText(f"Total items: {total}")
    
    def show_help(self):
        """
        Show help dialog for Files tab.
        
        Displays a message box with detailed explanations of:
        - Why additional files are needed
        - How to add files, folders, and binaries
        - Search functionality
        - Edit and remove all features
        - How to access included files in code (sys._MEIPASS)
        """
        help_text = """
        <h3>Additional Files Help</h3>
        
        <b>Why add additional files?</b><br>
        If your application uses external files (images, configs, databases, etc.),<br>
        you need to include them so they're available in the executable.<br><br>
        
        <b>Add Files:</b><br>
        Include individual files like images, data files, or configuration files.<br><br>
        
        <b>Add Folder:</b><br>
        Include an entire directory structure (e.g., assets/, data/, locales/).<br><br>
        
        <b>Add Binary:</b><br>
        Include binary files like DLLs on Windows or SO files on Linux.<br>
        This is useful for third-party libraries.<br><br>
        
        <b>Search:</b><br>
        Type to filter the list of files by name.<br><br>
        
        <b>Edit Selected:</b><br>
        Change the path of a selected file/folder.<br>
        Double-click an item to edit it quickly.<br><br>
        
        <b>Remove All:</b><br>
        Clear all files/folders from the list.<br><br>
        
        <b>How to access these files in your code:</b><br>
        Use: sys._MEIPASS + '/filename' (onefile mode)<br>
        Or: os.path.dirname(sys.executable) + '/filename' (onedir mode)
        """
        
        QMessageBox.information(self, "Additional Files Help", help_text)