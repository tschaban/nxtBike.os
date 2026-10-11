"""Record effective Arduino build settings for profile verification."""
import json
from pathlib import Path

Import("env")

defines = {}
for item in env.get("CPPDEFINES", []):
    if isinstance(item, (tuple, list)):
        defines[str(item[0])] = str(item[1]) if len(item) > 1 else None
    else:
        defines[str(item)] = None

board = env.BoardConfig()
metadata = {
    "profile": env.GetProjectOption("custom_profile"),
    "framework": list(env.get("PIOFRAMEWORK", [])),
    "defines": defines,
    "memory_type": board.get("build.arduino.memory_type"),
    "flash_size": board.get("upload.flash_size"),
}
build_dir = Path(env.subst("$BUILD_DIR"))
build_dir.mkdir(parents=True, exist_ok=True)
(build_dir / "firmware-profile.json").write_text(
    json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
)
