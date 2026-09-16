"""Tests for OutputWidget's command syntax highlighting.

These guard against a real, previously-shipped bug: the old highlighter
ran repeated plain str.replace() passes directly on text that already
contained previously-inserted HTML. Because the CSS text "font-weight:
bold;" is present in literally every inserted span, and "-w" (the short
flag for --windowed) was one of the strings being replaced, every command
preview containing more than one highlighted element got its HTML spans
torn apart mid-attribute wherever "-w" occurred - which is to say, almost
always. These tests exercise that exact scenario and assert on the
round-tripped plain text, which is what actually reaches the user (the
"Copy" button and the pre-fix, HTML-scraping execution path both relied
on it).
"""

import sys
import unittest

from PyQt6.QtWidgets import QApplication

from pyinstaller_gui.widgets.output_widget import OutputWidget


def _ensure_qapplication():
    """Ensure a QApplication instance exists (QTextEdit needs a GUI app)."""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    return app


class TestOutputWidgetHighlighting(unittest.TestCase):
    """Regression tests for CommandBuilder-generated command highlighting."""

    @classmethod
    def setUpClass(cls):
        """Create a (headless-safe) QApplication once for this test class."""
        cls.app = _ensure_qapplication()

    def setUp(self):
        """Create a fresh OutputWidget for each test."""
        self.widget = OutputWidget()

    def test_windowed_flag_does_not_corrupt_preceding_span(self):
        """--windowed's short form is a known trigger: '-w' is a substring
        of the CSS text 'font-weight' used in every previously-inserted
        span. The rendered plain text must exactly match the input."""
        command = 'pyinstaller "/tmp/app.py" --name "App" --onefile --windowed'
        self.widget.set_command_text(command)
        self.assertEqual(self.widget.get_command_text(), command)

    def test_roundtrip_fidelity_for_complex_command(self):
        """A command exercising many highlighted categories at once must
        still come back out exactly as it went in."""
        command = (
            'pyinstaller "/tmp/x.py" --name "My App" --onefile --windowed '
            '--icon="/some/path/icon.ico" --distpath="/out" '
            '--add-data "/tmp/data.txt:." --collect-all requests '
            '--log-level INFO --noupx --uac-admin'
        )
        self.widget.set_command_text(command)
        self.assertEqual(self.widget.get_command_text(), command)

    def test_no_leftover_span_tags_in_plain_text(self):
        """The bug manifested as literal '</span>' and CSS fragments
        leaking into the visible text; make sure none remain."""
        command = 'pyinstaller "/tmp/app.py" --name "App" --onefile --windowed --strip --clean'
        self.widget.set_command_text(command)
        plain = self.widget.get_command_text()
        self.assertNotIn("span>", plain)
        self.assertNotIn("font-weight", plain)
        self.assertNotIn("color:", plain)

    def test_error_message_still_shown_plainly(self):
        """An error string should still pass through readably, not be tokenized."""
        self.widget.set_command_text("Error: No script selected!")
        self.assertIn("No script selected", self.widget.get_command_text())

    def test_windows_path_backslashes_preserved(self):
        """Windows-style paths with backslashes must survive highlighting
        unchanged (no shlex posix-mode escape interpretation)."""
        command = r'pyinstaller "C:\Users\name\script.py" --onefile --windowed'
        self.widget.set_command_text(command)
        self.assertEqual(self.widget.get_command_text(), command)


if __name__ == "__main__":
    unittest.main()
