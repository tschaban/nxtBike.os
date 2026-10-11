# Automated tests

## Select checks

- Tooling changes: run the Python suite. It covers versioning, profiles,
  partitions, and documentation tooling.
- Documentation changes: run the documentation checker.
- Firmware or build configuration changes: build dev and prod using the
  [build instructions](../getting-started/build-and-flash.md), then check each
  profile. Run one firmware build at a time per workspace.

Run from the repository root:

```sh
python -m unittest discover -s tests -v
python scripts/check_docs.py
```

After firmware builds:

```sh
python scripts/check_profile.py dev .pio/build/nxtBike_os_S3_N16R8_dev
python scripts/check_profile.py prod .pio/build/nxtBike_os_S3_N16R8_prod
```

See [continuous integration](../operations/ci.md) for automated execution.

## Test approach

No native C++ test environment or automated board tests are configured.
For new portable firmware logic, prefer host tests with controlled time, inputs,
and hardware substitutes. Keep tests deterministic; avoid real delays.

Test observable behavior, boundaries, and meaningful failure paths. Add a
regression test for a reproducible bug where practical. Do not mirror
implementation details, invent feature requirements, or add tests solely to
meet a coverage percentage.

Use physical-board tests for boot, PSRAM, peripherals, timing, and recovery
claims that host tests cannot establish. Flash only when authorized. Give
automated board checks explicit success criteria and timeouts; capture serial
logs and firmware identity. Production disables application diagnostics, so
serial silence is not proof of successful boot.

## Report evidence

Report commands, results, tested profile/artifact, and unverified behavior.
Distinguish host tests, compilation, profile/artifact checks, and board results.
Successful builds and metadata checks do not prove runtime behavior. Results
from a test firmware image do not validate the production image.
