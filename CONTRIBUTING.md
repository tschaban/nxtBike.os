# Contributing

Use PlatformIO with the pinned `nxtBike_os_S3_N16R8` environment in `platformio.ini`. Keep commits
focused and document changes to wiring, dependencies, and persisted data.

## Workflow

1. Create a branch for the change.
2. Follow `.editorconfig`; use four-space indentation in C.
3. Run `pio run` from a PlatformIO terminal.
4. For hardware changes, flash the target and record the board revision,
   wiring, expected behavior, and observed serial output.
5. Include verification results and remaining limitations in the pull request.

Add unit tests for calculation and protocol logic when introduced. Validate
timing, power, and electrical behavior on hardware. A successful build alone
does not verify a peripheral.

## GitHub Actions

`.github/workflows/firmware.yml` builds the `nxtBike_os_S3_N16R8` environment on pushes
and pull requests, and supports manual runs. It saves firmware binaries and
debug symbols as a downloadable artifact for 14 days. Reproduce the build
locally with `pio run -e nxtBike_os_S3_N16R8`.

CI also runs Python unit tests for version allocation. Firmware application
logic has no unit-test suite yet. Once testable application logic exists,
add a PlatformIO `native` environment and a separate
CI job running `pio test -e native`. Do not make an empty test suite report
success. Tests requiring real ESP32 peripherals need a connected board and a
dedicated hardware runner or local execution.

The workflow becomes active once committed and pushed to GitHub. Repository
branch protection can then require the `Build ESP32-S3 firmware` check before
merging; that repository setting is not configured by this file.

Keep credentials, generated output, and machine-specific configuration out of
Git. Put shared configuration changes in `sdkconfig.defaults`; review generated
defaults before committing. Preserve the existing MIT license.
