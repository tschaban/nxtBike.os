# Lighting hardware

## Architecture

```text
20S battery --> fuse --> front-light branch (72 V reflector + 200 V MOSFET switch)
                                                           ^
12 V --> isolated gate driver -----------------------------+
                    ^
ESP32 --------------+

12 V --> fuse --> rear WS2815 strip
ESP32 RMT --> 74AHCT125 --> 68 ohm --> WS2815 data input

Brake switch --> independent red brake light
             +-> isolated ESP32 input --> WS2815 brake state
```

## Front light

The switching topology is undecided. The block diagram shows functional connections,
not the MOSFET position relative to the lamp or battery ground.

- Switch the existing 72 V reflector on the battery side; design for 84 V maximum pack voltage.
- Use an isolated gate driver powered from the existing 12 V rail.
- Use a MOSFET rated at least 200 V with current and thermal margin.
- Add a dedicated fuse close to the 72 V source.
- Keep a physical override independent from the touchscreen.
- Final MOSFET, fuse, topology, wire size and heat sinking require measured lamp current and confirmed ground wiring.

## Rear light

- Use an IP67 WS2815 12 V strip or sealed module.
- Translate 3.3 V data to 5 V with a 74AHCT125.
- Add a 33-100 ohm series data resistor and a bulk capacitor near the light.
- Use the strip's built-in backup data path; connect `DIN`/`BIN` according to the selected strip connector and its datasheet.
- Power it from the protected 12 V rail, not from the dashboard 5 V/3 A rail.

## Brake input and independent light

- Measure the brake-wire voltage before selecting the isolated input resistor or module.
- Keep the independent red tail/brake light on a hardware path independent of WS2815 data and ESP32 firmware.
- The independent brake-light path must work during ESP32 reset or WS2815 failure.

See [lighting control](../firmware/lighting-control.md) for output behavior.

See the [component list](components.md) for quantities and selected parts.
