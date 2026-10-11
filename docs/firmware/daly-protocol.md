# DALY BMS protocol

The DALY UART/RS485 protocol uses data IDs `0x90` through `0x98`.
Optional fields and current direction require verification on the installed BMS.

## Information read directly from the BMS

| Data ID | Information | Resolution / format |
|---|---|---|
| `0x90` | Total pack voltage | 0.1 V |
| `0x90` | Acquisition pack voltage | 0.1 V |
| `0x90` | Charge/discharge current | 0.1 A, raw value uses a 30000 offset |
| `0x90` | State of charge | 0.1% |
| `0x91` | Highest cell voltage and its cell number | 1 mV |
| `0x91` | Lowest cell voltage and its cell number | 1 mV |
| `0x92` | Highest temperature and its sensor number | 1°C, raw value uses a 40°C offset |
| `0x92` | Lowest temperature and its sensor number | 1°C, raw value uses a 40°C offset |
| `0x93` | Operating state | Stationary, charging or discharging |
| `0x93` | Charge MOSFET state | On/off |
| `0x93` | Discharge MOSFET state | On/off |
| `0x93` | BMS life field | 0-255; exact meaning must be verified on this BMS |
| `0x93` | Remaining capacity | mAh |
| `0x94` | Number of series cells | Count; expected value is 20 |
| `0x94` | Number of BMS temperature sensors | Count |
| `0x94` | Charger connection state | Connected/disconnected |
| `0x94` | Load connection state | Connected/disconnected |
| `0x94` | Optional digital input/output states | DI1-DI4 and DO1-DO4 |
| `0x95` | Individual voltage of every cell | 1 mV; 20 values for this battery |
| `0x96` | Individual BMS temperature readings | 1°C |
| `0x97` | Balancing state of every cell | Active/inactive bit per cell |
| `0x98` | Alarm flags, protection states and fault code | Bit fields |

## Available alarms and faults

| Category | Alarm or fault flags |
|---|---|
| Cell voltage | Cell overvoltage levels 1 and 2; cell undervoltage levels 1 and 2 |
| Pack voltage | Pack overvoltage levels 1 and 2; pack undervoltage levels 1 and 2 |
| Charge temperature | High-temperature levels 1 and 2; low-temperature levels 1 and 2 |
| Discharge temperature | High-temperature levels 1 and 2; low-temperature levels 1 and 2 |
| Current | Charge overcurrent levels 1 and 2; discharge overcurrent levels 1 and 2 |
| State of charge | High-SOC levels 1 and 2; low-SOC levels 1 and 2 |
| Differences | Cell-voltage difference levels 1 and 2; temperature difference levels 1 and 2 |
| MOSFETs | Charge/discharge MOSFET overtemperature, temperature-sensor error, adhesion error and open-circuit error |
| Sensors and storage | AFE acquisition error, voltage acquisition disconnection, cell-temperature sensor error, EEPROM error and RTC error |
| System | Precharge failure, external/internal communication failure, current-module fault, total-voltage detection fault, short-circuit protection and charging blocked by low voltage |
| General | BMS fault code |

## Communication basics

| Setting | Value |
|---|---|
| Interface | DALY UART/RS485 protocol |
| Serial configuration | 9600 baud, 8 data bits, no parity, 1 stop bit |
| Request address | `0x40` for upper-computer communication |
| Response address | `0x01` for the BMS master |
| Frame checksum | Low byte of the sum of all preceding frame bytes |

## References

- [DALY communication protocol overview](https://www.dalybms.com/pl/news/daly-three-communication-protocols-explanation/)
- [DALY UART/485 Communications Protocol V1.2](https://support.wirenboard.com/uploads/short-url/fF9iaKrYEuvAMgvJ3AfrPGHaULX.pdf)


See [BMS metrics](bms-metrics.md) for calculations using these values.
