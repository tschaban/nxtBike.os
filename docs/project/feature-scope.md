# Feature scope

The [current firmware entry point](../../main/main.cpp) implements startup diagnostics
and a periodic heartbeat.

## First release

| Area | Included |
|---|---|
| Dashboard | Speed, distance, ride time, battery state and temperatures |
| BMS | Pack voltage/current/SOC, power, cells, MOSFET state and DALY alarms |
| Calculations | Trip energy, Wh/km, estimated range and cell voltage delta |
| Diagnostics | Communication state, data age, sensor validity and firmware version |
| Storage | Odometer, settings, calibration, ride summary and recent alarms |
| Pedal assistance | Throttle is enabled only while valid forward pedalling is detected |
| Drive modes | Low, middle and high Sabvoton speed modes selected from the dashboard |
| Lighting | Front light, rear position light and brake-light priority |

## Planned

| Area | Functions |
|---|---|
| Connectivity | Wi-Fi configuration portal, web dashboard, log download and OTA |
| Telemetry | Optional BLE data service for a phone |
| History | Ride charts, charging sessions and battery-health trends |
| Maintenance | Weak-cell trend detection and service diagnostics |

## Optional hardware-dependent functions

| Addition | Functions enabled |
|---|---|
| microSD socket | Detailed long-term ride logging |
| GNSS receiver on reserved UART0 | Position, route, time and independent speed |
| I2C IMU | Movement, tilt, impact and theft detection |
| External TWAI/CAN transceiver | Future motor-controller integration |
| Ambient-light sensor | Automatic display brightness |

## Excluded from the first release

- Writing configuration to the DALY BMS.
- Generated throttle control or automatic assistance without the physical throttle.
- Changes to Sabvoton motor, current or regenerative-braking parameters while riding.
- Cloud dependency for normal dashboard operation.
- AI processing without a defined bicycle use case.
