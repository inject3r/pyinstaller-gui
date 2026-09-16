"""Extended tests for command builder module: cross-platform behavior,
build_args(), and newly added PyInstaller options."""

import os
import tempfile
import unittest
from unittest.mock import patch

from pyinstaller_gui.core.command_builder import CommandBuilder, _data_separator
from pyinstaller_gui.models.build_config import BuildConfig
from pyinstaller_gui.models.file_item import FileItem, FileType


class TestDataSeparator(unittest.TestCase):
    """Tests for the OS-aware --add-data/--add-binary separator helper."""

    @patch("pyinstaller_gui.core.command_builder.platform.system", return_value="Windows")
    def test_windows_uses_semicolon(self, mock_system):
        """On Windows, PyInstaller expects ';' between SOURCE and DEST."""
        self.assertEqual(_data_separator(), ";")

    @patch("pyinstaller_gui.core.command_builder.platform.system", return_value="Linux")
    def test_linux_uses_colon(self, mock_system):
        """On Linux, PyInstaller expects ':' between SOURCE and DEST."""
        self.assertEqual(_data_separator(), ":")

    @patch("pyinstaller_gui.core.command_builder.platform.system", return_value="Darwin")
    def test_macos_uses_colon(self, mock_system):
        """On macOS, PyInstaller expects ':' between SOURCE and DEST."""
        self.assertEqual(_data_separator(), ":")


class TestCommandBuilderCrossPlatform(unittest.TestCase):
    """Tests that --add-data honors the platform-correct separator."""

    def setUp(self):
        """Create a builder, a minimal config, and a temporary test script."""
        self.builder = CommandBuilder()
        self.config = BuildConfig()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_script = os.path.join(self.temp_dir.name, "test_script.py")
        with open(self.test_script, "w") as f:
            f.write("# Test script")
        self.config.script_path = self.test_script

    def tearDown(self):
        """Clean up the temporary directory."""
        self.temp_dir.cleanup()

    @patch("pyinstaller_gui.core.command_builder.platform.system", return_value="Windows")
    def test_add_data_uses_semicolon_on_windows(self, mock_system):
        """--add-data must use ';' as the separator when building on Windows."""
        self.config.additional_files = [FileItem("C:\\data\\file.txt", FileType.FILE)]
        self.builder.set_config(self.config)
        command = self.builder.build()
        self.assertIn('--add-data "C:\\data\\file.txt;."', command)
        self.assertNotIn('--add-data "C:\\data\\file.txt:."', command)

    def test_add_data_respects_custom_destination(self):
        """A custom destination should be preserved instead of always '.'."""
        self.config.additional_files = [FileItem("/path/to/file.txt", FileType.FILE, dest="assets/data")]
        self.builder.set_config(self.config)
        command = self.builder.build()
        self.assertIn('--add-data "/path/to/file.txt:assets/data"', command)

    def test_blank_destination_normalizes_to_root(self):
        """An empty destination should normalize to '.' (the bundle root)."""
        item = FileItem("/path/to/file.txt", FileType.FILE, dest="")
        self.assertEqual(item.dest, ".")


class TestCommandBuilderArgsList(unittest.TestCase):
    """Tests for CommandBuilder.build_args(), the safe argv-list builder."""

    def setUp(self):
        """Create a builder, a minimal config, and a temporary test script."""
        self.builder = CommandBuilder()
        self.config = BuildConfig()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_script = os.path.join(self.temp_dir.name, "test_script.py")
        with open(self.test_script, "w") as f:
            f.write("# Test script")
        self.config.script_path = self.test_script

    def tearDown(self):
        """Clean up the temporary directory."""
        self.temp_dir.cleanup()

    def test_build_args_raises_without_script(self):
        """build_args() should raise ValueError instead of returning an error string."""
        builder = CommandBuilder()
        builder.set_config(BuildConfig())
        with self.assertRaises(ValueError):
            builder.build_args()

    def test_build_args_returns_list_of_strings(self):
        """build_args() must return a plain list of string tokens."""
        self.builder.set_config(self.config)
        args = self.builder.build_args()
        self.assertIsInstance(args, list)
        self.assertTrue(all(isinstance(a, str) for a in args))
        self.assertEqual(args[0], self.test_script)

    def test_build_args_name_as_separate_tokens(self):
        """--name and its value should be separate argv entries (no shell quoting needed)."""
        self.config.app_name = "My Cool App"
        self.builder.set_config(self.config)
        args = self.builder.build_args()
        self.assertIn("--name", args)
        idx = args.index("--name")
        self.assertEqual(args[idx + 1], "My Cool App")

    def test_build_args_hidden_imports_multiple_entries(self):
        """Each hidden import should produce its own --hidden-import entry."""
        self.config.hidden_imports = ["numpy", "pandas"]
        self.builder.set_config(self.config)
        args = self.builder.build_args()
        self.assertEqual(args.count("--hidden-import"), 2)
        self.assertIn("numpy", args)
        self.assertIn("pandas", args)

    def test_build_args_custom_commands_split(self):
        """Custom commands should be tokenized instead of passed as one blob."""
        self.config.custom_commands = "--optimize 2 --noupx"
        self.builder.set_config(self.config)
        args = self.builder.build_args()
        self.assertIn("--optimize", args)
        self.assertIn("2", args)
        self.assertIn("--noupx", args)


