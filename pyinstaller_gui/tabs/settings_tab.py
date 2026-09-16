"""Settings configuration tab."""

from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, 
    QFileDialog, QMessageBox, QGroupBox, QFormLayout, QComboBox, QCheckBox
)
from PyQt6.QtCore import pyqtSignal

from .base_tab import BaseTab


class SettingsTab(BaseTab):
    """
    Tab for output, layout, and platform-specific settings.
    
    This tab allows users to configure:
    - Output folder location and custom icon for the executable
    - Runtime temporary directory for onefile mode extraction
    - Where PyInstaller stores the generated .spec file and work files
    - Windows-only packaging options (version info, manifest, UAC, console visibility)
    - macOS-only packaging options (argv emulation, bundle id, architecture, code signing)
    - Additional custom PyInstaller command-line arguments
    """
    
    output_folder_changed = pyqtSignal(str)
    custom_commands_changed = pyqtSignal(str)
    icon_path_changed = pyqtSignal(str)
    tmpdir_changed = pyqtSignal(str)
    specpath_changed = pyqtSignal(str)
    workpath_changed = pyqtSignal(str)
    console_explicit_changed = pyqtSignal(bool)
    hide_console_changed = pyqtSignal(str)
    disable_windowed_traceback_changed = pyqtSignal(bool)
    version_file_changed = pyqtSignal(str)
    manifest_file_changed = pyqtSignal(str)
    uac_admin_changed = pyqtSignal(bool)
    uac_uiaccess_changed = pyqtSignal(bool)
    argv_emulation_changed = pyqtSignal(bool)
    osx_bundle_identifier_changed = pyqtSignal(str)
    target_arch_changed = pyqtSignal(str)
    codesign_identity_changed = pyqtSignal(str)
    osx_entitlements_file_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        """
        Initialize the settings tab.
        
        Args:
            parent: Parent widget (default: None).
        """
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """
        Initialize the user interface.
        
        Creates the header with help button, then arranges output/layout
        controls, a Windows-only options group, a macOS-only options group,
        and the custom commands input.
        """
        # Help button in header
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 5)
        
        header_label = QLabel("Output Settings")
        header_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        
        self.settings_help_button = QPushButton("?")
        self.settings_help_button.setFixedSize(24, 24)
        self.settings_help_button.setToolTip("Show help for Output settings")
        self.settings_help_button.setStyleSheet("""
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
        header_layout.addWidget(self.settings_help_button)
        
        self.main_layout.addWidget(header_widget)
        
        # Output folder
        self.output_folder_label = QLabel("Select Output Folder:")
        self.output_folder_label.setToolTip("Where the built executable will be saved")
        
        self.output_folder_path = QLineEdit()
        self.output_folder_path.setPlaceholderText("Setting the program output location")
        self.output_folder_path.setToolTip("Default: ./dist folder in the current directory")
        
        self.output_folder_button = QPushButton("Browse Output Folder")
        self.output_folder_button.setToolTip("Select directory for the output executable")
        
        folder_layout = QHBoxLayout()
        folder_layout.addWidget(self.output_folder_path)
        folder_layout.addWidget(self.output_folder_button)
        
        # Icon
        self.icon_label = QLabel("Icon File:")
        self.icon_label.setToolTip("Custom icon for your executable file")
        
        self.icon_path = QLineEdit()
        self.icon_path.setPlaceholderText("Icon File (.ico for Windows, .icns for Mac)")
        self.icon_path.setToolTip(
            "Windows: .ico file\n"
            "macOS: .icns file\n"
            "Leave empty for default PyInstaller icon"
        )
        
        self.browse_icon_button = QPushButton("Browse Icon")
        self.browse_icon_button.setToolTip("Select icon file")
        
        icon_layout = QHBoxLayout()
        icon_layout.addWidget(self.icon_path)
        icon_layout.addWidget(self.browse_icon_button)
        
        # Temporary directory
        self.tmpdir_label = QLabel("Runtime Tmpdir:")
        self.tmpdir_label.setToolTip("Custom temporary directory for onefile mode")
        
        self.tmpdir_input = QLineEdit()
        self.tmpdir_input.setPlaceholderText("Specify a temp directory to boost performance")
        self.tmpdir_input.setToolTip(
            "For onefile mode, files are extracted to this directory.\n"
            "Use a RAM disk for faster performance."
        )
        
        self.main_layout.addWidget(self.output_folder_label)
        self.main_layout.addLayout(folder_layout)
        self.main_layout.addWidget(self.icon_label)
        self.main_layout.addLayout(icon_layout)
        self.main_layout.addWidget(self.tmpdir_label)
        self.main_layout.addWidget(self.tmpdir_input)
        
        # --- Build layout ---
        layout_group = QGroupBox("Build Layout")
        layout_form = QFormLayout()
        
        self.specpath_input = QLineEdit()
        self.specpath_input.setPlaceholderText("Folder to store the generated .spec file (default: current directory)")
        self.specpath_input.setToolTip("Equivalent to --specpath")
        self.specpath_button = QPushButton("Browse")
        specpath_row = QHBoxLayout()
        specpath_row.addWidget(self.specpath_input)
        specpath_row.addWidget(self.specpath_button)
        layout_form.addRow("Spec File Folder:", specpath_row)
        
        self.workpath_input = QLineEdit()
        self.workpath_input.setPlaceholderText("Folder for temporary work files (default: ./build)")
        self.workpath_input.setToolTip("Equivalent to --workpath")
        self.workpath_button = QPushButton("Browse")
        workpath_row = QHBoxLayout()
        workpath_row.addWidget(self.workpath_input)
        workpath_row.addWidget(self.workpath_button)
        layout_form.addRow("Work Folder:", workpath_row)
        
        layout_group.setLayout(layout_form)
        self.main_layout.addWidget(layout_group)
        
        # --- Windows-only options ---
        windows_group = QGroupBox("Windows Options")
        windows_group.setToolTip("These options only take effect when building on Windows.")
        windows_form = QFormLayout()
        
        self.console_mode_combo = QComboBox()
        self.console_mode_combo.addItems(["Default", "Force Console (--console)"])
        self.console_mode_combo.setToolTip(
            "PyInstaller defaults to a console window unless \"No Console\" is\n"
            "checked in the General tab. Force this explicitly if needed."
        )
        windows_form.addRow("Console Mode:", self.console_mode_combo)
        
        self.hide_console_combo = QComboBox()
        self.hide_console_combo.addItems(
            ["none", "minimize-early", "minimize-late", "hide-early", "hide-late"]
        )
        self.hide_console_combo.setToolTip(
            "Equivalent to --hide-console. Automatically hide/minimize the\n"
            "console window once the app owns it (console-enabled builds only)."
        )
        windows_form.addRow("Hide Console:", self.hide_console_combo)
        
        self.cmd_disable_traceback = QCheckBox("--disable-windowed-traceback")
        self.cmd_disable_traceback.setToolTip("Disable the windowed-mode unhandled-exception traceback dialog.")
        windows_form.addRow("", self.cmd_disable_traceback)
        
        self.version_file_input = QLineEdit()
        self.version_file_input.setPlaceholderText("Windows version-info resource file")
        self.version_file_button = QPushButton("Browse")
        version_file_row = QHBoxLayout()
        version_file_row.addWidget(self.version_file_input)
        version_file_row.addWidget(self.version_file_button)
        windows_form.addRow("Version File:", version_file_row)
        
        self.manifest_input = QLineEdit()
        self.manifest_input.setPlaceholderText("Manifest file or inline XML")
        self.manifest_button = QPushButton("Browse")
        manifest_row = QHBoxLayout()
        manifest_row.addWidget(self.manifest_input)
        manifest_row.addWidget(self.manifest_button)
        windows_form.addRow("Manifest:", manifest_row)
        
        self.cmd_uac_admin = QCheckBox("--uac-admin (Request elevation on start)")
        windows_form.addRow("", self.cmd_uac_admin)
        
        self.cmd_uac_uiaccess = QCheckBox("--uac-uiaccess (Allow elevated app with Remote Desktop)")
        windows_form.addRow("", self.cmd_uac_uiaccess)
        
        windows_group.setLayout(windows_form)
        self.main_layout.addWidget(windows_group)
        
        # --- macOS-only options ---
        macos_group = QGroupBox("macOS Options")
        macos_group.setToolTip("These options only take effect when building on macOS.")
        macos_form = QFormLayout()
        
        self.cmd_argv_emulation = QCheckBox("--argv-emulation (open document/URL events -> sys.argv)")
        macos_form.addRow("", self.cmd_argv_emulation)
        
        self.bundle_id_input = QLineEdit()
        self.bundle_id_input.setPlaceholderText("com.mycompany.department.appname")
        macos_form.addRow("Bundle Identifier:", self.bundle_id_input)
        
        self.target_arch_combo = QComboBox()
        self.target_arch_combo.addItems(["(current)", "x86_64", "arm64", "universal2"])
        self.target_arch_combo.setToolTip("Equivalent to --target-architecture")
        macos_form.addRow("Target Architecture:", self.target_arch_combo)
        
        self.codesign_identity_input = QLineEdit()
        self.codesign_identity_input.setPlaceholderText("Code signing identity (blank = ad-hoc signing)")
        macos_form.addRow("Codesign Identity:", self.codesign_identity_input)
        
        self.entitlements_input = QLineEdit()
        self.entitlements_input.setPlaceholderText("Entitlements file used when code-signing")
        self.entitlements_button = QPushButton("Browse")
        entitlements_row = QHBoxLayout()
        entitlements_row.addWidget(self.entitlements_input)
        entitlements_row.addWidget(self.entitlements_button)
        macos_form.addRow("Entitlements File:", entitlements_row)
        
        macos_group.setLayout(macos_form)
        self.main_layout.addWidget(macos_group)
        
        # Custom commands
        self.custom_commands_label = QLabel("Custom Commands:")
        self.custom_commands_label.setToolTip("Additional PyInstaller arguments")
        
        self.custom_commands = QLineEdit()
        self.custom_commands.setPlaceholderText("Enter additional commands here")
        self.custom_commands.setToolTip(
            "Example: --optimize 2 --noupx\n"
            "Add any PyInstaller option not covered by the GUI.\n"
            "Applied last, so it can override anything above."
        )
        
        self.main_layout.addWidget(self.custom_commands_label)
        self.main_layout.addWidget(self.custom_commands)
        self.main_layout.addStretch()
        
        # Connect signals
        self.output_folder_button.clicked.connect(self.browse_output_folder)
        self.output_folder_path.textChanged.connect(self.output_folder_changed.emit)
        self.browse_icon_button.clicked.connect(self.browse_icon)
        self.icon_path.textChanged.connect(self.icon_path_changed.emit)
        self.tmpdir_input.textChanged.connect(self.tmpdir_changed.emit)
        
        self.specpath_button.clicked.connect(lambda: self._browse_dir_into(self.specpath_input))
        self.specpath_input.textChanged.connect(self.specpath_changed.emit)
        self.workpath_button.clicked.connect(lambda: self._browse_dir_into(self.workpath_input))
        self.workpath_input.textChanged.connect(self.workpath_changed.emit)
        
        self.console_mode_combo.currentIndexChanged.connect(
            lambda idx: self.console_explicit_changed.emit(idx == 1)
        )
        self.hide_console_combo.currentTextChanged.connect(self.hide_console_changed.emit)
        self.cmd_disable_traceback.toggled.connect(self.disable_windowed_traceback_changed.emit)
        self.version_file_button.clicked.connect(lambda: self._browse_file_into(self.version_file_input, "All Files (*)"))
        self.version_file_input.textChanged.connect(self.version_file_changed.emit)
        self.manifest_button.clicked.connect(lambda: self._browse_file_into(self.manifest_input, "Manifest Files (*.manifest *.xml);;All Files (*)"))
        self.manifest_input.textChanged.connect(self.manifest_file_changed.emit)
        self.cmd_uac_admin.toggled.connect(self.uac_admin_changed.emit)
        self.cmd_uac_uiaccess.toggled.connect(self.uac_uiaccess_changed.emit)
        
        self.cmd_argv_emulation.toggled.connect(self.argv_emulation_changed.emit)
        self.bundle_id_input.textChanged.connect(self.osx_bundle_identifier_changed.emit)
        self.target_arch_combo.currentTextChanged.connect(self._on_target_arch_changed)
        self.codesign_identity_input.textChanged.connect(self.codesign_identity_changed.emit)
        self.entitlements_button.clicked.connect(lambda: self._browse_file_into(self.entitlements_input, "Entitlements (*.plist *.entitlements);;All Files (*)"))
        self.entitlements_input.textChanged.connect(self.osx_entitlements_file_changed.emit)
        
        self.custom_commands.textChanged.connect(self.custom_commands_changed.emit)
        self.settings_help_button.clicked.connect(self.show_help)
    
    def _browse_dir_into(self, line_edit: QLineEdit):
        """
        Open a directory dialog and write the result into a line edit.
        
        Args:
            line_edit: The QLineEdit to populate with the chosen directory.
        """
        dir_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if dir_path:
            line_edit.setText(dir_path)
    
    def _browse_file_into(self, line_edit: QLineEdit, file_filter: str):
        """
        Open a file dialog and write the result into a line edit.
        
        Args:
            line_edit: The QLineEdit to populate with the chosen file path.
            file_filter: The Qt file dialog filter string to use.
        """
        file_name, _ = QFileDialog.getOpenFileName(self, "Select File", "", file_filter)
        if file_name:
            line_edit.setText(file_name)
    
    def _on_target_arch_changed(self, text: str):
        """
        Forward the selected macOS target architecture, translating the placeholder.
        
        Args:
            text: The combo box text ("(current)", "x86_64", "arm64", or "universal2").
        """
        self.target_arch_changed.emit("" if text == "(current)" else text)
    
    def browse_output_folder(self):
        """
        Open directory dialog to select output folder.
        
        Updates the output folder path field with the selected directory.
        """
        folder_name = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder_name:
            self.output_folder_path.setText(folder_name)
    
    def browse_icon(self):
        """
        Open file dialog to select icon file.
        
        Filters for .ico (Windows) and .icns (macOS) icon files.
        Updates the icon path field with the selected file.
        """
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Icon", "", "Icon Files (*.ico *.icns)"
        )
        if file_name:
            self.icon_path.setText(file_name)
    
    def show_help(self):
        """
        Show help dialog for Settings tab.
        
        Displays a message box with detailed explanations of each setting,
        including the newer build-layout and platform-specific groups.
        """
        help_text = """
        <h3>Output Settings Help</h3>
        
        <b>Output Folder:</b><br>
        Directory where the built executable will be saved.<br>
        Default is the 'dist' folder in the current directory.<br><br>
        
        <b>Icon File:</b><br>
        Custom icon for your executable.<br>
        - Windows: Use .ico files<br>
        - macOS: Use .icns files<br>
        - Linux: Icon support varies by desktop environment<br><br>
        
        <b>Runtime Tmpdir:</b><br>
        For onefile mode, the bootloader extracts files to this directory.<br>
        Using a RAM disk (e.g., /dev/shm on Linux) can improve performance.<br><br>
        
        <b>Build Layout:</b><br>
        Spec File Folder and Work Folder control where PyInstaller writes
        its generated .spec file and intermediate build artifacts.<br><br>
        
        <b>Windows Options:</b><br>
        Console Mode/Hide Console control the console window's visibility.
        Version File and Manifest embed Windows resources into the exe.
        UAC options request elevated privileges on launch. These only have
        an effect when the build itself runs on Windows.<br><br>
        
        <b>macOS Options:</b><br>
        Argv Emulation routes open-document/URL events into sys.argv.
        Bundle Identifier and Target Architecture control the generated
        .app bundle. Codesign Identity/Entitlements are used for code
        signing. These only have an effect when the build itself runs on
        macOS.<br><br>
        
        <b>Custom Commands:</b><br>
        Add any PyInstaller option not covered by the GUI.
        Example: --optimize 2 --noupx --noconfirm
        """
        
        QMessageBox.information(self, "Output Settings Help", help_text)
