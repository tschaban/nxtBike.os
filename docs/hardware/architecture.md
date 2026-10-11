# Hardware architecture

## Block diagram

```text
20S battery
    +--> DALY BMS --> ADM2587E isolated RS485 --> ESP32-S3
    +--> Sabvoton SVMC072080 --------------------> motor
    +--> front-light branch

Existing protected 5 V / 3 A supply
        |
        +--> Nextion
        |
        +--> ESP32-S3 DevKit (on-board 3.3 V regulator)

Existing protected 12 V supply
        |
        +--> fused WS2815 rear RGB light
        +--> independent red tail/brake light

Hall speed sensor -------------------------------> ESP32-S3
Directional PAS sensor --------------------------> ESP32-S3
2 x DS18B20 -------------------------------------> ESP32-S3
Nextion UART <-----------------------------------> ESP32-S3

ESP32-S3 --> isolated HIGH/LOW outputs ----------> Sabvoton 3-speed inputs
ESP32-S3 --> fail-safe NC enable ----------------> Sabvoton LOW BRAKE
Brake switch --> isolated input -----------------> ESP32-S3
Brake switch ------------------------------------> independent brake light
ESP32-S3 --> rear-light data interface ----------> WS2815
```

## Requirements

- Use the existing protected 5 V / 3 A supply as the hardware power input.
- Keep DALY responsible for battery protection.
- Keep Sabvoton responsible for motor commutation, current limits and motor protection.
- Do not power the system from the BMS communication connector.
- Use waterproof connectors and ignition-controlled power.

See [component list](components.md), [lighting hardware](lighting.md) and
[PAS and speed-mode hardware](pas-and-speed-interface.md) for topic details.

See [interface allocation](../architecture/interfaces.md) for MCU peripherals.
