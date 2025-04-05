import sys
from PyQt6.QtWidgets import QApplication
from .gui import PyInstallerGUI 

def run():
    app = QApplication(sys.argv)
    window = PyInstallerGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    run()