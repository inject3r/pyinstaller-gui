<p align="center">
  <img src="https://github.com/inject3r/pyinstaller-gui/blob/main/logo.jpg?raw=true" alt="PyInstaller GUI Logo">
</p>

<!-- # PyInstaller GUI -->

A powerful GUI wrapper for PyInstaller — convert your Python scripts into standalone executables for Windows, macOS, and Linux with ease.

<br/>

<p align="center">
  <img src="https://github.com/inject3r/pyinstaller-gui/blob/main/tests/screenshot/screenshot_1.jpg?raw=true" alt="PyInstaller GUI Screenshot" width="500">
</p>

## Features

- **Cross-platform support**: Convert your Python scripts into executables for Windows, macOS, and Linux
- **Easy-to-use GUI**: No need to remember complex command-line arguments; a simple and intuitive interface
- **Dark & Light Themes**: Automatic system theme detection with manual override options
- **Drag & Drop Support**: Simply drag and drop your Python script into the application
- **Recent Files**: Quickly access recently used scripts from the dropdown menu
- **Configuration Management**: Export and import build configurations as JSON files for reuse and sharing
- **Syntax Highlighting**: Command preview with color-coded syntax highlighting for better readability
- **Search & Filter**: Search and filter additional files in the file tree
- **Edit Files**: Edit file paths directly or double-click to modify
- **Copy & Save Logs**: Copy generated commands or save build logs to files
- **Customizable settings**: Fine-tune various PyInstaller options like adding extra files, hidden imports, and more
- **Real-time logging**: View everything happening during the conversion process with detailed logs

## Installation

You can install PyInstaller GUI via pip:

```bash
pip install --upgrade pyinstaller-gui
```

Or, if you prefer to clone the repository directly:

```bash
git clone https://github.com/inject3r/pyinstaller-gui.git
cd pyinstaller-gui
pip install -e .
```

## Usage

### Launching the GUI

To start the PyInstaller GUI, simply run the following command:

```bash
pyinstaller-gui
```

Or:

```bash
pyinstallergui
```

### Converting a Script

1. Open the PyInstaller GUI application
2. Load your Python script by:
   - Clicking the **Browse** button
   - Dragging and dropping a `.py` file into the script field
   - Selecting from **Recent** files dropdown
3. Configure your build options across the tabs:
   - **General**: Basic options (OneFile, No Console, Hidden Imports)
   - **Additional Files**: Add files, folders, or binaries to bundle
   - **Advanced**: Log level, UPX compression, debug mode
   - **Settings**: Output folder, custom icon, runtime tmpdir
   - **Config**: Export/Import build configurations
4. Click **Run PyInstaller** to generate the executable

### Configuration Management

- **Export Configuration**: Save your current settings as a JSON file
- **Import Configuration**: Load previously saved settings
- **Preview**: View a human-readable summary of your current configuration

### Keyboard Shortcuts & Tips

- **Double-click** any file in the Additional Files list to edit its path
- Use the **Search** box to filter files in the Additional Files tab
- **Copy** button copies the generated command to clipboard
- **Save Log** saves the build output to a file with timestamp
- **Clear** button clears the output console

### Custom Settings

| Feature | Description |
|---------|-------------|
| **OneFile (-F)** | Create a single executable file instead of a folder |
| **No Console (-w)** | Hide the console window (GUI applications) |
| **Hidden Imports** | Specify modules that are imported dynamically |
| **Additional Files** | Include files, folders, or binaries to bundle |
| **Icon** | Choose a custom icon (.ico for Windows, .icns for macOS) |
| **Output Folder** | Define where the executable will be saved |
| **UPX Directory** | Path to UPX for executable compression |
| **Log Level** | Control build output verbosity (TRACE, DEBUG, INFO, WARN, ERROR, FATAL) |
| **Debug Mode** | Enable debug features (all, imports, bootloader, noarchive) |
| **Runtime Tmpdir** | Custom temporary directory for onefile mode |
| **Clean Cache** | Clear PyInstaller cache before building |
| **Custom Commands** | Add any additional PyInstaller arguments |

> **Note:** To generate the executable for a specific operating system, you must run this module on that system. For example, to create a Windows executable, you need to run the module on a Windows machine.

## Requirements

- Python 3.6+
- PyInstaller 6.11.1+
- PyQt6 6.8.1+

## Supported Platforms

- **Windows**: Create .exe files for Windows
- **macOS**: Generate .app bundles for macOS
- **Linux**: Create executables for Linux

## Development

### Running Tests

```bash
# Run all tests with coverage
./scripts/tests.sh

# Clean test output files
./scripts/test_clean.sh

# Run a single test file
python -m pytest tests/test_command_builder.py -v
```

### Building from Source

