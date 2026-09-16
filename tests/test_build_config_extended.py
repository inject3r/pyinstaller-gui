"""Tests for the newly added BuildConfig fields (Imports & Hooks, build
behavior, and Windows/macOS specific options)."""

import unittest

from pyinstaller_gui.models.build_config import BuildConfig


class TestBuildConfigExtendedDefaults(unittest.TestCase):
    """Test cases verifying sensible, backward-compatible defaults."""

    def setUp(self):
        """Set up test fixtures."""
        self.config = BuildConfig()

    def test_import_discovery_defaults(self):
        """Search paths, excludes, and collect-* options default to empty lists."""
        self.assertEqual(self.config.search_paths, [])
        self.assertEqual(self.config.exclude_modules, [])
        self.assertEqual(self.config.collect_all, [])
        self.assertEqual(self.config.collect_submodules, [])
        self.assertEqual(self.config.collect_data, [])
        self.assertEqual(self.config.collect_binaries, [])
        self.assertEqual(self.config.copy_metadata, [])
        self.assertEqual(self.config.recursive_copy_metadata, [])
        self.assertEqual(self.config.additional_hooks_dir, "")
        self.assertEqual(self.config.runtime_hooks, [])
        self.assertEqual(self.config.splash_image, "")

    def test_build_behavior_defaults(self):
        """Build-behavior toggles default to their PyInstaller-safe values."""
        self.assertFalse(self.config.noconfirm)
        self.assertFalse(self.config.strip)
        self.assertFalse(self.config.noupx)
        self.assertEqual(self.config.upx_exclude, [])
        self.assertEqual(self.config.optimize_level, "")
        self.assertEqual(self.config.python_options, [])
        self.assertEqual(self.config.contents_directory, "")
        self.assertEqual(self.config.specpath, "")
        self.assertEqual(self.config.workpath, "")
        self.assertFalse(self.config.bootloader_ignore_signals)

    def test_windows_and_macos_defaults(self):
        """Platform-specific options default to off/empty."""
        self.assertFalse(self.config.console_explicit)
        self.assertEqual(self.config.hide_console, "none")
        self.assertFalse(self.config.disable_windowed_traceback)
        self.assertEqual(self.config.version_file, "")
        self.assertEqual(self.config.manifest_file, "")
        self.assertFalse(self.config.uac_admin)
        self.assertFalse(self.config.uac_uiaccess)
        self.assertFalse(self.config.argv_emulation)
        self.assertEqual(self.config.osx_bundle_identifier, "")
        self.assertEqual(self.config.target_arch, "")
        self.assertEqual(self.config.codesign_identity, "")
        self.assertEqual(self.config.osx_entitlements_file, "")

    def test_lists_are_independent_between_instances(self):
        """Mutating one instance's list fields must not affect a new instance
        (regression guard against a shared mutable default)."""
        config_a = BuildConfig()
        config_a.search_paths.append("./libs")
        config_b = BuildConfig()
        self.assertEqual(config_b.search_paths, [])


if __name__ == "__main__":
    unittest.main()
