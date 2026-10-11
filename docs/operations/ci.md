# Continuous integration

The [Firmware CI workflow](../../.github/workflows/firmware.yml) runs on pushes,
pull requests, and manual dispatch. It builds Arduino-ESP32 firmware with
PlatformIO for both environments:

- `nxtBike_os_S3_N16R8_dev`
- `nxtBike_os_S3_N16R8_prod`

Each job checks the build profile and firmware artifacts, runs Python tooling
tests, and checks documentation structure and local links. CI does not flash or
test a physical board.

To download build outputs, open **Actions → Firmware CI → a completed run →
Artifacts**. Each environment's artifact contains the generated `.bin` files,
`firmware.elf` debug symbols, `firmware-version.json`, and
`firmware-profile.json`. Artifacts are retained for 14 days.
