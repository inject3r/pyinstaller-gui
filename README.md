# PyInstaller GUI

A powerful GUI wrapper for PyInstaller — convert your Python scripts into standalone executables for Windows, macOS, and Linux with ease.

![Screenshot](/screenshot/screenshot_1.jpg)

## Features

- **Cross-platform support**: Convert your Python scripts into executables for Windows, macOS, and Linux.
- **Easy-to-use GUI**: No need to remember complex command-line arguments; a simple and intuitive interface for creating executables.
- **Customizable settings**: Fine-tune various PyInstaller options like adding extra files, hidden imports, and more.
- **Real-time logging**: View everything happening during the conversion process with detailed logs.

## Installation

You can install PyInstaller GUI via pip:

```bash
pip install pyinstaller-gui
```

Or, if you prefer to clone the repository directly:

```bash
git clone https://github.com/inject3r/pyinstaller-gui.git
cd pyinstaller-gui
pip install -r requirements.txt
```

## Usage

### Launching the GUI

To start the PyInstaller GUI, simply run the following command:

```bash
pyinstaller-gui
```

### Converting a Script

1. Open the PyInstaller GUI application.
2. Load your Python script by clicking the **Browse** button.
3. Adjust the settings (optional).
4. Click **Build** to generate the executable.

### Custom Settings

- **Add Files/Folders**: Include additional files or folders to bundle with your executable.
- **Hidden Imports**: Specify hidden imports to ensure your script runs smoothly after packaging.
- **Icon**: Choose a custom icon for your executable.
- **Output Folder**: Define where the output executable will be saved.
- **And** ...

> **Note:** To generate the executable for a specific operating system, you must run this module on that system. For example, to create a Windows executable, you need to run the module on a Windows machine.

## Requirements

- Python 3.x
- PyInstaller (automatically installed when using PyInstaller GUI)
- Qt (for the graphical interface)

## Supported Platforms

- **Windows**: Create .exe files for Windows.
- **macOS**: Generate .app files for macOS.
- **Linux**: Create executables for Linux.

## Screenshots

![Screenshot](/screenshot/screenshot_1.jpg)
![Screenshot](/screenshot/screenshot_2.jpg)
![Screenshot](/screenshot/screenshot_3.jpg)
![Screenshot](/screenshot/screenshot_4.jpg)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
