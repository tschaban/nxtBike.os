# nxtBike.os

Firmware for a custom eBike computer based on an ESP32-S3 DevKitC-1 with
16 MB flash and 8 MB PSRAM. The project uses ESP-IDF and its FreeRTOS runtime;
"OS" describes the planned device firmware and services, not a new kernel.

Current status: an initial boot application that reports chip information,
PSRAM size, and a heartbeat every 10 seconds. Display, sensors, ride tracking,
wireless connectivity, and bike communication are not implemented yet.

## Hardware

- ESP32-S3 with dual-core CPU, 2.4 GHz Wi-Fi, and Bluetooth 5 LE.
- Assumed module: ESP32-S3-WROOM-1-N16R8 (Quad flash, Octal PSRAM).
- USB-C connector and routing depend on the board vendor; verify the module
  marking and board schematic before flashing or assigning pins.
- Bluetooth Classic is not supported by ESP32-S3.

See [hardware notes](docs/HARDWARE.md) before connecting peripherals.

## Build and run

Install **PlatformIO IDE for VS Code**, then open this existing project folder.
Use PlatformIO's Build, Upload, and Serial Monitor actions, or open a
PlatformIO terminal and run:

```powershell
pio run
pio run -t upload
pio device monitor
```

PlatformIO detects the upload port automatically. If multiple devices are
connected, use `pio run -t upload --upload-port COM5` and
`pio device monitor --port COM5`, replacing `COM5` with your board's port.
Exit the monitor with `Ctrl+C`.
The initial configuration uses the default UART console; use the board's
USB-to-UART connector where available. A native-USB-only board requires a
matching console selection in `pio run -t menuconfig`.

