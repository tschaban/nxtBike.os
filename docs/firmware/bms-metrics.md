# BMS metrics

## Symbols

| Symbol | Meaning | Unit |
|---|---|---|
| `Vpack` | Pack voltage | V |
| `I` | Signed pack current after direction validation | A |
| `SOC` | State of charge | % |
| `Vi` | Voltage of cell `i` | V |
| `Ti` | Temperature sensor `i` | °C |
| `N` | Number of series cells | count |
| `dt` | Sample interval | s |
| `v` | Bicycle speed | km/h |
| `d` | Distance | km |

The firmware should normalize current so that `Idischarge > 0` and `Icharge > 0`. The raw DALY current direction must be confirmed during bench testing.

## Metrics calculated from BMS data

| Metric | Required inputs | Formula or logic | Unit / note |
|---|---|---|---|
| Instantaneous pack power | `Vpack`, `I` | `P = Vpack × I` | W; retain direction for charge/discharge |
| Discharge power | `Vpack`, `Idischarge` | `Pdischarge = Vpack × Idischarge` | W |
| Charging power | `Vpack`, `Icharge` | `Pcharge = Vpack × Icharge` | W |
| Remaining charge | Remaining capacity | `Qremaining = remaining_mAh / 1000` | Ah |
| Cell-voltage spread | Highest and lowest cell voltage | `ΔVcell = Vmax - Vmin` | V or mV |
| Average cell voltage | All `Vi` | `Vavg = ΣVi / N` | V |
| Cell deviation from average | `Vi`, `Vavg` | `Vdeviation_i = Vi - Vavg` | V or mV |
| Relative cell imbalance | `Vmax`, `Vmin`, `Vavg` | `Imbalance = (Vmax - Vmin) / Vavg × 100` | % |
| Sum of cell voltages | All `Vi` | `Vcells = ΣVi` | V |
| Pack-voltage measurement difference | `Vpack`, all `Vi` | `Vdifference = Vpack - ΣVi` | V; diagnostic value |
| Average BMS temperature | All `Ti` | `Tavg = ΣTi / sensor_count` | °C |
| Temperature spread | Highest and lowest temperature | `ΔT = Tmax - Tmin` | °C |
| Temperature change rate | Current and previous temperature | `Temperature_rate = (Tnow - Tprevious) / elapsed_minutes` | °C/min |
| Active balancing count | Balance bits | `Nbalancing = Σ(active balance bits)` | Number of cells |
| Charged capacity | Current samples | `Ah_in += Icharge × dt / 3600` | Ah, accumulated over time |
| Discharged capacity | Current samples | `Ah_out += Idischarge × dt / 3600` | Ah, accumulated over time |
| Charged energy | Charging-power samples | `Wh_in += Pcharge × dt / 3600` | Wh, accumulated over time |
| Discharged energy | Discharge-power samples | `Wh_out += Pdischarge × dt / 3600` | Wh, accumulated over time |
| Approximate remaining energy | `Vpack`, `Qremaining` | `Eremaining ≈ Vpack × Qremaining` | Wh; estimate because pack voltage changes under load |
| Approximate time to empty | `Qremaining`, stable `Idischarge` | `Time_empty ≈ Qremaining / Idischarge` | Hours; valid only for a reasonably stable load |
| Approximate time to full | Configured full capacity, `Qremaining`, stable `Icharge` | `Time_full ≈ (Qfull - Qremaining) / Icharge` | Hours; excludes charge-current tapering |
| SOC change rate | Two SOC samples | `SOC_rate = (SOCnow - SOCprevious) / elapsed_hours` | %/h |
| Peak discharge current | Current history | `Ipeak = max(Idischarge)` | A |
| Peak discharge power | Power history | `Ppeak = max(Pdischarge)` | W |
| Minimum pack voltage | Voltage history | `Vpack_min = min(Vpack)` | V |
| Estimated pack resistance | Voltage and current before/after a load step | `Rpack ≈ abs(ΔVpack / ΔI)` | Ω; diagnostic estimate, not a direct BMS measurement |
| Estimated state of health | Measured full-cycle discharged capacity, rated capacity | `SOH_est ≈ Qmeasured / Qrated × 100` | %; requires a controlled near-full discharge cycle |

For energy integration, trapezoidal integration may be used for better accuracy:

`Wh += ((Pprevious + Pnow) / 2) × dt / 3600`

## Metrics requiring BMS and bicycle data

These values also require speed or distance from the wheel Hall sensor.

| Metric | Required inputs | Formula or logic | Unit / note |
|---|---|---|---|
| Energy consumption | `Wh_out`, `d` | `Consumption = Wh_out / d` | Wh/km |
| Regenerated energy per distance | `Wh_in`, `d` | `Regeneration = Wh_in / d` | Wh/km; only applicable if the controller supports regenerative braking |
| Net trip energy | `Wh_out`, `Wh_in`; integrators reset at trip start | `Wh_net = Wh_out - Wh_in` | Wh; also called `Trip_energy` |
| Average trip power | `Wh_net`, trip time | `Pavg = Wh_net / trip_time_hours` | W |
| Estimated remaining range | `Eremaining`, recent average consumption | `Range ≈ Eremaining / Consumption_recent` | km |
| Capacity used per trip | Capacity integrators reset at trip start | `Trip_capacity = Ah_out - Ah_in` | Ah |

Range must not be calculated until enough distance has been travelled to obtain a stable recent consumption value.

The [DALY protocol reference](daly-protocol.md) defines raw measurements, formats and alarms.
