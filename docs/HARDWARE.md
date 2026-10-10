# Hardware baseline

The initial configuration assumes **ESP32-S3-WROOM-1-N16R8**, with 16 MB Quad
SPI flash and 8 MB Octal SPI PSRAM. Verify the physical module marking:
WROOM-2 variants such as N16R8V have different flash and voltage requirements
and must not be treated as interchangeable.

## Pin planning

- Reserve GPIO35, GPIO36, and GPIO37 for internal memory on Octal PSRAM modules.
- GPIO19 and GPIO20 are native USB D- and D+; reserve them if using native USB.
- Review strapping pins GPIO0, GPIO3, GPIO45, and GPIO46 before wiring inputs.
- Check the exact board schematic for its RGB LED, UART bridge, and USB routing.
- No display, sensor, button, or bike-bus pins are assigned by this starter.

## Power and interfaces

Use a regulated supply suitable for the board. An eBike battery requires an
appropriately rated DC/DC supply; do not connect it directly to the board.
GPIO signals use 3.3 V logic. Select the required transceiver and electrical
protection after identifying the bike's actual communication interface.

## First boot checklist

1. Confirm the module marking and USB connector function.
2. Build and flash using the pinned PlatformIO environment.
3. Confirm the log reports 8,388,608 bytes of PSRAM.
4. Confirm a heartbeat every 10 seconds and no reset loop.
5. Record board revision and peripheral wiring here as hardware is selected.

## References

- [Espressif DevKitC-1 user guide](https://documentation.espressif.com/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/user_guide_v1.0.html)
- [ESP32-S3 flash and PSRAM configuration](https://docs.espressif.com/projects/esp-idf/en/v5.4.2/esp32s3/api-guides/flash_psram_config.html)
- [ESP-IDF configuration reference](https://docs.espressif.com/projects/esp-idf/en/v5.4.2/esp32s3/api-reference/kconfig.html)
