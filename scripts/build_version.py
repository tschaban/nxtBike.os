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
        {"clean", "idedata", "erase", "nobuild", "uploadfs", "buildfs"}
    ):
        return
    root = Path(env.subst("$PROJECT_DIR"))
    allocate = runpy.run_path(str(root / "scripts" / "versioning.py"))["allocate"]
    info = allocate(root, os.environ.get("NXTB_BUILD_NUMBER"))
    build_dir = Path(env.subst("$BUILD_DIR"))
    build_dir.mkdir(parents=True, exist_ok=True)
    env.Append(CPPDEFINES=[
        ("NXTB_FIRMWARE_VERSION", env.StringifyMacro(info["version"])),
    ])
    env.Append(LINKFLAGS=["-Wl,--undefined=nxtbike_firmware_version"])
    (build_dir / "firmware-version.json").write_text(
        json.dumps(info, indent=2) + "\n", encoding="utf-8"
    )
    print("nxtBike.os firmware version: " + info["version"])


prepare_version()
