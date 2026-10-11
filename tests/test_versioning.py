import json
import os
from pathlib import Path
import sys
import runpy
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from versioning import allocate


class VersionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.configure(1, 0)

    def configure(self, major, minor):
        config = self.root / "config"
        config.mkdir(exist_ok=True)
        (config / "version.json").write_text(json.dumps(dict(major=major, minor=minor)))

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
        for target in ("clean", "idedata", "nobuild"):
            # No subst() method: any attempt to allocate would fail this test.
            runpy.run_path(str(hook), init_globals={
                "Import": lambda name: None, "env": EditorEnv(),
                "COMMAND_LINE_TARGETS": [target],
            })

    def test_build_hook_keeps_version_outputs_consistent(self):
        scripts = Path(__file__).resolve().parents[1] / "scripts"
        (self.root / "scripts").mkdir()
        (self.root / "scripts/versioning.py").write_bytes(
            (scripts / "versioning.py").read_bytes())
        build_dir = self.root / "build"
        root = self.root

        class BuildEnv(dict):
            def IsIntegrationDump(self):
                return False

            def subst(self, value):
                return str({"$PROJECT_DIR": root, "$BUILD_DIR": build_dir}[value])

            def StringifyMacro(self, value):
                return json.dumps(value)

            def Append(self, **values):
                for key, value in values.items():
                    self.setdefault(key, []).extend(value)

        for build in (1, 2):
            env = BuildEnv()
            with patch.dict(os.environ, {}, clear=True):
                runpy.run_path(str(scripts / "build_version.py"), init_globals={
                    "Import": lambda name: None, "env": env,
                    "COMMAND_LINE_TARGETS": [],
                })
            expected = f"1.0.{build:04d}"
            self.assertFalse((root / "version.txt").exists())
            manifest = json.loads((build_dir / "firmware-version.json").read_text())
            self.assertEqual(manifest["version"], expected)
            self.assertEqual(manifest["build"], build)
            self.assertEqual(dict(env["CPPDEFINES"])["NXTB_FIRMWARE_VERSION"],
                             json.dumps(expected))
            self.assertIn("-Wl,--undefined=nxtbike_firmware_version", env["LINKFLAGS"])


if __name__ == "__main__":
    unittest.main()
