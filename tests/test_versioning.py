import json
from pathlib import Path
import sys
import runpy
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from versioning import allocate


class VersionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.configure(1, 0)

    def configure(self, major, minor):
        (self.root / "version.json").write_text(json.dumps(dict(major=major, minor=minor)))

    def test_increment_and_manual_change(self):
        self.assertEqual(allocate(self.root)["version"], "1.0.0001")
        self.assertEqual(allocate(self.root)["version"], "1.0.0002")
        self.configure(2, 3)
        self.assertEqual(allocate(self.root)["version"], "2.3.0003")

    def test_ci_does_not_change_local_counter(self):
        self.assertEqual(allocate(self.root, "10001")["version"], "1.0.10001")
        self.assertEqual(allocate(self.root)["build"], 1)

    def test_invalid_config(self):
        self.configure(True, 0)
        with self.assertRaises(ValueError):
            allocate(self.root)

    def test_corrupt_counter_is_not_reset(self):
        allocate(self.root)
        (self.root / ".version/counter.txt").write_text("broken")
        with self.assertRaises(ValueError):
            allocate(self.root)

    def test_lock_prevents_double_allocation(self):
        (self.root / ".version/lock").mkdir(parents=True)
        with self.assertRaises(RuntimeError):
            allocate(self.root)

    def test_non_build_commands_do_not_allocate(self):
        class EditorEnv:
            def IsIntegrationDump(self):
                return False
        hook = Path(__file__).resolve().parents[1] / "scripts/build_version.py"
        for target in ("clean", "idedata", "menuconfig", "nobuild"):
            # No subst() method: any attempt to allocate would fail this test.
            runpy.run_path(str(hook), init_globals={
                "Import": lambda name: None, "env": EditorEnv(),
                "COMMAND_LINE_TARGETS": [target],
            })


if __name__ == "__main__":
    unittest.main()
