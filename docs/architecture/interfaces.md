# Interface allocation

| Function | ESP32-S3 peripheral |
|---|---|
| DALY BMS | UART2 |
| Nextion | UART1 |
| Development diagnostics | USB Serial/JTAG; primary console and debugger |
| Future serial device | UART0; reserved, for example GNSS |
| Wheel sensor | Dedicated PCNT unit |
| PAS sensor | Separate dedicated PCNT unit |
| Temperature sensors | 1-Wire |
| Sabvoton HIGH/LOW | 2 x GPIO |
| Sabvoton LOW BRAKE | GPIO |
| Brake switch | GPIO |
| Front light | GPIO |
| Rear WS2815 | RMT |

## Acquisition and GPIO rules

- Use PCNT for distance and pulse count, with protected inputs and glitch filtering.
- Use pulse timestamps for stable low-speed calculation.
- Address both DS18B20 sensors and request conversion asynchronously; do not block a task while waiting.
- Keep the exact GPIO map open until the final PCB and connector layout are defined.
- Do not use GPIOs reserved by Flash, PSRAM or native USB.

## PCNT resource allocation

ESP32-S3 provides four independent PCNT units with two channels per unit.

| Logical allocation | Purpose |
|---|---|
| PCNT wheel unit | Wheel speed, distance and stopped state |
| PCNT PAS unit | Pedal cadence and forward-pedalling detection |
| Two remaining units | Reserved for motor Hall speed or future pulse sensors |

PCNT only measures pulses. Speed limiting and PAS decisions are made by the drive-state task; Sabvoton commands use separate GPIO outputs.

See [hardware architecture](../hardware/architecture.md) for system connections,
[PAS and speed modes](../firmware/pas-and-speed-modes.md) for drive interlocks,
and [optional hardware-dependent functions](../project/feature-scope.md#optional-hardware-dependent-functions)
for expansion interfaces.
