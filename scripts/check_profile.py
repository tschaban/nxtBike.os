"""Check effective ESP-IDF settings after building a firmware profile."""
import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile", choices=("dev", "prod"))
    parser.add_argument("build_dir", type=Path)
    args = parser.parse_args()
    config = json.loads((args.build_dir / "config/sdkconfig.json").read_text())
    production = args.profile == "prod"
    expected = {
        "LOG_DEFAULT_LEVEL": 0 if production else 3,
        "LOG_MAXIMUM_LEVEL": 0 if production else 3,
        "BOOTLOADER_LOG_LEVEL": 0 if production else 3,
        "ESP_CONSOLE_SECONDARY_NONE": True,
        "ESP_CONSOLE_NONE" if production else "ESP_CONSOLE_UART_DEFAULT": True,
        "ESP_SYSTEM_PANIC_SILENT_REBOOT" if production else
        "ESP_SYSTEM_PANIC_PRINT_REBOOT": True,
    }
    errors = [f"{key}: expected {value!r}, got {config.get(key)!r}"
              for key, value in expected.items() if config.get(key) != value]
    if errors:
        parser.exit(1, "Profile validation failed:\n" + "\n".join(errors) + "\n")
    print(f"{args.profile}: effective logging, console and panic settings verified")


if __name__ == "__main__":
    main()
