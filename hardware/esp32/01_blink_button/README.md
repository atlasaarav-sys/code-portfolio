# ESP32-01 — Blink + Button Dev Board

**Level:** Beginner
**Goal:** Minimal, self-contained ESP32-WROOM-32 board: power from USB,
program over USB-UART, one user LED, one user button. This is the "hello
world" board — the reference every later board in this track builds on.

## 1. Schematic — component & connection list

### Power
| Ref | Part | Value/Part # | Notes |
|---|---|---|---|
| J1 | USB-C receptacle | Molex 105450 (or any USB-C, power-only pins) | VBUS -> U2 IN, GND -> GND plane, CC1/CC2 each via 5.1k to GND (required for USB-C to source 5V) |
| U2 | LDO regulator | AMS1117-3.3 or ME6211C33 | IN = VBUS (5V), OUT = 3V3 net, EN tied high via 10k if available |
| C1 | Cap | 10uF | U2 IN to GND (bulk) |
| C2 | Cap | 10uF | 3V3 to GND (bulk, regulator output) |
| C3 | Cap | 100nF | 3V3 to GND, placed at U1 VDD pins (decoupling) |
| D1 | LED (power) | Green 0805 | 3V3 -> R1 -> D1 -> GND |
| R1 | Resistor | 1k | Power LED current limit |

### MCU + programming
| Ref | Part | Value/Part # | Notes |
|---|---|---|---|
| U1 | ESP32-WROOM-32 module | Espressif ESP32-WROOM-32E | VDD (pins 2) -> 3V3, GND (pins 1,15,38-41 per datasheet) -> GND plane |
| U3 | USB-UART bridge | CP2102N-A02-GQFN28 | VBUS -> 3V3 (via own LDO or shared 3V3), D+/D- -> J1 USB data pins |
| U1.EN | EN pin | — | 10k pull-up to 3V3; 100nF to GND (auto-reset RC) |
| U1.GPIO0 | Boot mode select | — | 10k pull-up to 3V3; pulled LOW during flashing by auto-reset circuit or manually via SW2 |
| Q1, Q2 | NPN transistor (auto-reset) | MMBT3904 | Standard "auto-program" circuit: U3 DTR -> C(RC network) -> Q1 base drives EN; U3 RTS -> Q2 base drives GPIO0. (Optional — can omit and use manual BOOT/EN buttons instead, see SW1/SW2) |
| SW1 | Tactile button | EN / reset | EN pin -> SW1 -> GND |
| SW2 | Tactile button | BOOT (GPIO0) | GPIO0 -> SW2 -> GND |

### User I/O
| Ref | Part | Value/Part # | Notes |
|---|---|---|---|
| D2 | LED (user) | Blue 0805 | GPIO2 -> R2 -> D2 -> GND |
| R2 | Resistor | 330R | User LED current limit |
| SW3 | Tactile button | User button | GPIO4 -> SW3 -> GND; GPIO4 has internal pull-up enabled in firmware (no external R needed, but add R3 = 10k to 3V3 if you want it visible in schematic for clarity) |
| J2 | 2x1 header | — | Spare 3V3/GND breakout for a breadboard jumper |

## 2. PCB layout plan

- **Board size/shape:** 50mm x 30mm, 2-layer. ESP32-WROOM-32 module along one
  long edge with its antenna section overhanging the board edge (no copper
  or ground plane under/near the antenna — keep a keepout of at least 15mm
  in front of the module's antenna cutout on all layers).
- **Placement:** USB-C connector (J1) on the opposite short edge from the
  antenna, mechanically anchored with its shield pins to GND. U3
  (CP2102N) and its supporting caps placed close to J1 to keep USB D+/D-
  traces short. U2 (LDO) placed between J1 and U1, with C1 on the input
  side and C2 immediately at the output pin. SW1/SW2 placed along the
  board edge, easily reachable with a finger.
- **Routing notes:**
  - USB D+/D- routed as a tight differential pair (match length within
    5mil), 90ohm differential impedance, kept away from switching
    regulator traces.
  - 3V3 as a short, wide (>=30mil) trace or a small local plane; place
    100nF decoupling caps within 3mm of every U1 VDD pin, via directly to
    GND.
  - GND poured as a plane on both layers, stitched with vias every
    ~5mm, especially around U1's ground pins and the antenna keepout
    boundary.
  - Keep EN/GPIO0 traces short and away from noisy digital lines (SPI
    flash inside the module switches fast during boot).
- **Layer stackup:** 2-layer, 1.6mm FR4, top = signal + component, bottom =
  GND pour + a few 3V3 routes. Standard 1oz copper.

## 3. Bill of materials

| Qty | Ref | Part | Footprint | Example distributor P/N |
|---|---|---|---|---|
| 1 | U1 | ESP32-WROOM-32E | SMD module, castellated | Digi-Key 1904-1021-1-ND |
| 1 | U2 | AMS1117-3.3 | SOT-223 | Digi-Key AMS1117-3.3DICT-ND |
| 1 | U3 | CP2102N-A02-GQFN28 | QFN-28 | Digi-Key 336-3773-1-ND |
| 2 | Q1,Q2 | MMBT3904 | SOT-23 | Digi-Key MMBT3904-FDICT-ND |
| 1 | J1 | USB-C receptacle | SMD, 16-pin | Digi-Key 538-105450-0621-ND |
| 3 | C1,C2 | 10uF ceramic X5R | 0805 | Digi-Key 490-6560-1-ND |
| 1 | C3 | 100nF ceramic | 0603 | Digi-Key 311-1141-1-ND |
| 2 | D1,D2 | LED 0805 (green, blue) | 0805 | Digi-Key any 0805 LED |
| 2 | R1,R2 | 330R-1k resistor | 0603 | Digi-Key any 0603 |
| 2 | R (EN/GPIO0 pull-ups) | 10k resistor | 0603 | Digi-Key any 0603 |
| 3 | SW1-SW3 | Tactile switch 6x6mm | SMD | Digi-Key 450-1650-ND |
| 1 | J2 | 2-pin header 2.54mm | THT | Digi-Key any |

## Firmware

[`firmware/blink_button.ino`](firmware/blink_button.ino) — Arduino
framework. Debounces the user button (GPIO4) and toggles the user LED
(GPIO2) on each press, logging state changes over serial. Flash with the
Arduino IDE (ESP32 board package) or `arduino-cli compile --fqbn
esp32:esp32:esp32`.

Compiles clean against the ESP32 Arduino core (`arduino-cli compile --fqbn
esp32:esp32:esp32`): 271,928 bytes flash (20%), 22,140 bytes RAM (6%).
