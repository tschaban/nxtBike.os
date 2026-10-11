# Contributing

Use PlatformIO with environments defined in
[environments.ini](config/platformio/environments.ini). Keep changes focused.

## Workflow

1. Create a branch for the change.
2. Follow `.editorconfig`; use four-space indentation in C/C++.
3. Run relevant [automated tests](tests/).
4. Build affected profiles defined in [environments.ini](config/platformio/environments.ini).
5. For hardware changes, record board revision, wiring, expected behavior, and
   observed results. A successful build alone does not verify a peripheral.
6. Update affected documents using the [documentation standard](docs/documentation-standard.md).
7. Include verification results and remaining limitations in the pull request.

## Documentation and design

Document current behavior and keep requested placeholders empty of body content.
Do not turn suggestions into accepted requirements or add speculative designs,
ownership notes, or work-tracking commentary. Put technical specifications in
the relevant document, such as the [architecture overview](docs/architecture/overview.md).
Omit separate decision records, rationale, and alternatives unless requested.

## Configuration and CI

The [firmware workflow](.github/workflows/firmware.yml) defines automated build checks.
Keep credentials, generated output, and machine-specific configuration out of Git.
Put shared, hardware, and profile configuration in `config/platformio/`.
Preserve the existing MIT license.
