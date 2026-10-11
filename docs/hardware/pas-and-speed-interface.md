# PAS and speed-mode hardware

## Architecture

```text
Directional PAS --> separate protected PCNT unit --> PAS state machine
                                                |
                                                +--> fail-safe NC relay --> Sabvoton LOW BRAKE

Nextion --> mode request --> interlock --> 2 x isolated open-drain output
                                             |                |
                                             +--> LOW SPEED    +--> HIGH SPEED
```

## Fail-safe output

- Use the Sabvoton `LOW BRAKE` input only as a motor cut-off, without automatic regeneration.
- A normally-closed signal relay connects `LOW BRAKE` to Sabvoton GND when its coil is not energized.
- Physical brake switches remain connected directly to Sabvoton; ESP32 or firmware failure must not disable this path.

See [PAS and speed modes](../firmware/pas-and-speed-modes.md) for control behavior.

See the [component list](components.md) for quantities and selected parts.
