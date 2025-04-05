STYLE_SHEET = """
    * {
        font-family: 'Fira Code', monospace;
        font-size: 14px;
        color: #F8F8F2;
    }

    QWidget {
        background-color: #282A36;
    }

    QPushButton {
        background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #BD93F9, stop:1 #6272A4);
        border-radius: 8px;
        padding: 10px 20px;
        border: 2px solid #BD93F9;
        font-weight: bold;
        letter-spacing: 1px;
        text-transform: uppercase;
        transition: all 0.2s ease-in-out;
        box-shadow: 0px 4px 8px rgba(189, 147, 249, 0.3);
    }
    QPushButton:hover {
        background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #FF79C6, stop:1 #BD93F9);
        border: 2px solid #FF79C6;
        box-shadow: 0px 6px 12px rgba(255, 121, 198, 0.5);
        transform: scale(1.05);
    }
    QPushButton:pressed {
        background: #FF5555;
        transform: scale(0.95);
    }

    QLineEdit, QTextEdit, QComboBox {
        background-color: #44475A;
        border: 2px solid #6272A4;
        border-radius: 6px;
        padding: 8px;
        selection-background-color: #FF79C6;
        transition: border 0.3s ease-in-out;
    }
    QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
        border: 2px solid #FF79C6;
        box-shadow: 0px 0px 8px rgba(255, 121, 198, 0.8);
    }

    QCheckBox {
        spacing: 6px;
    }
    QCheckBox::indicator {
        width: 16px;
        height: 16px;
        border-radius: 4px;
        border: 2px solid #BD93F9;
        background: #44475A;
        transition: all 0.3s ease-in-out;
    }
    QCheckBox::indicator:checked {
        background: #FF79C6;
        border: 2px solid #FF5555;
        box-shadow: 0px 0px 6px rgba(255, 85, 85, 0.8);
    }

    QLabel {
        font-size: 14px;
        font-weight: bold;
        color: #F8F8F2;
    }

    QTextEdit {
        background-color: #44475A;
        border: 2px solid #6272A4;
        border-radius: 6px;
    }
    QTextEdit:read-only {
        background-color: #343746;
    }

    QGroupBox {
        border: 2px solid #6272A4;
        border-radius: 6px;
        padding: 10px;
        margin-top: 10px;
        background-color: rgba(68, 71, 90, 0.5);
    }
    QGroupBox:title {
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 3px 6px;
        background-color: #BD93F9;
        color: white;
        font-size: 14px;
        font-weight: bold;
        border-radius: 6px;
    }
"""

GITHUB_BUTTON_STYLE = """
    background-color: #FF79C6;
    color: #F8F8F2;
    font-weight: bold;
    border-radius: 8px;
    padding: 5px;
    max-width: 150px;
    height: 20px;
    margin-bottom: 10px;
"""

PROJECT_NAME_STYLE = """
    font-size: 25px;
    font-weight: bold;
    color: #BD93F9;
    text-align: center;
"""

PROJECT_VERSION_STYLE = """
    font-size: 14px;
    color: #F8F8F2;
    text-align: center;
"""