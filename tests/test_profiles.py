import csv
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check_profile import validate


class ProfileTests(unittest.TestCase):
    def test_partition_layout_reserves_arduino_boot_app0(self):
        partition_file = (Path(__file__).resolve().parents[1]
                          / "config/partitions/esp32s3-n16r8.csv")
        # PlatformIO's Arduino uploader writes boot_app0.bin over this range.
        reserved_start, reserved_end = 0xE000, 0x10000
        ota_regions = []
        with partition_file.open(encoding="utf-8") as source:
            for row in csv.reader(line for line in source
                                  if line.strip() and not line.lstrip().startswith("#")):
                name, kind, subtype, offset, size = [cell.strip() for cell in row[:5]]
                start = int(offset, 0)
                end = start + int(size, 0)
                if kind == "data" and subtype == "ota":
                    ota_regions.append((start, end))
                else:
                    self.assertFalse(start < reserved_end and end > reserved_start,
                                     f"{name} overlaps Arduino boot_app0 upload")
        self.assertEqual(ota_regions, [(reserved_start, reserved_end)])

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in ("firmware.bin", "firmware.elf"):
            (self.root / name).write_bytes(b"test artifact")

    def metadata(self, profile="dev"):
        return {
            "profile": profile, "framework": ["arduino"],
            "memory_type": "qio_opi", "flash_size": "16MB",
            "defines": {"CORE_DEBUG_LEVEL": "0" if profile == "prod" else "3",
                        "NXTB_DIAGNOSTICS": "0" if profile == "prod" else "1",
                        "BOARD_HAS_PSRAM": None},
        }

    def write_metadata(self, data):
        (self.root / "firmware-profile.json").write_text(json.dumps(data), encoding="utf-8")

    def test_both_profiles(self):
        for profile in ("dev", "prod"):
            with self.subTest(profile=profile):
                self.write_metadata(self.metadata(profile))
                self.assertEqual(validate(profile, self.root), [])

    def test_wrong_profile(self):
        self.write_metadata(self.metadata("dev"))
        errors = validate("prod", self.root)
        self.assertTrue(any("profile:" in error for error in errors))
        self.assertTrue(any("NXTB_DIAGNOSTICS:" in error for error in errors))

    def test_incompatible_framework_or_board(self):
        for key, value in (("framework", ["espidf"]),
                           ("framework", ["arduino", "espidf"]),
                           ("memory_type", "qio_qspi"), ("flash_size", "8MB")):
            with self.subTest(key=key, value=value):
                data = self.metadata()
                data[key] = value
                self.write_metadata(data)
                self.assertTrue(any(key in error for error in validate("dev", self.root)))

    def test_missing_and_incorrect_defines(self):
        for key in ("CORE_DEBUG_LEVEL", "NXTB_DIAGNOSTICS", "BOARD_HAS_PSRAM"):
            with self.subTest(key=key):
                data = self.metadata()
                del data["defines"][key]
                self.write_metadata(data)
                self.assertTrue(any(key in error for error in validate("dev", self.root)))
        for key in ("CORE_DEBUG_LEVEL", "NXTB_DIAGNOSTICS"):
            data = self.metadata()
            data["defines"][key] = "0"
            self.write_metadata(data)
            self.assertTrue(any(key in error for error in validate("dev", self.root)))

    def test_missing_and_empty_artifacts(self):
        self.write_metadata(self.metadata())
        (self.root / "firmware.bin").unlink()
        (self.root / "firmware.elf").write_bytes(b"")
        errors = validate("dev", self.root)
        self.assertEqual(len(errors), 2)
        self.assertTrue(any("firmware.bin" in error for error in errors))
        self.assertTrue(any("firmware.elf" in error for error in errors))

    def test_missing_and_malformed_metadata(self):
        self.assertTrue(validate("dev", self.root))
        (self.root / "firmware-profile.json").write_text("{broken", encoding="utf-8")
        self.assertTrue(validate("dev", self.root))
        for data in ([], {"defines": []}):
            self.write_metadata(data)
            self.assertTrue(validate("dev", self.root))

    def test_cli_exit_status(self):
        checker = Path(__file__).resolve().parents[1] / "scripts/check_profile.py"
        self.write_metadata(self.metadata())
        for profile, status in (("dev", 0), ("prod", 1)):
            result = subprocess.run([sys.executable, str(checker), profile, str(self.root)],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, status, result.stderr)
            self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
