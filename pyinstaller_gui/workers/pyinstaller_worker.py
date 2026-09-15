"""PyInstaller worker thread module."""

import subprocess
from PyQt6.QtCore import QThread, pyqtSignal


class PyInstallerWorker(QThread):
    """
    Worker thread for executing PyInstaller commands.
    
    This thread runs PyInstaller in a separate thread to prevent the GUI
    from freezing during the build process. All output (stdout and stderr)
    is emitted via the output_signal for real-time display in the GUI.
    """
    
    output_signal = pyqtSignal(str)
    
    def __init__(self, command: str):
        """
        Initialize the PyInstaller worker thread.
        
        Args:
            command: The complete PyInstaller command string to execute.
        """
        super().__init__()
        self.command = command
    
    def run(self):
        """
        Run the PyInstaller command in a subprocess.
        
        Executes the PyInstaller command with PIPE redirection for both
        stdout and stderr. Reads output line by line and emits each line
        via output_signal for real-time display. Continues reading until
        the process completes and all output has been consumed.
        """
        process = subprocess.Popen(
            self.command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            universal_newlines=True,
            bufsize=1
        )
        
        while True:
            stdout_line = process.stdout.readline()
            stderr_line = process.stderr.readline()
            
            if stdout_line:
                self.output_signal.emit(stdout_line)
            if stderr_line:
                self.output_signal.emit(stderr_line)
            
            if not stdout_line and not stderr_line and process.poll() is not None:
                break
        
        process.stdout.close()
        process.stderr.close()
        process.wait()