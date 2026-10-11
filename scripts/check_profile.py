"""Check Arduino build metadata and firmware artifacts after a profile build."""
import argparse
import json
from pathlib import Path


def validate(profile, build_dir):
    """Return configuration/artifact errors; this does not test board behavior."""
    build_dir = Path(build_dir)
    try:
        config = json.loads((build_dir / "firmware-profile.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        return [f"Cannot read firmware-profile.json: {error}"]
    if not isinstance(config, dict):
        return ["firmware-profile.json must contain an object"]
    expected = {
        "profile": profile,
        "framework": ["arduino"],
        "memory_type": "qio_opi",
        "flash_size": "16MB",
    }
    errors = [f"{key}: expected {value!r}, got {config.get(key)!r}"
              for key, value in expected.items() if config.get(key) != value]
    defines = config.get("defines")
    if not isinstance(defines, dict):
        errors.append("defines must contain an object")
    else:
        for key, value in {
            "CORE_DEBUG_LEVEL": "0" if profile == "prod" else "3",
            "NXTB_DIAGNOSTICS": "0" if profile == "prod" else "1",
        }.items():
            if defines.get(key) != value:
                errors.append(f"{key}: expected {value!r}, got {defines.get(key)!r}")
        if "BOARD_HAS_PSRAM" not in defines:
            errors.append("BOARD_HAS_PSRAM is missing")
    for name in ("firmware.bin", "firmware.elf"):
        artifact = build_dir / name
        if not artifact.is_file() or artifact.stat().st_size == 0:
            errors.append(f"{name}: missing or empty build artifact")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile", choices=("dev", "prod"))
    parser.add_argument("build_dir", type=Path)
    args = parser.parse_args()
    errors = validate(args.profile, args.build_dir)
    if errors:
        parser.exit(1, "Profile validation failed:\n" + "\n".join(errors) + "\n")
    print(f"{args.profile}: Arduino build metadata and firmware artifacts verified")


if __name__ == "__main__":
    main()
