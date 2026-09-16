## Changelog

### Version 1.3.0 (Current)

**Critical fixes:**
- Fixed `--add-data`/`--add-binary` to use the OS-correct separator between
  source and destination (`;` on Windows, `:` on Linux/macOS). It was
  previously hardcoded to `:` and silently produced broken builds on Windows.
- Replaced `shell=True` command execution (a hand-quoted string run through
  the system shell) with a direct, argument-list `subprocess` call via
  `sys.executable -m PyInstaller`. This removes a shell-quoting/injection
  risk, always uses the exact PyInstaller installed for this app instead of
  whatever happens to be first on PATH, and execution now uses the parsed
  configuration directly instead of scraping the on-screen (HTML) command
  preview.
- Fixed a real deadlock risk in the build worker: it used to read PyInstaller's
  stdout and stderr as two separate blocking pipes in turn; since PyInstaller
  writes most of its output to stderr, this could hang once a pipe buffer
  filled. Streams are now merged before reading.
- Fixed `VersionChecker` to use `sys.executable` instead of a hardcoded
  `python`/`pyinstaller` command name, which is unreliable across OSes
  (some Linux distros have no bare `python`) and inside virtual environments.
- Fixed a severe pre-existing bug in the command preview's syntax
  highlighter: it ran repeated plain-text `str.replace()` calls on text that
  already contained previously inserted HTML. Because the CSS text
  `font-weight: bold;` is present in every inserted span, and `-w` (the short
  flag for `--windowed`) was one of the strings being replaced, `-w` matched
  *inside that CSS text* and tore the span apart mid-attribute, corrupting
  the preview into garbled, unreadable HTML for almost any real command.
  Rewritten as a proper tokenizer with exact round-trip-fidelity tests.
- Fixed the "No Console (-w)" tooltip/help text, which incorrectly said
  "Windows only" — it is actually Windows **and** macOS (and on macOS it
  also triggers building a proper `.app` bundle).
- Fixed the Recent Files list being polluted with every partial path typed
  character-by-character into the script field; it now only records paths
  once they point to an existing `.py` file.
- Added `darkdetect` as a declared dependency — the "System" theme option
  silently never detected the OS's actual dark/light mode without it.
- Version detection at startup now runs on a background thread instead of
  blocking the UI while two subprocesses run synchronously.

**PyInstaller 6.22.x option coverage:**
- New "Imports & Hooks" tab: `--paths`, `--exclude-module`,
  `--collect-all`/`--collect-submodules`/`--collect-data`/`--collect-binaries`,
  `--copy-metadata`/`--recursive-copy-metadata`, `--additional-hooks-dir`,
  `--runtime-hook`, `--splash`
- Advanced tab: a real "Disable UPX" (`--noupx`) toggle (previously there was
  no way to actually turn UPX off, only point at a directory),
  `--upx-exclude`, `--optimize`, `--strip`, `--python-option`, `--noconfirm`,
  `--contents-directory`, `--bootloader-ignore-signals`
- Settings tab: `--specpath`/`--workpath`, a Windows Options group
  (`--hide-console`, `--disable-windowed-traceback`, `--version-file`,
  `--manifest`, `--uac-admin`, `--uac-uiaccess`) and a macOS Options group
  (`--argv-emulation`, `--osx-bundle-identifier`, `--target-architecture`,
  `--codesign-identity`, `--osx-entitlements-file`)
- Additional Files tab: files/folders/binaries can now target a specific
  destination folder inside the bundle (editable Destination column),
  not just the bundle root
- Config export/import (JSON) covers every new field, with graceful
  fallback to defaults for older config files

**Other improvements:**
- Run button now has a Stop button next to it to cancel an in-progress build
- On a successful build, the app offers to open the output folder directly
- Every tab now scrolls, so the larger option set stays usable in a smaller
  window
- Added a CI workflow (there was none before) running the full test suite
  on Linux, Windows, and macOS
- Bumped the minimum PyInstaller dependency to 6.22.0 and PyQt6's declared
  Python floor to 3.9 (matching what PyQt6 itself actually requires)

### Version 1.2.1

- Added Dark & Light themes with system theme detection
- Added Drag & Drop support for script files
- Added Recent Files functionality
- Added Configuration Export/Import (JSON format)
- Added Syntax highlighting for command preview
- Added Search and Filter in Additional Files tab
- Added Edit functionality for file paths (double-click or edit button)
- Added Copy command and Copy log buttons
- Added Save log to file functionality
- Added Remove All button for additional files
- Added Help dialogs with ? button in each tab
- Added Tooltips for all UI elements
- Improved error handling and user feedback
- Added comprehensive unit tests (98+ tests)
- Added test coverage reporting