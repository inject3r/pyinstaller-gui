"""Output widget for displaying command and console output."""

import re
import shlex
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
    
    # Recognized flags (no argument) and options (take a value), used by the
    # tokenizing highlighter below.
    _HIGHLIGHT_FLAGS = {
        '--onefile', '-F', '--onedir', '-D', '--windowed', '-w',
        '--noconsole', '--console', '-c', '--clean', '--noupx',
        '--strip', '-s', '--uac-admin', '--uac-uiaccess',
        '--argv-emulation', '--disable-windowed-traceback',
        '--bootloader-ignore-signals', '--noconfirm', '-y',
    }
    _HIGHLIGHT_OPTIONS = {
        '--name', '-n', '--distpath', '--workpath', '--specpath',
        '--add-data', '--add-binary', '--hidden-import', '--hiddenimport',
        '--exclude-module', '--icon', '-i', '--upx-dir', '--upx-exclude',
        '--runtime-tmpdir', '--log-level', '--debug', '-d', '--optimize',
        '-O', '--python-option', '--version-file', '--manifest',
        '--resource', '-r', '--key', '--paths', '-p', '--collect-all',
        '--collect-submodules', '--collect-data', '--collect-binaries',
        '--copy-metadata', '--recursive-copy-metadata',
        '--additional-hooks-dir', '--runtime-hook', '--splash',
        '--contents-directory', '--hide-console', '--osx-bundle-identifier',
        '--target-architecture', '--codesign-identity',
        '--osx-entitlements-file',
    }
    _HIGHLIGHT_EXTENSIONS = ('.py', '.pyw', '.ico', '.icns', '.exe', '.dll', '.so', '.dylib', '.png', '.jpg')

    @staticmethod
    def _escape_html(text: str) -> str:
        """
        Escape a plain-text fragment for safe embedding in Qt rich text.
        
        Args:
            text: Raw, unescaped text.
        
        Returns:
            Text with &, <, and > replaced by their HTML entities.
        """
        return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    
    def highlight_command(self, command: str) -> str:
        """
        Highlight PyInstaller command syntax.
        
        Applies color coding to different elements of the PyInstaller command:
        - pyinstaller command: Purple
        - Flags (--onefile, -F, etc.): Blue
        - Options (--name, --distpath, etc.): Green
        - Quoted strings/paths: Orange (with file extensions bolded)
        
        The command is first tokenized (respecting quoted substrings, and
        without touching backslashes so Windows paths survive intact), and
        each token is classified and wrapped in its own HTML span exactly
        once. This avoids the classic bug of running repeated plain
        substring replacements on text that already contains previously
        inserted HTML, which can match fragments of earlier markup (e.g. a
        naive replace of the short flag "-w" also matches inside the CSS
        text "font-weight" of a span inserted moments before) and corrupt
        the whole preview.
        
        Args:
            command: The raw command string to highlight.
            
        Returns:
            HTML-formatted string with color-coded syntax highlighting.
        """
        flag_color = "#2D8FBA"
        option_color = "#28A745"
        string_color = "#FFA500"
        command_color = "#6F42C1"
        
        try:
            tokens = shlex.split(command, posix=False)
        except ValueError:
            # Unbalanced quotes (e.g. while the user is still typing in the
            # custom commands field) - fall back to a naive whitespace split
            # rather than raising out of the UI.
            tokens = command.split()
        
        rendered_tokens = []
        for index, token in enumerate(tokens):
            # Some options are emitted as a single "--flag=value" token
            # (no space) rather than two separate tokens. Split that off
            # first so the option and its quoted value are still colored
            # independently, without re-scanning already-rendered HTML.
            eq_match = re.match(r'^(--[A-Za-z0-9-]+)=(.*)$', token) if token.startswith('--') else None
            if eq_match:
                flag_part, value_part = eq_match.group(1), eq_match.group(2)
                flag_html = self._render_plain_token(flag_part, flag_color, option_color, command_color, is_first=False)
                value_html = self._render_value_token(value_part, string_color)
                rendered_tokens.append(f'{flag_html}=<wbr>{value_html}')
                continue
            
            is_quoted = len(token) >= 2 and token[0] in ('"', "'") and token[-1] == token[0]
            if is_quoted:
                rendered_tokens.append(self._render_value_token(token, string_color))
            else:
                rendered_tokens.append(
                    self._render_plain_token(token, flag_color, option_color, command_color, is_first=(index == 0))
                )
        
        joined = " ".join(rendered_tokens)
        return f'<div style="font-family: \'Courier New\', monospace; font-size: 12px; line-height: 1.4;">{joined}</div>'
    
    def _render_plain_token(self, token: str, flag_color: str, option_color: str, command_color: str, is_first: bool) -> str:
        """
        Render a single non-quoted token (the "pyinstaller" command itself,
        a flag, an option, or plain unrecognized text) as one HTML span.
        
        Args:
            token: The raw, unescaped token text.
            flag_color: Hex color for boolean flags (e.g. --onefile).
            option_color: Hex color for value-taking options (e.g. --name).
            command_color: Hex color for the leading "pyinstaller" token.
            is_first: True if this is the first token in the command.
        
        Returns:
            An HTML span (or plain escaped text) for this token.
        """
        escaped = self._escape_html(token)
        if is_first and token == "pyinstaller":
            return f'<span style="color: {command_color}; font-weight: bold;">{escaped}</span>'
        if token in self._HIGHLIGHT_FLAGS:
            return f'<span style="color: {flag_color}; font-weight: bold;">{escaped}</span>'
        if token in self._HIGHLIGHT_OPTIONS:
            return f'<span style="color: {option_color}; font-weight: bold;">{escaped}</span>'
        return escaped
    
    def _render_value_token(self, token: str, string_color: str) -> str:
        """
        Render a single quoted value token (a path, name, or other string
        argument) as one HTML span, bolding a trailing recognized file
        extension if present.
        
        Args:
            token: The raw, unescaped token text, including its surrounding
                quote characters if any.
            string_color: Hex color for string/path values.
        
        Returns:
            An HTML span for this token.
        """
        is_quoted = len(token) >= 2 and token[0] in ('"', "'") and token[-1] == token[0]
        quote_char = token[0] if is_quoted else ""
        inner = token[1:-1] if is_quoted else token
        
        escaped_inner = self._escape_html(inner)
        lower_inner = inner.lower()
        matched_ext = next((ext for ext in self._HIGHLIGHT_EXTENSIONS if lower_inner.endswith(ext)), None)
        if matched_ext:
            split_at = len(escaped_inner) - len(matched_ext)
            escaped_inner = (
                escaped_inner[:split_at]
                + f'<span style="font-weight: bold;">{escaped_inner[split_at:]}</span>'
            )
        return f'<span style="color: {string_color};">{quote_char}{escaped_inner}{quote_char}</span>'
    
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