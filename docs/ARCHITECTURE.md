# Architecture

## Implemented foundation

ESP-IDF provides startup, memory initialization, peripheral APIs, and FreeRTOS.
`main/main.c` runs a minimal diagnostic loop. Wi-Fi and Bluetooth are not started.
No external peripherals or motor controls are driven.

## Planned boundaries

Add ESP-IDF components under `components/` as working features are introduced:

- **Board support:** verified pin definitions, power setup, and bus ownership.
- **Drivers:** display, buttons, sensors, and any external bus transceivers.
- **Services:** ride measurements, settings, storage, and connectivity.
- **User interface:** screen rendering and input handling.
- **Application:** startup order and coordination of services.

Keep hardware access in drivers and board support. Pass measurements through
explicit interfaces; use queues where tasks need asynchronous communication.
Assign task priorities, stack sizes, and sampling intervals based on measured
requirements. Avoid introducing a task for every feature by default.

## Open decisions

Display model and UI library, sensors, bike protocol, input controls, power
budget, persistent data format, and update strategy remain undecided. The
starter does not assume access to the bike's motor controller.
