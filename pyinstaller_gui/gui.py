import subprocess
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFileDialog, QTabWidget, QComboBox,
    QCheckBox, QLineEdit, QLabel, QHBoxLayout, QTextEdit, QGroupBox, QTreeWidget, QTreeWidgetItem
)

from pyinstaller_thread import PyInstallerThread
from styles import STYLE_SHEET, GITHUB_BUTTON_STYLE, PROJECT_NAME_STYLE, PROJECT_VERSION_STYLE
from project_info import *

class PyInstallerGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(PROJECT_NAME)
        self.setGeometry(100, 100, 600, 500)
        self.setStyleSheet(STYLE_SHEET)
        layout = QVBoxLayout()

        self.logo_label = QLabel(PROJECT_NAME)
        self.logo_label.setStyleSheet(PROJECT_NAME_STYLE)
        layout.addWidget(self.logo_label)

        self.version_label = QLabel(f"Version {PROJECT_VERSION}")
        self.version_label.setStyleSheet(PROJECT_VERSION_STYLE)
        layout.addWidget(self.version_label)

        self.github_button = QPushButton("Visit on GitHub")
        self.github_button.setStyleSheet(GITHUB_BUTTON_STYLE)
        self.github_button.clicked.connect(self.open_github)
        layout.addWidget(self.github_button)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        self.general_tab = QWidget()
        self.icon_tab = QWidget()
        self.additional_files_tab = QWidget()
        self.advanced_tab = QWidget()
        self.settings_tab = QWidget()

        self.tabs.addTab(self.general_tab, "General")
        self.tabs.addTab(self.additional_files_tab, "Additional Files")
        self.tabs.addTab(self.advanced_tab, "Advanced")
        self.tabs.addTab(self.settings_tab, "Settings")

        self.general_layout = QVBoxLayout(self.general_tab)
        self.general_tab.setLayout(self.general_layout)

        self.additional_files_layout = QVBoxLayout(self.additional_files_tab)
        self.additional_files_tab.setLayout(self.additional_files_layout)

        self.advanced_layout = QVBoxLayout(self.advanced_tab)
        self.advanced_tab.setLayout(self.advanced_layout)

        self.settings_layout = QVBoxLayout(self.settings_tab)
        self.settings_tab.setLayout(self.settings_layout)


        self.script_label = QLabel("Select script:")
        self.script_path = QLineEdit()
        self.script_path.setPlaceholderText("Enter script location...")
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_script)

        file_layout = QHBoxLayout()
        file_layout.addWidget(self.script_path)
        file_layout.addWidget(self.browse_button)

        self.general_layout.addWidget(self.script_label)
        self.general_layout.addLayout(file_layout)

        self.app_name_label = QLabel("Application name:")
        self.app_name_input = QLineEdit()
        self.app_name_input.setPlaceholderText("Application name (Default name of the first script)")

        self.general_layout.addWidget(self.app_name_label)
        self.general_layout.addWidget(self.app_name_input)


        self.onefile_checkbox = QCheckBox("OneFile (-F)")
        self.noconsole_checkbox = QCheckBox("No Console (-w)")
        self.hidden_imports = QLineEdit()
        self.hidden_imports.setPlaceholderText("Hidden Imports (comma-separated)")

        self.general_layout.addWidget(self.onefile_checkbox)
        self.general_layout.addWidget(self.noconsole_checkbox)
        self.general_layout.addWidget(self.hidden_imports)


        self.additional_files_tree = QTreeWidget()
        self.additional_files_tree.setHeaderLabels(["Name", "Type", "Action"])
        self.additional_files_tree.setColumnWidth(0, 300)
        self.additional_files_tree.setColumnWidth(1, 100)
        self.additional_files_tree.setColumnWidth(2, 80)
        self.additional_files_tree.setRootIsDecorated(False)

        self.add_files_button = QPushButton("Add Files")
        self.add_files_button.clicked.connect(self.add_files)

        self.add_folder_button = QPushButton("Add Folder")
        self.add_folder_button.clicked.connect(self.add_folder)

        self.add_binary_button = QPushButton("Add Binary")
        self.add_binary_button.clicked.connect(self.add_binary)

        self.additional_files_group = QGroupBox("Additional Files")
        additional_files_layout = QVBoxLayout()
        additional_files_layout.addWidget(self.add_files_button)
        additional_files_layout.addWidget(self.add_folder_button)
        additional_files_layout.addWidget(self.add_binary_button)
        additional_files_layout.addWidget(self.additional_files_tree)
        self.additional_files_group.setLayout(additional_files_layout)

        self.additional_files_layout.addWidget(self.additional_files_group)


        self.output_folder_label = QLabel("Select Output Folder:")
        self.output_folder_path = QLineEdit()
        self.output_folder_path.setPlaceholderText("Setting the program output location")
        self.output_folder_button = QPushButton("Browse Output Folder")
        self.output_folder_button.clicked.connect(self.browse_output_folder)

        folder_layout = QHBoxLayout()
        folder_layout.addWidget(self.output_folder_path)
        folder_layout.addWidget(self.output_folder_button)

        self.settings_layout.addWidget(self.output_folder_label)
        self.settings_layout.addLayout(folder_layout)

        self.icon_path = QLineEdit()
        self.icon_path.setPlaceholderText("Icon File (.ico for Windows, .icns for Mac)")
        self.browse_icon_button = QPushButton("Browse Icon")
        self.browse_icon_button.clicked.connect(self.browse_icon)

        icon_layout = QHBoxLayout()
        icon_layout.addWidget(self.icon_path)
        icon_layout.addWidget(self.browse_icon_button)
        self.settings_layout.addLayout(icon_layout)


        self.tmpdir_label = QLabel("Runtime Tmpdir:")
        self.tmpdir_input = QLineEdit()
        self.tmpdir_input.setPlaceholderText("Specify a temp directory to boost performance")
        self.settings_layout.addWidget(self.tmpdir_label)
        self.settings_layout.addWidget(self.tmpdir_input)

        self.custom_commands_label = QLabel("Custom Commands:")
        self.custom_commands = QLineEdit()
        self.custom_commands.setPlaceholderText("Enter additional commands here")
        self.settings_layout.addWidget(self.custom_commands_label)
        self.settings_layout.addWidget(self.custom_commands)


        self.advanced_label = QLabel("Advanced Settings")

        self.log_level_label = QLabel("Log Level:")
        self.log_level_combo = QComboBox()
        self.log_level_combo.addItems(["DEBUG", "INFO", "WARN", "ERROR"])

        self.advanced_layout.addWidget(self.log_level_label)
        self.advanced_layout.addWidget(self.log_level_combo)


        self.upx_label = QLabel("UPX Directory:")
        self.upx_path = QLineEdit()
        self.upx_path.setPlaceholderText("Set the UPX path to compress binary files")
        self.upx_button = QPushButton("Browse")
        self.upx_button.clicked.connect(self.select_upx_dir)

        upx_layout = QHBoxLayout()
        upx_layout.addWidget(self.upx_path)
        upx_layout.addWidget(self.upx_button)
        self.advanced_layout.addWidget(self.upx_label)
        self.advanced_layout.addLayout(upx_layout)


        self.debug_label = QLabel("Debug Mode:")
        self.debug_combo = QComboBox()
        self.debug_combo.addItems(["None", "Imports", "All", "NoArchive"])

        self.advanced_layout.addWidget(self.debug_label)
        self.advanced_layout.addWidget(self.debug_combo)

        self.key_label = QLabel("Encryption Key:")
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Enter your encryption key here")

        self.advanced_layout.addWidget(self.key_label)
        self.advanced_layout.addWidget(self.key_input)

        

        self.cmd_clean = QCheckBox("--clean (Clear PyInstaller cache and temp files before building.)")

        self.advanced_layout.addWidget(self.cmd_clean)


        self.command_preview = QTextEdit()
        self.command_preview.setReadOnly(True)
        self.command_preview.setFixedHeight(60)
        self.command_preview_label = QLabel("Generated Command:")
        self.command_preview_label.setStyleSheet("margin-top: 10px;")
        layout.addWidget(self.command_preview_label)
        layout.addWidget(self.command_preview)

        self.output_console = QTextEdit()
        self.output_console.setReadOnly(True)
        self.output_console.setFixedHeight(90)
        layout.addWidget(QLabel("Output Console:"))
        layout.addWidget(self.output_console)

        self.python_version_label = QLabel("Python Version: --")
        layout.addWidget(self.python_version_label)

        self.pyinstaller_version_label = QLabel("PyInstaller Version: --")
        layout.addWidget(self.pyinstaller_version_label)

        self.run_button = QPushButton("Run PyInstaller")
        self.run_button.clicked.connect(self.run_pyinstaller)

        layout.addWidget(self.run_button)

        self.setLayout(layout)

        # Display versions
        self.display_versions()

        # Connect signals to update the command instantly
        self.script_path.textChanged.connect(self.update_command)
        self.app_name_input.textChanged.connect(self.update_command)
        self.onefile_checkbox.toggled.connect(self.update_command)
        self.noconsole_checkbox.toggled.connect(self.update_command)
        self.hidden_imports.textChanged.connect(self.update_command)
        self.output_folder_path.textChanged.connect(self.update_command)
        self.custom_commands.textChanged.connect(self.update_command)
        self.icon_path.textChanged.connect(self.update_command)
        self.additional_files_tree.itemChanged.connect(self.update_command)
        self.log_level_combo.currentIndexChanged.connect(self.update_command)
        self.debug_combo.currentTextChanged.connect(self.update_command)
        self.cmd_clean.toggled.connect(self.update_command)
        self.tmpdir_input.textChanged.connect(self.update_command)
        self.key_input.textChanged.connect(self.update_command)


    def select_upx_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select UPX Directory")
        if dir_path:
            self.upx_path.setText(dir_path)
            self.update_command()

    def browse_output_folder(self):
        folder_name = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder_name:
            self.output_folder_path.setText(folder_name)

    def open_github(self):
        import webbrowser
        webbrowser.open("https://github.com/inject3r/pyinstaller-gui")

    def browse_script(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Python Script", "", "Python Files (*.py)")
        if file_name:
            self.script_path.setText(file_name)

    def browse_icon(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Icon", "", "Icon Files (*.ico *.icns)")
        if file_name:
            self.icon_path.setText(file_name)

    def add_files(self):
        file_names, _ = QFileDialog.getOpenFileNames(self, "Select Files", "", "All Files (*)")
        for file_name in file_names:
            item = QTreeWidgetItem(self.additional_files_tree)
            item.setText(0, file_name)
            item.setText(1, "File")

            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda _, item=item: self.remove_item(item))
            self.additional_files_tree.setItemWidget(item, 2, delete_button)

    def add_folder(self):
        folder_name = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_name:
            item = QTreeWidgetItem(self.additional_files_tree)
            item.setText(0, folder_name)
            item.setText(1, "Folder")

            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda _, item=item: self.remove_item(item))
            self.additional_files_tree.setItemWidget(item, 2, delete_button)

    def add_binary(self):
        item = QTreeWidgetItem(self.additional_files_tree)
        item.setText(0, "Binary File")
        item.setText(1, "Binary")

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(lambda _, item=item: self.remove_item(item))
        self.additional_files_tree.setItemWidget(item, 2, delete_button)

    def remove_item(self, item):
        index = self.additional_files_tree.indexOfTopLevelItem(item)
        if index != -1:
            self.additional_files_tree.takeTopLevelItem(index)

    def run_pyinstaller(self):
        command = self.command_preview.toPlainText()
        if command.startswith("Error"):
            return

        self.output_console.clear()  # Clear the output console before starting
        self.pyinstaller_thread = PyInstallerThread(command)
        self.pyinstaller_thread.output_signal.connect(self.update_output_console)
        self.pyinstaller_thread.start()

    def update_output_console(self, output):
        self.output_console.append(output)
        self.output_console.verticalScrollBar().setValue(self.output_console.verticalScrollBar().maximum())

    def update_command(self):
        script = self.script_path.text()
        if not script:
            self.command_preview.setText("Error: No script selected!")
            return

        command = f'pyinstaller "{script}"'

        if self.app_name_input.text():
            command += f' --name "{self.app_name_input.text()}"'

        if self.onefile_checkbox.isChecked():
            command += " --onefile"

        if self.noconsole_checkbox.isChecked():
            command += " --windowed"

        if self.hidden_imports.text():
            hidden_imports = self.hidden_imports.text().split(',')
            for imp in hidden_imports:
                command += f' --hidden-import {imp.strip()}'

        if self.icon_path.text():
            command += f' --icon="{self.icon_path.text()}"'

        output_folder = self.output_folder_path.text()
        
        if output_folder:
            command += f' --distpath="{output_folder}"'

        for i in range(self.additional_files_tree.topLevelItemCount()):
            item = self.additional_files_tree.topLevelItem(i)
            file_path = item.text(0)
            if item.text(1) == "File":
                command += f' --add-data "{file_path};."'
            elif item.text(1) == "Folder":
                command += f' --add-data "{file_path}/*;."'
            elif item.text(1) == "Binary":
                command += f' --add-binary "{file_path};."'

        log_level = self.log_level_combo.currentText()
        if log_level:
            command += f" --log-level {log_level}"
        
        upx_dir = self.upx_path.text().strip()
        if upx_dir:
            command += f' --upx-dir "{upx_dir}"'

        debug_mode = self.debug_combo.currentText().lower()
        if debug_mode != "none":
            command += f' --debug {debug_mode}'

        if self.cmd_clean.isChecked():
            command += " --clean"

        custom_commands = self.custom_commands.text()
        if custom_commands:
            command += f' {custom_commands}'

        tmpdir = self.tmpdir_input.text().strip()
        if tmpdir:
            command += f' --runtime-tmpdir={tmpdir}'

        encryption_key = self.key_input.text().strip()
        if encryption_key:
            command += f' --key {encryption_key}'


        self.command_preview.setText(command)

    def display_versions(self):
        try:
            python_version = subprocess.check_output(["python", "--version"]).decode("utf-8").strip()
            self.python_version_label.setText(python_version)
            self.python_version_label.setStyleSheet("color: #f3db5f;margin-top: 10px;")
        except subprocess.CalledProcessError:
            self.python_version_label.setText("Python Version: Not Found")
            self.python_version_label.setStyleSheet("color: red;margin-top: 10px;")

        try:
            pyinstaller_version = subprocess.check_output(["pyinstaller", "--version"]).decode("utf-8").strip()
            self.pyinstaller_version_label.setText(f"PyInstaller Version: {pyinstaller_version}")
            self.pyinstaller_version_label.setStyleSheet("color: #4f5ca1;")
        except subprocess.CalledProcessError:
            self.pyinstaller_version_label.setText("PyInstaller Version: Not Found")
            self.pyinstaller_version_label.setStyleSheet("color: red;")