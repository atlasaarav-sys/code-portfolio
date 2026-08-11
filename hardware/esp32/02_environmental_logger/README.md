# ESP32-02 — Environmental Logger

**Level:** Beginner-Intermediate
**Goal:** Battery-powered environmental sensor node: reads temperature,
humidity, and pressure over I2C, shows live readings on a small OLED, and
runs off a single-cell LiPo with USB charging.

## 1. Schematic — component & connection list

### Power
| Ref | Part | Value/Part # | Notes |
|---|---|---|---|
| J1 | USB-C receptacle (power only) | Molex 105450 | VBUS -> U2 (charger) IN, CC1/CC2 via 5.1k to GND |
| U2 | LiPo charge controller | MCP73831T-2ACI/OT | VBAT pin -> battery +, PROG pin -> R1 (sets charge current) -> GND, STAT -> LED via R2 |
| BT1 | JST-PH 2-pin battery connector | — | + -> U2 VBAT / power switch input, - -> GND |
| SW1 | Slide switch (on/off) | SPDT SMD | Battery+/VBUS-combined rail -> SW1 -> U3 (regulator) IN |
| U3 | LDO regulator | ME6211C33 (low IQ, ~5uA) | IN = switched battery/USB rail, OUT = 3V3 |
| D1 | Charge status LED | Red 0603 | U2 STAT -> R2 (1k) -> D1 -> 3V3 |
| C1,C2 | Caps | 10uF, 4.7uF | U2 input/output per datasheet typical app circuit |
| C3,C4 | Caps | 10uF, 100nF | U3 output bulk + local decoupling |
| R1 | Resistor | 2k (sets ~450mA charge current, lower for smaller cells) | U2 PROG to GND |

### MCU
| Ref | Part | Value/Part # | Notes |
|---|---|---|---|
| U1 | ESP32-WROOM-32E | — | VDD -> 3V3, GND -> plane, EN -> 10k pull-up + 100nF to GND, GPIO0 -> 10k pull-up + SW2 to GND (manual boot button, no auto-reset circuit needed for this battery board) |
| U4 | USB-UART bridge (for programming) | CP2102N | Only needed if you want onboard programming; otherwise omit and program via an external FTDI header (J3: TX/RX/3V3/GND) to save BOM cost/power |
| SW2 | Tactile button | BOOT | GPIO0 -> SW2 -> GND |
| SW3 | Tactile button | RESET | EN -> SW3 -> GND |

### Sensors & display (I2C bus)
| Ref | Part | Value/Part # | Notes |
|---|---|---|---|
| U5 | BME280 (temp/humidity/pressure) | Bosch BME280, I2C variant | VDD -> 3V3, GND -> GND, SCL -> GPIO22, SDA -> GPIO21, SDO -> GND (sets I2C addr 0x76), CSB -> 3V3 (forces I2C mode) |
| U6 | OLED display module | SSD1306 128x64 I2C | VCC -> 3V3, GND -> GND, SCL -> GPIO22, SDA -> GPIO21 (shared bus, addr 0x3C default) |
| R3,R4 | I2C pull-ups | 4.7k | SCL and SDA each to 3V3 (only one set needed on the bus — place near the MCU) |

### User I/O
| Ref | Part | Value/Part # | Notes |
|---|---|---|---|
| D2 | Status LED | Blue 0603 | GPIO2 -> R5 (330R) -> D2 -> GND |
| SW4 | Tactile button | Wake/mode button | GPIO4 -> SW4 -> GND (also wired to an RTC GPIO for deep-sleep wake if GPIO4 supports it on your variant; alternatively use GPIO33) |

## 2. PCB layout plan

- **Board size/shape:** 45mm x 45mm, 2-layer, ESP32 module on one edge with
  antenna keepout as in ESP32-01.
- **Placement:** Battery connector (BT1) and charger (U2) grouped near one
  corner, away from the antenna keepout. OLED (U6) mounted via a 2x4-pin
  header so it can sit as a "hat" above the rest of the board — place its
  connector centered so the visible display isn't obstructed. BME280 placed
  at a board edge, ideally with a small cutout/vent nearby since it's a
  pressure sensor sensitive to a sealed enclosure without a vent hole.
- **Routing notes:**
  - I2C SDA/SCL routed as a single bus with 4.7k pull-ups placed once, near
    the MCU; keep the bus away from the USB D+/D- pair and switching
    charger traces to minimize noise.
  - Battery +/- traces sized for the charge current (>=20mil for 500mA).
  - Keep U2 (charge IC) thermal pad connected to a small copper pour for
    heat dissipation during charging.
  - GND poured on bottom layer as a continuous plane; stitch vias around
    U1 and U2.
- **Layer stackup:** 2-layer, 1.6mm FR4 standard stackup, same as ESP32-01.

## 3. Bill of materials

| Qty | Ref | Part | Footprint | Example distributor P/N |
|---|---|---|---|---|
| 1 | U1 | ESP32-WROOM-32E | SMD module | Digi-Key 1904-1021-1-ND |
| 1 | U2 | MCP73831T-2ACI/OT | SOT-23-5 | Digi-Key MCP73831T-2ACI/OTCT-ND |
| 1 | U3 | ME6211C33M5G | SOT-23-5 | LCSC C82942 |
| 1 | U4 | CP2102N-A02-GQFN28 (optional) | QFN-28 | Digi-Key 336-3773-1-ND |
| 1 | U5 | BME280 breakout/bare IC | LGA-8 or breakout module | Digi-Key 828-1063-1-ND (breakout) |
| 1 | U6 | SSD1306 0.96" OLED module | 4-pin header module | Amazon/Adafruit 128x64 I2C OLED |
| 1 | J1 | USB-C receptacle | SMD | Digi-Key 538-105450-0621-ND |
| 1 | BT1 | JST-PH 2-pin | THT | Digi-Key 455-1719-ND |
| 1 | SW1 | Slide switch SPDT | SMD | Digi-Key CKN9112-ND |
| 3 | SW2-SW4 | Tactile switch 6x6mm | SMD | Digi-Key 450-1650-ND |
| 2 | R3,R4 | 4.7k resistor | 0603 | Digi-Key any 0603 |
| 1 | R1 | 2k resistor | 0603 | Digi-Key any 0603 |
| 2 | R2,R5 | 330R-1k resistor | 0603 | Digi-Key any 0603 |
| 2 | D1,D2 | LED 0603 | 0603 | Digi-Key any 0603 |
| 4 | C1-C4 | 4.7uF-10uF ceramic | 0805 | Digi-Key 490-6560-1-ND |
| 1 | Battery | 1S LiPo, JST-PH | 500-1000mAh pouch cell | Adafruit/SparkFun LiPo |

## Firmware

[`firmware/environmental_logger.ino`](firmware/environmental_logger.ino)
— Arduino framework. Reads the BME280 over I2C, renders to the OLED, then
deep-sleeps for 60s (or until SW4 wakes it early via `ext0` interrupt).
Requires the "Adafruit BME280 Library" + "Adafruit Unified Sensor" +
"Adafruit SSD1306" + "Adafruit GFX Library" from the Arduino Library
Manager.

Compiles clean (320,228 bytes flash / 24%, 23,836 bytes RAM / 7%) with the
Adafruit libraries pulled in via `arduino-cli lib install`.
