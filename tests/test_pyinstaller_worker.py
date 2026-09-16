"""Tests for the PyInstallerWorker background execution thread.

These tests run PyInstallerWorker against a stub 'PyInstaller' module
(importable on sys.path) instead of the real PyInstaller, so they stay fast
and deterministic while still exercising the real subprocess plumbing
(no shell, sys.executable -m PyInstaller, merged stdout/stderr, signals).
"""

import sys
import textwrap
import unittest
from pathlib import Path

from PyQt6.QtCore import QCoreApplication, QEventLoop, QTimer

from pyinstaller_gui.workers.pyinstaller_worker import PyInstallerWorker


def _ensure_qcoreapplication():
    """Ensure a QCoreApplication instance exists (QThread needs an event loop)."""
    app = QCoreApplication.instance()
    if app is None:
        app = QCoreApplication(sys.argv)
    return app


class _StubPyInstallerOnPath(unittest.TestCase):
    """Base class that puts a fake 'PyInstaller' package on PYTHONPATH.

    The stub package prints a couple of lines (one to stdout, one to
    stderr, to exercise the stream-merging behavior) and exits with a
    configurable status code, so tests don't depend on PyInstaller
    actually being able to freeze a script (slow, and not the point here).
    """

    EXIT_CODE = 0

    def setUp(self):
        """Create a temporary fake PyInstaller module importable via -m."""
        self.app = _ensure_qcoreapplication()

        import tempfile
        self.stub_dir = tempfile.TemporaryDirectory()
        pkg_dir = Path(self.stub_dir.name) / "PyInstaller"
        pkg_dir.mkdir()
        (pkg_dir / "__init__.py").write_text("")
        (pkg_dir / "__main__.py").write_text(textwrap.dedent(f"""
            import sys
            print("stub pyinstaller: starting build")
            print("stub pyinstaller: warning example", file=sys.stderr)
            print("stub pyinstaller: args=" + " ".join(sys.argv[1:]))
            sys.exit({self.EXIT_CODE})
        """))

        self._orig_path = list(sys.path)
        self._orig_pythonpath = None

        import os
        self._orig_pythonpath = os.environ.get("PYTHONPATH", "")
        os.environ["PYTHONPATH"] = self.stub_dir.name + os.pathsep + self._orig_pythonpath

    def tearDown(self):
        """Restore PYTHONPATH and clean up the temporary stub package."""
        import os
        if self._orig_pythonpath is not None:
            os.environ["PYTHONPATH"] = self._orig_pythonpath
        self.stub_dir.cleanup()

    def _run_worker_and_wait(self, worker: PyInstallerWorker, timeout_ms: int = 10000):
        """Start a worker and block (via a local event loop) until it finishes."""
        loop = QEventLoop()
        result = {}

        def on_finished(code):
            result["code"] = code
            loop.quit()

        worker.finished_signal.connect(on_finished)

        timer = QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(loop.quit)
        timer.start(timeout_ms)

        worker.start()
        loop.exec()

        self.assertIn("code", result, "worker did not finish within the timeout")
        return result["code"]


class TestPyInstallerWorkerSuccess(_StubPyInstallerOnPath):
    """Tests for a successful (exit code 0) build."""

    EXIT_CODE = 0

    def test_runs_via_module_invocation_and_streams_output(self):
        """Worker should run `sys.executable -m PyInstaller <args>` and stream lines."""
        worker = PyInstallerWorker(["--name", "DemoApp", "script.py"])
        lines = []
        worker.output_signal.connect(lines.append)

        code = self._run_worker_and_wait(worker)

        self.assertEqual(code, 0)
        joined = "".join(lines)
        self.assertIn("stub pyinstaller: starting build", joined)
        # stderr output must have been captured too (merged stream, no deadlock)
        self.assertIn("stub pyinstaller: warning example", joined)
        self.assertIn("--name DemoApp script.py", joined)


class TestPyInstallerWorkerFailure(_StubPyInstallerOnPath):
    """Tests for a failed (non-zero exit code) build."""

    EXIT_CODE = 1

    def test_reports_nonzero_exit_code(self):
        """A failing PyInstaller invocation should report its real exit code."""
        worker = PyInstallerWorker(["script.py"])
        code = self._run_worker_and_wait(worker)
        self.assertEqual(code, 1)


class TestPyInstallerWorkerStop(unittest.TestCase):
    """Tests for cancellation support."""

    def setUp(self):
        """Ensure a QCoreApplication instance exists."""
        self.app = _ensure_qcoreapplication()

    def test_stop_without_running_process_does_not_raise(self):
        """Calling stop() before start() must be a safe no-op."""
        worker = PyInstallerWorker(["--version"])
        worker.stop()  # should not raise


if __name__ == "__main__":
    unittest.main()
