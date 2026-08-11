# ESP32-03 — WiFi Weather Station

**Level:** Intermediate
**Goal:** Desk weather station: color TFT display, real-time clock, local
data logging to microSD, WiFi for fetching a forecast/NTP time. Mains-
powered via USB (no battery).

## 1. Schematic — component & connection list

### Power
| Ref | Part | Value/Part # | Notes |
|---|---|---|---|
| J1 | USB-C receptacle | Molex 105450 | VBUS -> U2 IN |
| U2 | LDO regulator | AMS1117-3.3, 1A | IN = 5V, OUT = 3V3 |
| C1,C2 | Caps | 10uF | U2 in/out per typical app circuit |
| C3 | Cap | 100nF | 3V3 decoupling at U1 |

### MCU + programming
| Ref | Part | Value/Part # | Notes |
|---|---|---|---|
| U1 | ESP32-WROOM-32E | — | Same EN/GPIO0/reset circuit as ESP32-01 (auto-reset via U3 CP2102N + Q1/Q2) |
| U3 | CP2102N-A02-GQFN28 | — | USB-UART for programming, D+/D- to J1 |
| Q1,Q2 | MMBT3904 | — | Auto-reset transistors |
| SW1,SW2 | Tactile switches | RESET / BOOT | As in ESP32-01 |

### Display (SPI)
| Ref | Part | Value/Part # | Notes |
|---|---|---|---|
| U4 | TFT display module | ILI9341 2.4" SPI, 240x320 | VCC -> 3V3, GND -> GND, SCK -> GPIO18, MOSI -> GPIO23, MISO -> GPIO19 (optional, ILI9341 mostly write-only), CS -> GPIO5, DC -> GPIO2, RST -> GPIO4, LED (backlight) -> 3V3 via R1 (100R) |

### RTC (I2C)
| Ref | Part | Value/Part # | Notes |
|---|---|---|---|
| U5 | RTC IC | DS3231SN | VCC -> 3V3, GND -> GND, SCL -> GPIO22, SDA -> GPIO21, INT/SQW -> GPIO34 (input-only pin, optional wake interrupt) |
| BT2 | Coin cell holder | CR2032 | + -> U5 VBAT, - -> GND (RTC backup power) |
| R2,R3 | I2C pull-ups | 4.7k | SCL/SDA to 3V3 |

### microSD (SPI, shared bus with TFT)
| Ref | Part | Value/Part # | Notes |
|---|---|---|---|
| J2 | microSD card slot | Molex 47215 (push-push) | VCC -> 3V3, GND -> GND, SCK -> GPIO18 (shared), MOSI -> GPIO23 (shared), MISO -> GPIO19 (shared), CS -> GPIO15 (dedicated) |
| C4 | Cap | 100nF | J2 VCC decoupling |

### User I/O
| Ref | Part | Value/Part # | Notes |
|---|---|---|---|
| SW3 | Tactile button | Mode/select button | GPIO32 -> SW3 -> GND |
| SW4 | Tactile button | Up/next button | GPIO33 -> SW4 -> GND |
| D1 | Status LED | Blue 0603 | GPIO13 -> R4 (330R) -> D1 -> GND |

## 2. PCB layout plan

- **Board size/shape:** 70mm x 50mm, 2-layer. Antenna keepout on ESP32
  module edge as before.
- **Placement:** TFT connector (U4, typically a 2x7 or FPC header) placed
  on the top face, centered, since it's the primary visible element —
  design the enclosure cutout around it. microSD slot (J2) placed on a
  board edge for card insertion/removal. RTC (U5) and coin cell holder
  (BT2) placed together, away from the TFT's backlight driver noise. SD
  and TFT share the SPI bus but have separate CS lines — keep the shared
  SCK/MOSI/MISO trio routed as a bundle from U1 out to a junction, then
  split to each CS-selected device.
- **Routing notes:**
  - SPI clock (SCK) is the fastest signal here; keep it short and away
    from the I2C bus and RTC crystal.
  - DS3231 has an integrated crystal (TCXO) — keep noisy digital traces
    (SPI, backlight PWM if used) at least 3mm away from U5.
  - Route TFT backlight current (through R1) on a slightly wider trace
    (>=20mil) since it can draw 100+mA depending on panel size.
  - GND plane on bottom layer, stitched vias around U1, U4 connector, and
    U5.
- **Layer stackup:** 2-layer, 1.6mm FR4.

## 3. Bill of materials

| Qty | Ref | Part | Footprint | Example distributor P/N |
|---|---|---|---|---|
| 1 | U1 | ESP32-WROOM-32E | SMD module | Digi-Key 1904-1021-1-ND |
| 1 | U2 | AMS1117-3.3, 1A | SOT-223 | Digi-Key AMS1117-3.3DICT-ND |
| 1 | U3 | CP2102N-A02-GQFN28 | QFN-28 | Digi-Key 336-3773-1-ND |
| 2 | Q1,Q2 | MMBT3904 | SOT-23 | Digi-Key MMBT3904-FDICT-ND |
| 1 | U4 | ILI9341 2.4" SPI TFT module | 2x7 header module | Adafruit/generic ILI9341 SPI TFT |
| 1 | U5 | DS3231SN | SOIC-16 | Digi-Key DS3231SN#-ND |
| 1 | BT2 | CR2032 coin cell holder | THT | Digi-Key BAT-HLD-001-ND |
| 1 | J1 | USB-C receptacle | SMD | Digi-Key 538-105450-0621-ND |
| 1 | J2 | microSD push-push slot | SMD | Digi-Key WM17109-ND |
| 4 | SW1-SW4 | Tactile switch 6x6mm | SMD | Digi-Key 450-1650-ND |
| 2 | R2,R3 | 4.7k resistor | 0603 | Digi-Key any 0603 |
| 2 | R1,R4 | 100R-330R resistor | 0603 | Digi-Key any 0603 |
| 1 | D1 | LED 0603 | 0603 | Digi-Key any 0603 |
| 3 | C1-C3 | 10uF/100nF ceramic | 0805/0603 | Digi-Key per value |
| 1 | C4 | 100nF ceramic | 0603 | Digi-Key 311-1141-1-ND |

## Firmware

[`firmware/weather_station.ino`](firmware/weather_station.ino) — Arduino
framework. Connects to WiFi, syncs the DS3231 RTC from NTP, draws a
date/time + connection-status dashboard on the ILI9341, and appends a CSV
timestamp to `/weather_log.csv` on the SD card once a minute. Falls back
to RTC-only timekeeping if WiFi isn't available. Requires "Adafruit
ILI9341", "Adafruit GFX Library", and "RTClib" from the Library Manager
(`SD`/`WiFi` ship with the ESP32 core). Set `WIFI_SSID`/`WIFI_PASSWORD`
before flashing.

Compiles clean — 976,174 bytes flash (74%, WiFi + TFT pull in a lot), 48,740
bytes RAM (14%). That 74% flash number is worth noting if you're
comparing against a smaller module. This is the most subsystem-heavy
firmware in the ESP32 track (SPI, I2C, WiFi, and SD all at once).