class TestCommandBuilderNewOptions(unittest.TestCase):
    """Tests for the newly added PyInstaller options."""

    def setUp(self):
        """Create a builder, a minimal config, and a temporary test script."""
        self.builder = CommandBuilder()
        self.config = BuildConfig()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_script = os.path.join(self.temp_dir.name, "test_script.py")
        with open(self.test_script, "w") as f:
            f.write("# Test script")
        self.config.script_path = self.test_script

    def tearDown(self):
        """Clean up the temporary directory."""
        self.temp_dir.cleanup()

    def test_search_paths(self):
        """--paths should appear once per configured search path."""
        self.config.search_paths = ["./libs", "../shared"]
        self.builder.set_config(self.config)
        command = self.builder.build()
        self.assertIn('--paths "./libs"', command)
        self.assertIn('--paths "../shared"', command)

    def test_exclude_modules(self):
        """--exclude-module should appear once per excluded module."""
        self.config.exclude_modules = ["tkinter", "unittest"]
        self.builder.set_config(self.config)
        command = self.builder.build()
        self.assertIn("--exclude-module tkinter", command)
        self.assertIn("--exclude-module unittest", command)

    def test_collect_all(self):
        """--collect-all should appear once per package."""
        self.config.collect_all = ["requests"]
        self.builder.set_config(self.config)
        command = self.builder.build()
        self.assertIn("--collect-all requests", command)

    def test_copy_metadata(self):
        """--copy-metadata should appear once per package."""
        self.config.copy_metadata = ["my_package"]
        self.builder.set_config(self.config)
        command = self.builder.build()
        self.assertIn("--copy-metadata my_package", command)

    def test_splash_image(self):
        """--splash should include the configured image path."""
        self.config.splash_image = "/path/to/splash.png"
        self.builder.set_config(self.config)
        command = self.builder.build()
        self.assertIn('--splash "/path/to/splash.png"', command)

    def test_noupx_takes_precedence_over_upx_dir(self):
        """When noupx is set, --noupx should be used and --upx-dir omitted."""
        self.config.noupx = True
        self.config.upx_dir = "/opt/upx"
        self.builder.set_config(self.config)
        command = self.builder.build()
        self.assertIn("--noupx", command)
        self.assertNotIn("--upx-dir", command)

    def test_optimize_and_strip(self):
        """--optimize and --strip should reflect the configured values."""
        self.config.optimize_level = "2"
        self.config.strip = True
        self.builder.set_config(self.config)
        command = self.builder.build()
        self.assertIn("--optimize 2", command)
        self.assertIn("--strip", command)

    def test_noconfirm(self):
        """--noconfirm should appear when enabled."""
        self.config.noconfirm = True
        self.builder.set_config(self.config)
        command = self.builder.build()
        self.assertIn("--noconfirm", command)

    def test_contents_directory(self):
        """--contents-directory should reflect a custom onedir layout name."""
        self.config.contents_directory = "support"
        self.builder.set_config(self.config)
        command = self.builder.build()
        self.assertIn('--contents-directory "support"', command)

    def test_specpath_and_workpath(self):
        """--specpath and --workpath should reflect configured folders."""
        self.config.specpath = "./spec"
        self.config.workpath = "./work"
        self.builder.set_config(self.config)
        command = self.builder.build()
        self.assertIn('--specpath "./spec"', command)
        self.assertIn('--workpath "./work"', command)

    def test_windows_options(self):
        """Windows-only options should be included when set."""
        self.config.hide_console = "minimize-late"
        self.config.disable_windowed_traceback = True
        self.config.version_file = "version.txt"
        self.config.manifest_file = "app.manifest"
        self.config.uac_admin = True
        self.config.uac_uiaccess = True
        self.builder.set_config(self.config)
        command = self.builder.build()
        self.assertIn("--hide-console minimize-late", command)
        self.assertIn("--disable-windowed-traceback", command)
        self.assertIn('--version-file "version.txt"', command)
        self.assertIn('--manifest "app.manifest"', command)
        self.assertIn("--uac-admin", command)
        self.assertIn("--uac-uiaccess", command)

    def test_macos_options(self):
        """macOS-only options should be included when set."""
        self.config.argv_emulation = True
        self.config.osx_bundle_identifier = "com.example.app"
        self.config.target_arch = "universal2"
        self.config.codesign_identity = "Developer ID"
        self.config.osx_entitlements_file = "entitlements.plist"
        self.builder.set_config(self.config)
        command = self.builder.build()
        self.assertIn("--argv-emulation", command)
        self.assertIn('--osx-bundle-identifier "com.example.app"', command)
        self.assertIn("--target-architecture universal2", command)
        self.assertIn('--codesign-identity "Developer ID"', command)
        self.assertIn('--osx-entitlements-file "entitlements.plist"', command)

    def test_console_explicit_ignored_when_noconsole_set(self):
        """--windowed (noconsole) should win over an explicit --console request."""
        self.config.noconsole = True
        self.config.console_explicit = True
        self.builder.set_config(self.config)
        command = self.builder.build()
        self.assertIn("--windowed", command)
        self.assertNotIn("--console", command)

    def test_log_level_normalizes_common_aliases(self):
        """WARNING/CRITICAL should map to PyInstaller's WARN/FATAL values."""
        self.config.log_level = "warning"
        self.builder.set_config(self.config)
        self.assertIn("--log-level WARN", self.builder.build())

        self.config.log_level = "critical"
        self.builder.set_config(self.config)
        self.assertIn("--log-level FATAL", self.builder.build())


if __name__ == "__main__":
    unittest.main()