```bash
# Install in development mode
pip install -e .

# Install with dev dependencies
pip install -e ".[dev]"

# Build distribution
python -m build

# Build executable with PyInstaller
pyinstaller pyinstaller-gui.spec
```

### Code Coverage

After running `./scripts/tests.sh`, open the coverage report:

```bash
# Open HTML coverage report
firefox tests/coverage_html/index.html
# or
google-chrome tests/coverage_html/index.html
```

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **PyInstaller not found** | Install with `pip install pyinstaller` |
| **Module not found errors** | Add missing modules to Hidden Imports |
| **Icon not showing** | Ensure icon format is correct (.ico for Windows, .icns for macOS) |
| **Permission denied on Linux** | Run `chmod +x dist/your_app` |
| **Command preview shows error** | Check if script path is valid and file exists |
| **Build fails with no console** | GUI applications need `--windowed` flag (already set by No Console option) |

### Getting Help

- Check the built-in help dialogs (click the **?** button in each tab)
- View the command preview before building to verify arguments
- Check the output console for detailed error messages
- Visit the [GitHub Issues](https://github.com/inject3r/pyinstaller-gui/issues) page

## Screenshots

<div style="display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; margin: 30px 0;">
  
  <div style="text-align: center; flex: 1; min-width: 250px;">
    <a href="https://github.com/inject3r/pyinstaller-gui/blob/main/tests/screenshot/screenshot_1.jpg" target="_blank">
      <img src="https://github.com/inject3r/pyinstaller-gui/blob/main/tests/screenshot/screenshot_1.jpg?raw=true" alt="Screenshot 1" style="width: 100%; max-width: 350px; border: 1px solid #ddd; border-radius: 8px; transition: transform 0.2s;">
    </a>
  </div>

  <div style="text-align: center; flex: 1; min-width: 250px;">
    <a href="https://github.com/inject3r/pyinstaller-gui/blob/main/tests/screenshot/screenshot_2.jpg" target="_blank">
      <img src="https://github.com/inject3r/pyinstaller-gui/blob/main/tests/screenshot/screenshot_2.jpg?raw=true" alt="Screenshot 2" style="width: 100%; max-width: 350px; border: 1px solid #ddd; border-radius: 8px; transition: transform 0.2s;">
    </a>
  </div>

  <div style="text-align: center; flex: 1; min-width: 250px;">
    <a href="https://github.com/inject3r/pyinstaller-gui/blob/main/tests/screenshot/screenshot_3.jpg" target="_blank">
      <img src="https://github.com/inject3r/pyinstaller-gui/blob/main/tests/screenshot/screenshot_3.jpg?raw=true" alt="Screenshot 3" style="width: 100%; max-width: 350px; border: 1px solid #ddd; border-radius: 8px; transition: transform 0.2s;">
    </a>
  </div>

</div>

<div style="display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; margin: 30px 0;">
  
  <div style="text-align: center; flex: 1; min-width: 250px;">
    <a href="https://github.com/inject3r/pyinstaller-gui/blob/main/tests/screenshot/screenshot_4.jpg" target="_blank">
      <img src="https://github.com/inject3r/pyinstaller-gui/blob/main/tests/screenshot/screenshot_4.jpg?raw=true" alt="Screenshot 4" style="width: 100%; max-width: 350px; border: 1px solid #ddd; border-radius: 8px; transition: transform 0.2s;">
    </a>
  </div>

  <div style="text-align: center; flex: 1; min-width: 250px;">
    <a href="https://github.com/inject3r/pyinstaller-gui/blob/main/tests/screenshot/screenshot_5.jpg" target="_blank">
      <img src="https://github.com/inject3r/pyinstaller-gui/blob/main/tests/screenshot/screenshot_5.jpg?raw=true" alt="Screenshot 5" style="width: 100%; max-width: 350px; border: 1px solid #ddd; border-radius: 8px; transition: transform 0.2s;">
    </a>
  </div>

  <div style="text-align: center; flex: 1; min-width: 250px;">
    <a href="https://github.com/inject3r/pyinstaller-gui/blob/main/tests/screenshot/screenshot_6.jpg" target="_blank">
      <img src="https://github.com/inject3r/pyinstaller-gui/blob/main/tests/screenshot/screenshot_6.jpg?raw=true" alt="Screenshot 6" style="width: 100%; max-width: 350px; border: 1px solid #ddd; border-radius: 8px; transition: transform 0.2s;">
    </a>
  </div>

</div>

<style>
  a:hover img {
    transform: scale(1.02);
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
  }
</style>

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting

## Acknowledgments

- [PyInstaller](https://www.pyinstaller.org/) - The core packaging tool
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) - GUI framework
- [UPX](https://upx.github.io/) - Executable compressor
- All contributors and users of this project