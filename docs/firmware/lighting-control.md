# Lighting control

## Functions

| Function | Decision |
|---|---|
| Front light | Dashboard control plus a physical override |
| Rear position light | Constant red output from WS2815 |
| Brake light | Highest-priority bright red output |
| Decorative effects | Optional; cannot override position or brake functions |
| Failure fallback | Independent red tail/brake light remains available |

## Brake priority

```text
Brake > position light > user effects
```

- Do not infer braking only from BMS current or motor regeneration.

See [lighting hardware](../hardware/lighting.md) for wiring, power stages and components.
