# Build and flash

Install [PlatformIO Core](https://docs.platformio.org/en/latest/core/installation/index.html).
Run commands from the repository root, one build at a time.

Build the development or production profile:

```sh
pio run -e nxtBike_os_S3_N16R8_dev
pio run -e nxtBike_os_S3_N16R8_prod
```

Development prints application diagnostics on UART0 at 115200 baud. Production
disables application diagnostics; framework boot and panic output may remain.

With the board connected, upload and monitor the development profile:

```sh
pio run -e nxtBike_os_S3_N16R8_dev -t upload
pio device monitor -e nxtBike_os_S3_N16R8_dev
```

Use `nxtBike_os_S3_N16R8_prod` to upload production firmware. OTA is not implemented.
