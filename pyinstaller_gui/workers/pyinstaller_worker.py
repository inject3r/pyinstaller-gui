"""PyInstaller worker thread module."""

import subprocess
import sys
from typing import List, Optional

from PyQt6.QtCore import QThread, pyqtSignal


class PyInstallerWorker(QThread):
    """
    Worker thread for executing PyInstaller in the background.
    
    This thread runs PyInstaller in a separate process (never through a
    shell) so the GUI stays responsive during the build and so paths
    containing spaces, quotes, or other shell-special characters are
    handled correctly and safely on every platform.
    
    PyInstaller is always invoked as ``<sys.executable> -m PyInstaller ...``,
    i.e. as a module of the very same Python interpreter that is running the
    GUI. This guarantees the build uses the PyInstaller that is actually
    installed for this application (matching what ``VersionChecker``
    reports), regardless of what happens to be first on PATH.
    
    stdout and stderr are merged into a single stream before being read.
    PyInstaller writes most of its progress output to stderr; reading two
    separate blocking pipes in turn (as a naive line-by-line read loop would)
    can deadlock once one of the pipe buffers fills up while the code is
    blocked reading the other. Merging the streams avoids that entirely.
    """
    
    output_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(int)
    
    def __init__(self, args: List[str], parent=None):
        """
        Initialize the PyInstaller worker thread.
        
        Args:
            args: The PyInstaller arguments (NOT including the executable
                itself), e.g. as returned by ``CommandBuilder.build_args()``.
            parent: Optional parent QObject.
        """
        super().__init__(parent)
        self.args = list(args)
        self._process: Optional[subprocess.Popen] = None
        self._stop_requested = False
    
    def run(self):
        """
        Run PyInstaller in a subprocess and stream its output.
        
        Launches ``<sys.executable> -m PyInstaller <args>`` with merged
        stdout/stderr, emitting each line via ``output_signal`` as soon as
        it is available, and finally emits ``finished_signal`` with the
        process return code (or -1 if the process could not be started, or
        it was cancelled by the user).
        """
        command = [sys.executable, "-m", "PyInstaller"] + self.args
        
        try:
            self._process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                bufsize=1,
            )
        except OSError as exc:
            self.output_signal.emit(f"Failed to start PyInstaller: {exc}\n")
            self.finished_signal.emit(-1)
            return
        
        assert self._process.stdout is not None
        for line in self._process.stdout:
            self.output_signal.emit(line)
            if self._stop_requested:
                break
        
        self._process.stdout.close()
        return_code = self._process.wait()
        
        if self._stop_requested:
            self.output_signal.emit("\nBuild cancelled by user.\n")
            return_code = -1
        
        self.finished_signal.emit(return_code)
    
    def stop(self):
        """
        Request cancellation of the running build.
        
        Terminates the underlying PyInstaller process (escalating to a
        forceful kill if it doesn't exit promptly). Safe to call even if
        the process has already finished.
        """
        self._stop_requested = True
        if self._process and self._process.poll() is None:
            try:
                self._process.terminate()
                try:
                    self._process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self._process.kill()
            except OSError:
                pass
