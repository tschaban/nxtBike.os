"""Version allocation shared by the PlatformIO hook and its tests."""
import json
from pathlib import Path


def allocate(root, build_override=None):
    root = Path(root)
    config = json.loads((root / "version.json").read_text(encoding="utf-8"))
    for field in ("major", "minor"):
        value = config.get(field)
        if type(value) is not int or not 0 <= value <= 999:
            raise ValueError(f"version.json: {field} must be an integer from 0 to 999")

    state_dir = root / ".version"
    state_dir.mkdir(exist_ok=True)
    lock = state_dir / "lock"
    try:
        lock.mkdir()
    except FileExistsError as exc:
        raise RuntimeError("Version allocation is locked. If no build is running, remove .version/lock.") from exc
    try:
        state = state_dir / "counter.txt"
        if build_override is None:
            previous = int(state.read_text()) if state.exists() else 0
            if previous < 0:
                raise ValueError("Invalid negative build counter")
            build = previous + 1
        else:
            build = int(build_override)
            if build < 1:
                raise ValueError("NXTB_BUILD_NUMBER must be positive")
        version = f"{config['major']}.{config['minor']}.{build:04d}"
        if len(version) > 31:
            raise ValueError("Version exceeds ESP-IDF's 31-character limit")
        if build_override is None:
            temporary = state.with_suffix(".tmp")
            temporary.write_text(str(build) + "\n", encoding="utf-8")
            temporary.replace(state)
        return dict(config, build=build, version=version,
                    source="ci" if build_override is not None else "local")
    finally:
        lock.rmdir()
