# Software architecture

## Platform

- Target: ESP32-S3-WROOM-1-N16R8, dual core at up to 240 MHz.
- Keep the dashboard operational without Wi-Fi, BLE or a phone.

## Data flow

```text
Sensors and BMS -> acquisition tasks -> VehicleState -> UI / logger / network
                                |
                                +-> alarm manager
```

- `VehicleState` is the single normalized snapshot of current bicycle data.
- Drivers do not update Nextion or network clients directly.
- Use queues and event groups between acquisition, processing and output tasks.

## Core allocation

| CPU | Responsibilities |
|---|---|
| Core 0 | Wi-Fi, BLE, web API, OTA, log persistence and diagnostics |
| Core 1 | BMS processing, PAS state, drive-mode safety, lighting, vehicle state, alarms, calculated metrics and Nextion |

- Pin only time-critical vehicle tasks to Core 1.
- Leave non-critical tasks unpinned when fixed affinity is not required.
- Do not perform filesystem or network operations in sensor callbacks or interrupts.

## Priority order

1. Physical brake, PAS timeout and drive-disable state
2. BMS communication and alarms
3. Speed acquisition, speed mode and `VehicleState`
4. Brake and position lighting
5. Nextion updates
6. Logging
7. Wi-Fi, BLE and background services

See [interface allocation](interfaces.md) for hardware acquisition and output peripherals.
