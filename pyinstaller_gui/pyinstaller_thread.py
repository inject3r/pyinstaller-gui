import subprocess
from PyQt6.QtCore import QThread, pyqtSignal

# This thread is responsible for executing the PyInstaller command in a separate thread to avoid freezing the GUI.
class PyInstallerThread(QThread):
    # Signal to pass output (both stdout and stderr) back to the main GUI thread.
    output_signal = pyqtSignal(str)

    def __init__(self, command):
        """
        Initializes the PyInstallerThread with the given command to be executed.
        
        Args:
        - command (str): The command that will be run using subprocess.
        """
        super().__init__()
        self.command = command

    def run(self):
        """
        Runs the PyInstaller command in a subprocess. Captures the output and emits it back to the main thread.
        """
        process = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, universal_newlines=True)

        # Continuously read the stdout and stderr of the process
        while True:
            stdout_line = process.stdout.readline()
            stderr_line = process.stderr.readline()

            # If there is data in stdout, emit it to the GUI
            if stdout_line:
                self.output_signal.emit(stdout_line)
            # If there is data in stderr, emit it to the GUI
            if stderr_line:
                self.output_signal.emit(stderr_line)

            # Break the loop when the process finishes and there is no more output
            if not stdout_line and not stderr_line and process.poll() is not None:
                break

        process.stdout.close()
        process.stderr.close()
        process.wait()
