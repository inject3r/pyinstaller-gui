"""Output widget for displaying command and console output."""

import re
from datetime import datetime

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QHBoxLayout, QMessageBox, QFileDialog
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QClipboard


class OutputWidget(QWidget):
    """
    Widget for displaying generated command and console output.
    
    This widget provides a real-time view of the PyInstaller command
    being executed and its console output. It includes syntax highlighting
    for commands, color-coded console output, and utility buttons for
    copying, clearing, and saving logs.
    """
    
    def __init__(self, parent=None):
        """
        Initialize the output widget.
        
        Args:
            parent: Parent widget (default: None).
        """
        super().__init__(parent)
        self.init_ui()
        self.output_history = []  # Store output history for saving
    
    def init_ui(self):
        """
        Initialize the user interface.
        
        Creates the command preview section with copy button and the
        output console section with clear, copy, and save buttons.
        Both sections use monospace fonts and custom styling for
        better readability.
        """
        layout = QVBoxLayout(self)
        layout.setSpacing(5)
        
        # Command section with buttons
        command_header = QHBoxLayout()
        self.command_preview_label = QLabel("Generated Command:")
        self.command_preview_label.setStyleSheet("font-weight: bold;")
        
        self.copy_command_button = QPushButton("Copy")
        self.copy_command_button.setFixedWidth(60)
        self.copy_command_button.setToolTip("Copy the generated command to clipboard")
        self.copy_command_button.setStyleSheet("""
            QPushButton {
                padding: 5px;
            }
        """)
        
        command_header.addWidget(self.command_preview_label)
        command_header.addStretch()
        command_header.addWidget(self.copy_command_button)
        
        self.command_preview = QTextEdit()
        self.command_preview.setReadOnly(True)
        self.command_preview.setFixedHeight(60)
        self.command_preview.setStyleSheet("""
            QTextEdit {
                font-family: 'Courier New', 'Fira Code', monospace;
                font-size: 12px;
            }
        """)
        
        # Output section with buttons
        output_header = QHBoxLayout()
        self.output_console_label = QLabel("Output Console:")
        self.output_console_label.setStyleSheet("font-weight: bold;")
        
        self.clear_output_button = QPushButton("Clear")
        self.save_output_button = QPushButton("Save Log")
        self.copy_output_button = QPushButton("Copy Log")
        
        self.clear_output_button.setFixedWidth(60)
        self.save_output_button.setFixedWidth(80)
        self.copy_output_button.setFixedWidth(80)
        
        self.clear_output_button.setToolTip("Clear the output console")
        self.save_output_button.setToolTip("Save the output console to a file")
        self.copy_output_button.setToolTip("Copy the output console content to clipboard")
        
        self.clear_output_button.setStyleSheet("""
            QPushButton {
                padding: 5px;
            }
        """)
        
        self.save_output_button.setStyleSheet("""
            QPushButton {
                padding: 5px;
            }
        """)
        
        self.copy_output_button.setStyleSheet("""
            QPushButton {
                padding: 5px;
            }
        """)
        
        output_header.addWidget(self.output_console_label)
        output_header.addStretch()
        output_header.addWidget(self.clear_output_button)
        output_header.addWidget(self.copy_output_button)
        output_header.addWidget(self.save_output_button)
        
        self.output_console = QTextEdit()
        self.output_console.setReadOnly(True)
        self.output_console.setFixedHeight(120)
        self.output_console.setStyleSheet("""
            QTextEdit {
                font-family: 'Courier New', 'Fira Code', monospace;
                font-size: 12px;
            }
        """)
        
        layout.addLayout(command_header)
        layout.addWidget(self.command_preview)
        layout.addLayout(output_header)
        layout.addWidget(self.output_console)
        
        # Connect signals
        self.copy_command_button.clicked.connect(self.copy_command_to_clipboard)
        self.clear_output_button.clicked.connect(self.clear_output)
        self.save_output_button.clicked.connect(self.save_output_to_file)
        self.copy_output_button.clicked.connect(self.copy_output_to_clipboard)
    
    def set_command_text(self, text: str):
        """
        Set the command preview text with syntax highlighting.
        
        Args:
            text: The PyInstaller command string to display.
        
        If the text starts with "Error", it is displayed in red.
        Otherwise, syntax highlighting is applied.
        """
        if text.startswith("Error"):
            self.command_preview.setHtml(f'<span style="color: #DC3545; font-weight: bold;">{text}</span>')
        else:
            highlighted_text = self.highlight_command(text)
            self.command_preview.setHtml(highlighted_text)
    
    def get_command_text(self) -> str:
        """
        Get the command preview text.
        
        Returns:
            The plain text content of the command preview.
        """
        return self.command_preview.toPlainText()
    
    def copy_command_to_clipboard(self):
        """
        Copy the generated command to clipboard.
        
        Shows a success message if the command is valid and non-empty,
        or a warning message if there's nothing to copy.
        """
        command = self.command_preview.toPlainText()
        if command and not command.startswith("Error"):
            clipboard = QApplication.clipboard()
            clipboard.setText(command)
            QMessageBox.information(self, "Copied", "Command copied to clipboard!")
        elif command.startswith("Error"):
            QMessageBox.warning(self, "Nothing to Copy", "No valid command to copy!")
        else:
            QMessageBox.warning(self, "Nothing to Copy", "Command is empty!")
    
    def copy_output_to_clipboard(self):
        """
        Copy the output console content to clipboard.
        
        Shows a success message if there is output content,
        or a warning message if the console is empty.
        """
        output = self.output_console.toPlainText()
        if output:
            clipboard = QApplication.clipboard()
            clipboard.setText(output)
            QMessageBox.information(self, "Copied", "Output log copied to clipboard!")
        else:
            QMessageBox.warning(self, "Nothing to Copy", "Output console is empty!")
    
    def save_output_to_file(self):
        """
        Save the output console content to a file.
        
        Opens a file save dialog with a timestamped default filename.
        Writes the build log including header information, the generated
        command, and the console output. Shows success or error messages
        based on the outcome.
        """
        output = self.output_console.toPlainText()
        if not output:
            QMessageBox.warning(self, "Nothing to Save", "Output console is empty!")
            return
        
        # Generate default filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"pyinstaller_output_{timestamp}.log"
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Output Log",
            default_filename,
            "Log Files (*.log);;Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    # Write header
                    f.write("=" * 60 + "\n")
                    f.write(f"PyInstaller GUI Build Log\n")
                    f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("=" * 60 + "\n\n")
                    
                    # Write command if exists
                    command = self.command_preview.toPlainText()
                    if command and not command.startswith("Error"):
                        f.write("GENERATED COMMAND:\n")
                        f.write("-" * 40 + "\n")
                        f.write(command + "\n\n")
                    
                    # Write output
                    f.write("BUILD OUTPUT:\n")
                    f.write("-" * 40 + "\n")
                    f.write(output + "\n")
                    
                    f.write("=" * 60 + "\n")
                
                QMessageBox.information(
                    self, 
                    "Save Successful", 
                    f"Output log saved to:\n{file_path}"
                )
            except Exception as e:
                QMessageBox.critical(
                    self, 
                    "Save Failed", 
                    f"Failed to save output log:\n{str(e)}"
                )
    
    def highlight_command(self, command: str) -> str:
        """
        Highlight PyInstaller command syntax.
        
        Applies color coding to different elements of the PyInstaller command:
        - pyinstaller command: Purple
        - Flags (--onefile, -F, etc.): Blue
        - Options (--name, --distpath, etc.): Green
        - Strings and paths: Orange
        - File extensions: Orange bold
        
        Args:
            command: The raw command string to highlight.
            
        Returns:
            HTML-formatted string with color-coded syntax highlighting.
        """
        # Colors (will be adapted to theme)
        flag_color = "#2D8FBA"
        option_color = "#28A745"
        string_color = "#FFA500"
        command_color = "#6F42C1"
        
        # Escape HTML
        command = command.replace("&", "&amp;")
        command = command.replace("<", "&lt;")
        command = command.replace(">", "&gt;")
        
        # Highlight pyinstaller command
        command = command.replace("pyinstaller", f'<span style="color: {command_color}; font-weight: bold;">pyinstaller</span>')
        
        # Flags
        flags = [
            '--onefile', '-F', '--onedir', '-D', '--windowed', '-w',
            '--noconsole', '--console', '-c', '--clean', '--noupx',
            '--strip', '-s', '--uac-admin', '--uac-uiaccess',
            '--argv-emulation', '--disable-windowed-traceback',
            '--bootloader-ignore-signals',
        ]
        
        for flag in flags:
            command = command.replace(flag, f'<span style="color: {flag_color}; font-weight: bold;">{flag}</span>')
        
        # Options
        options = [
            '--name', '-n', '--distpath', '--workpath', '--specpath',
            '--add-data', '--add-binary', '--hidden-import', '--hiddenimport',
            '--exclude-module', '--icon', '-i', '--upx-dir', '--runtime-tmpdir',
            '--log-level', '--debug', '-d', '--optimize', '-O', '--python-option',
            '--version-file', '--manifest', '--resource', '-r', '--key',
        ]
        
        for option in options:
            command = command.replace(option, f'<span style="color: {option_color}; font-weight: bold;">{option}</span>')
        
        # Highlight quoted strings
        command = re.sub(r'"(.*?)"', f'<span style="color: {string_color};">"\\1"</span>', command)
        command = re.sub(r"\'(.*?)\'", f"<span style='color: {string_color};'>'\\1'</span>", command)
        
        # Highlight paths
        command = re.sub(r'([a-zA-Z]:)?[\/][\w\-.\\\/]+', f'<span style="color: {string_color};">\\g<0></span>', command)
        
        # Highlight extensions
        for ext in ['.py', '.ico', '.icns', '.exe', '.dll', '.so', '.dylib']:
            command = command.replace(ext, f'<span style="color: {string_color}; font-weight: bold;">{ext}</span>')
        
        return f'<div style="font-family: \'Courier New\', monospace; font-size: 12px; line-height: 1.4;">{command}</div>'
    
    def append_output(self, text: str):
        """
        Append text to the output console with highlighting.
        
        Colors the output based on content type:
        - Errors/failures/exceptions: Red
        - Warnings: Yellow
        - Success/completed messages: Green
        
        Also stores plain text for saving and auto-scrolls to the bottom.
        
        Args:
            text: The output line to append.
        """
        # Store plain text for saving
        self.output_history.append(text)
        
        # Remove HTML from existing text
        text = text.replace("&", "&amp;")
        text = text.replace("<", "&lt;")
        text = text.replace(">", "&gt;")
        
        # Highlight based on content
        if "error" in text.lower() or "failed" in text.lower() or "exception" in text.lower():
            text = f'<span style="color: #DC3545;">{text}</span>'
        elif "warning" in text.lower():
            text = f'<span style="color: #FFC107;">{text}</span>'
        elif "success" in text.lower() or "completed" in text.lower():
            text = f'<span style="color: #28A745;">{text}</span>'
        
        self.output_console.append(text)
        scrollbar = self.output_console.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def clear_output(self):
        """Clear the output console and reset the output history."""
        self.output_console.clear()
        self.output_history.clear()
    
    def clear_command(self):
        """Clear the command preview."""
        self.command_preview.clear()
    
    def get_output_text(self) -> str:
        """
        Get the plain text of output console.
        
        Returns:
            The plain text content of the output console.
        """
        return self.output_console.toPlainText()