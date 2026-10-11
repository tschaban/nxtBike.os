# Firmware versioning

Edit `major` and `minor` in [`config/version.json`](../../config/version.json),
then [build normally](../getting-started/build-and-flash.md). The build number is
assigned automatically. Find the full `major.minor.build` version in
`.pio/build/<environment>/firmware-version.json` for your selected build environment.

Firmware code reads the version string through `NXTB_FIRMWARE_VERSION`.
For logging after serial initialization:

```cpp
const char* firmwareVersion = NXTB_FIRMWARE_VERSION;
Serial.printf("Firmware: %s\n", firmwareVersion);
```

Pass the same `firmwareVersion` string to your display code to show it on screen.
