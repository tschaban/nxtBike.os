# PAS and speed modes

## Scope

- Controller: Sabvoton `SVMC072080`.
- The physical throttle remains the torque request.
- Throttle operation is permitted only during valid forward pedalling.
- ESP32 does not generate an analog throttle signal.
- The dashboard selects low, middle or high Sabvoton mode.

## Sabvoton 3-speed switch mode

| Selected mode | LOW SPEED input | HIGH SPEED input |
|---|---|---|
| Low | Connected to Sabvoton GND | Open |
| Middle | Open | Open |
| High | Open | Connected to Sabvoton GND |

- Configure `3-speed (switch)` in the Sabvoton software.
- Never connect both mode inputs to ground.
- Select low mode after startup and as the software fault fallback.
- A mode change affects the Sabvoton limit only; it does not bypass PAS or brake state.
- Brake, invalid PAS, sensor timeout and critical faults override every drive-mode request.
- Energize the enable relay only while forward pedalling is valid and no blocking fault exists.

## PAS state machine

| Condition | Decision |
|---|---|
| Startup | Drive disabled |
| At least two valid forward pulses | Pedalling valid; release `LOW BRAKE` |
| No PAS pulse for 400-700 ms | Apply `LOW BRAKE` |
| Reverse pedal direction | Apply `LOW BRAKE` |
| Physical brake active | Apply brake independently of ESP32 |
| Invalid sensor state | De-energize the relay; NC contact disables drive |
| ESP32 reset or power loss | De-energized NC relay disables drive; inactive speed outputs select middle mode |

The exact PAS timeout is calibrated after the sensor pole count and minimum usable cadence are known.

## Deferred

- Automatic assistance without using the throttle.
- Torque-sensor proportional assistance.
- Sabvoton configuration or telemetry over its service port.

See [PAS and speed-mode hardware](../hardware/pas-and-speed-interface.md) for wiring and components.
