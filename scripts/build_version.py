"""PlatformIO PRE hook: reserve one version per build invocation."""
import json
import os
from pathlib import Path
import runpy

Import("env")

def prepare_version():
    # These commands must not consume a build number.
    targets = set(COMMAND_LINE_TARGETS)
    if env.IsIntegrationDump() or targets.intersection(
        {"clean", "idedata", "menuconfig", "erase", "nobuild", "uploadfs", "buildfs"}
    ):
        return
    root = Path(env.subst("$PROJECT_DIR"))
    allocate = runpy.run_path(str(root / "scripts" / "versioning.py"))["allocate"]
    info = allocate(root, os.environ.get("NXTB_BUILD_NUMBER"))
    build_dir = Path(env.subst("$BUILD_DIR"))
    build_dir.mkdir(parents=True, exist_ok=True)
    (root / "version.txt").write_text(info["version"] + "\n", encoding="utf-8")
    # PlatformIO 6.12 checks this directory's mtime, but not version.txt,
    # when deciding whether to refresh ESP-IDF's CMake compilation flags.
    config_dir = build_dir / "config"
    if config_dir.exists():
        os.utime(config_dir, None)
    (build_dir / "firmware-version.json").write_text(
        json.dumps(info, indent=2) + "\n", encoding="utf-8"
    )
    print("nxtBike.os firmware version: " + info["version"])


prepare_version()