`platformio.ini` pins the Espressif32 platform to **6.12.0**, which selects the
ESP-IDF 5.5.0 package series. PlatformIO manages the framework and toolchain;
a separate ESP-IDF installation is unnecessary. The project retains ESP-IDF
and FreeRTOS as its framework. See the
[PlatformIO ESP-IDF guide](https://docs.platformio.org/en/latest/frameworks/espidf.html)
and [pinned platform manifest](https://github.com/platformio/platform-espressif32/blob/v6.12.0/platform.json).

### Hardware and firmware profiles

`platformio.ini` only selects the default environment and includes configuration
files from `config/platformio/`:

| File | Responsibility |
| --- | --- |
| `common.ini` | Pinned platform, framework, build hooks, monitor speed |
| `hardware.ini` | Board templates, flash settings, partition layout |
| `profiles.ini` | Development/debug and production/release templates |
| `environments.ini` | Buildable combinations of hardware and profile |

The default is `nxtBike_os_S3_N16R8_dev`. The former environment name
`nxtBike_os_S3_N16R8` has been replaced by these explicit variants:

```sh
pio run -e nxtBike_os_S3_N16R8_dev
pio run -e nxtBike_os_S3_N16R8_prod
pio run -e nxtBike_os_S3_N16R8_dev -t upload
pio device monitor -e nxtBike_os_S3_N16R8_dev
```

Development enables INFO logs over UART0 at 115200 baud, bootloader logs,
and panic diagnostics. Production disables application and second-stage
bootloader logs, primary/secondary consoles, and panic output (silent reboot).
The immutable ROM can still print at reset: suppressing those messages requires
board-specific strapping or eFuse configuration. No eFuses are changed by this
project. Direct UART driver writes added by future code are independent of the
console configuration.

ESP-IDF defaults are loaded in order: shared `sdkconfig.defaults`, hardware
`config/sdkconfig/esp32s3-n16r8.defaults`, then `dev.defaults` or `prod.defaults`.
Each environment has separate `.pio/build/<environment>/` output and ignored
`sdkconfig.<environment>` settings, so switching profiles does not reuse the
other profile's configuration. Existing local sdkconfig values override defaults.
After changing defaults, back up any local menuconfig customizations, remove
only the affected `sdkconfig.<environment>` and `.pio/build/<environment>/`, then
rebuild. `pio run -t clean` alone does not reset sdkconfig. For a production
release, build with freshly generated configuration rather than local overrides.
Verify effective settings after building (CI runs these checks too):

```sh
python scripts/check_profile.py dev .pio/build/nxtBike_os_S3_N16R8_dev
python scripts/check_profile.py prod .pio/build/nxtBike_os_S3_N16R8_prod
```

To add hardware, create a template in `hardware.ini` and its ESP-IDF defaults
under `config/sdkconfig/`. Add combinations in `environments.ini` using `extends`
and list the shared, hardware, and profile files in `SDKCONFIG_DEFAULTS`.
To add a profile, add its template to `profiles.ini` and its own defaults file.
Add any new supported environment to the CI matrix as well. Paths are relative
to the project root, including paths in included INI files.

### Build troubleshooting

If the build reports `ModuleNotFoundError: No module named 'intelhex'`, the
pinned platform's esptool dependency is missing from its Python environment.
For the default Windows PlatformIO IDE installation, run in PowerShell:

```powershell
& "$env:USERPROFILE\.platformio\penv\Scripts\python.exe" -m pip install intelhex==2.3.0
```

Then build again. If the error comes from ESP-IDF's separate Python environment,
install the same package using the Python executable listed as `PYTHON` in
`.pio/build/<environment>/CMakeCache.txt`. GitHub Actions installs this dependency
explicitly. See the [upstream issue](https://github.com/platformio/platform-espressif32/issues/1632).

## Firmware version

Edit `version.json` to choose the major and minor numbers:

```json
{ "major": 1, "minor": 0 }
```

Every PlatformIO build invocation reserves the next local build number:
`1.0.0001`, `1.0.0002`, etc. An Upload that builds also increments it. Failed
attempts consume a number. Clean, menuconfig, and IDE indexing do not increment
it. The counter continues when you change major/minor; after 9999 it expands
to five digits.

The counter lives in ignored `.version/counter.txt`, outside `.pio`, so Clean
preserves it. Keep this file to preserve numbering. A fresh clone starts at 1;
local counters are independent across computers. Run only one build at a time
per checkout because the generated version file is shared.

The hook writes ignored `version.txt`, which ESP-IDF embeds in its standard
application descriptor inside `firmware.bin`. Firmware reads it with
`esp_app_get_description()->version` and prints it at startup in development builds. No filesystem
partition is needed. A matching `firmware-version.json` is generated beside
the binary in `.pio/build/<environment>/`.

GitHub Actions uses `run_number * 100 + run_attempt` as its build number, reserving
99 attempts per workflow run. Its metadata says `source: ci`; local builds say
`source: local`. CI numbers and local numbers are separate sequences and may
overlap. CI uploads the JSON with the firmware. `NXTB_BUILD_NUMBER` is reserved
for this explicit CI override and does not change the local counter.

Run versioning tests with `python -m unittest discover -s tests -v`.

## Repository

| Path | Purpose |
| --- | --- |
| `main/` | Boot application |
| `platformio.ini`, `config/platformio/` | Modular PlatformIO environments, hardware, and profiles |
| `CMakeLists.txt` | ESP-IDF project definition |
| `sdkconfig.defaults`, `config/sdkconfig/` | Shared, hardware, and profile ESP-IDF defaults |
| `partitions.csv` | NVS, PHY, and a 4 MiB factory application |
| `docs/ARCHITECTURE.md` | Boundaries for future firmware components |
| `docs/HARDWARE.md` | Board assumptions and pin constraints |
| `docs/ROADMAP.md` | Initial milestones |
| `CONTRIBUTING.md` | Development and verification workflow |

Remaining flash is unallocated. OTA and persistent ride storage need a planned
partition migration before implementation.

## Continuous integration

[Firmware CI](.github/workflows/firmware.yml) builds the ESP32-S3 firmware on
GitHub Actions for pushes and pull requests and saves the build artifacts.
CI builds both profiles, checks their effective logging/console settings, and
tests the version allocator. Firmware unit tests will be added as
application logic is implemented. See [Contributing](CONTRIBUTING.md#github-actions).

## License

[MIT](LICENSE), retaining the existing project copyright.
