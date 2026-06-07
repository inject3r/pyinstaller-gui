def get_dark_stylesheet() -> str:
    """Get dark theme stylesheet."""
    return """
        * {
            font-family: 'Segoe UI', 'Fira Code', 'Monaco', monospace;
            font-size: 13px;
            color: #E8EDF2;
        }
        
        QWidget {
            background-color: #0A0C10;
        }
        
        QPushButton {
            background: #1A5C7E;
            border: none;
            border-radius: 6px;
            padding: 8px 20px;
            font-weight: 500;
        }
        QPushButton:hover {
            background: #217A9E;
        }
        QPushButton:pressed {
            background: #0E4A64;
        }
        
        QPushButton#GitHubButton {
            background: #1E1E1E;
            color: #E8EDF2;
            font-weight: 500;
            border-radius: 6px;
            padding: 5px 16px 5px 10px;
            font-size: 12px;
        }
        QPushButton#GitHubButton:hover {
            background: #1A5C7E;
        }
        
        QPushButton#ThemeToggle {
            background: transparent;
            border: none;
            border-radius: 4px;
            padding: 2px;
        }
        QPushButton#ThemeToggle:hover {
            background: transparent;
        }
        
        QWidget#HeaderWidget {
            background-color: #14171C;
            border-radius: 10px;
            margin-bottom: 5px;
        }
        
        QLineEdit, QTextEdit, QComboBox {
            background-color: #14171C;
            border: 1px solid #2A2E36;
            border-radius: 6px;
            padding: 7px 12px;
            selection-background-color: #1A5C7E;
        }
        QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
            border-color: #2D8FBA;
            background-color: #1A1E24;
        }
        
        QCheckBox {
            spacing: 8px;
        }
        QCheckBox::indicator {
            width: 16px;
            height: 16px;
            border-radius: 4px;
            border: 1.5px solid #3A3F48;
            background: #14171C;
        }
        QCheckBox::indicator:checked {
            background: #1A5C7E;
            border-color: #1A5C7E;
        }
        
        QGroupBox {
            border: 1px solid #2A2E36;
            border-radius: 8px;
            margin-top: 12px;
            padding-top: 8px;
            background-color: rgba(20, 23, 28, 0.6);
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            left: 10px;
            padding: 0 10px;
            background-color: #1A1E24;
            color: #2D8FBA;
            font-weight: 600;
            border-radius: 12px;
        }
        
        QTabWidget::pane {
            border: 1px solid #2A2E36;
            border-radius: 8px;
            background-color: #0A0C10;
        }
        QTabBar::tab {
            background-color: #14171C;
            padding: 8px 20px;
            margin-right: 3px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
        }
        QTabBar::tab:selected {
            background-color: #0A0C10;
            border-bottom: 2px solid #2D8FBA;
            color: #2D8FBA;
        }
        
        QScrollBar:vertical {
            background-color: #0A0C10;
            width: 10px;
            border-radius: 5px;
        }
        QScrollBar::handle:vertical {
            background-color: #2A2E36;
            border-radius: 5px;
            min-height: 30px;
        }
        QScrollBar::handle:vertical:hover {
            background-color: #1A5C7E;
        }
        
        QTreeWidget, QListWidget {
            background-color: #14171C;
            border: 1px solid #2A2E36;
            border-radius: 6px;
            alternate-background-color: #1A1E24;
        }
        QTreeWidget::item, QListWidget::item {
            padding: 5px;
        }
        QTreeWidget::item:selected, QListWidget::item:selected {
            background-color: #1A5C7E;
        }
        
        QTextEdit:read-only {
            background-color: #0D0F12;
            color: #7A8089;
        }
        
        QComboBox {
            min-height: 30px;
        }
        QComboBox::drop-down {
            border: none;
            width: 25px;
        }
    """


def get_light_stylesheet() -> str:
    """Get light theme stylesheet."""
    return """
        * {
            font-family: 'Segoe UI', 'Fira Code', 'Monaco', monospace;
            font-size: 13px;
            color: #1E1E1E;
        }
        
        QWidget {
            background-color: #F5F5F5;
        }
        
        QPushButton {
            background: #007ACC;
            border: none;
            border-radius: 6px;
            padding: 8px 20px;
            font-weight: 500;
            color: white;
        }
        QPushButton:hover {
            background: #005A9E;
        }
        QPushButton:pressed {
            background: #004070;
        }
        
        QPushButton#GitHubButton {
            background: #1E1E1E;
            color: #E8EDF2;
            font-weight: 500;
            border-radius: 6px;
            padding: 5px 16px 5px 10px;
            font-size: 12px;
        }
        QPushButton#GitHubButton:hover {
            background: #007ACC;
            color: white;
        }
        
        QPushButton#ThemeToggle {
            background: transparent;
            border: none;
            border-radius: 4px;
            padding: 2px;
        }
        QPushButton#ThemeToggle:hover {
            background: transparent;
        }
        
        QWidget#HeaderWidget {
            background-color: #FFFFFF;
            border-radius: 10px;
            margin-bottom: 5px;
        }
        
        QLineEdit, QTextEdit, QComboBox {
            background-color: white;
            border: 1px solid #CCCCCC;
            border-radius: 6px;
            padding: 7px 12px;
            selection-background-color: #007ACC;
            selection-color: white;
        }
        QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
            border-color: #007ACC;
        }
        
        QCheckBox {
            spacing: 8px;
        }
        QCheckBox::indicator {
            width: 16px;
            height: 16px;
            border-radius: 4px;
            border: 1.5px solid #CCCCCC;
            background: white;
        }
        QCheckBox::indicator:checked {
            background: #007ACC;
            border-color: #007ACC;
        }
        
        QGroupBox {
            border: 1px solid #CCCCCC;
            border-radius: 8px;
            margin-top: 12px;
            padding-top: 8px;
            background-color: rgba(255, 255, 255, 0.6);
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            left: 10px;
            padding: 0 10px;
            background-color: #E0E0E0;
            color: #007ACC;
            font-weight: 600;
            border-radius: 12px;
        }
        
        QTabWidget::pane {
            border: 1px solid #CCCCCC;
            border-radius: 8px;
            background-color: #F5F5F5;
        }
        QTabBar::tab {
            background-color: #E0E0E0;
            padding: 8px 20px;
            margin-right: 3px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
        }
        QTabBar::tab:selected {
            background-color: #F5F5F5;
            border-bottom: 2px solid #007ACC;
            color: #007ACC;
        }
        
        QScrollBar:vertical {
            background-color: #F5F5F5;
            width: 10px;
            border-radius: 5px;
        }
        QScrollBar::handle:vertical {
            background-color: #CCCCCC;
            border-radius: 5px;
            min-height: 30px;
        }
        QScrollBar::handle:vertical:hover {
            background-color: #007ACC;
        }
        
        QTreeWidget, QListWidget {
            background-color: white;
            border: 1px solid #CCCCCC;
            border-radius: 6px;
            alternate-background-color: #F9F9F9;
        }
        QTreeWidget::item, QListWidget::item {
            padding: 5px;
        }
        QTreeWidget::item:selected, QListWidget::item:selected {
            background-color: #007ACC;
            color: white;
        }
        
        QTextEdit:read-only {
            background-color: #F0F0F0;
            color: #6E6E6E;
        }
        
        QComboBox {
            min-height: 30px;
        }
        QComboBox::drop-down {
            border: none;
            width: 25px;
        }
    """


def get_stylesheet(is_dark_mode: bool = True) -> str:
    """Get stylesheet based on theme."""
    if is_dark_mode:
        return get_dark_stylesheet()
    else:
        return get_light_stylesheet()