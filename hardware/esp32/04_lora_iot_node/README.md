# ESP32-04 — LoRa IoT Sensor Node

**Level:** Advanced
**Goal:** Long-range, battery-powered sensor node: LoRa radio for
kilometers-range uplink, multiple sensors, aggressive deep-sleep power
management, USB-C for charging/programming. This is the most complex board
in the ESP32 track — it combines everything from ESP32-01 through 03 plus
RF and careful power-domain design.

## 1. Schematic — component & connection list

### Power (dual-rail: always-on for RTC domain, switched for sensors/radio)
| Ref | Part | Value/Part # | Notes |
|---|---|---|---|
| J1 | USB-C receptacle | Molex 105450 | VBUS -> U2 charger IN, CC1/CC2 5.1k to GND |
| U2 | LiPo charger | MCP73831T-2ACI/OT | Same topology as ESP32-02 |
| BT1 | JST-PH battery connector | — | To U2 VBAT |
| U3 | Buck-boost or LDO regulator | TPS63020 (buck-boost, if you want full battery range) or ME6211C33 (simpler, LDO) | Battery (3.0-4.2V) -> 3V3 rail. Buck-boost is the "advanced" choice: keeps 3V3 stable even as battery droops below 3.3V near end of discharge |
| U4 | Load switch (sensor rail) | TPS22918 | 3V3 -> switched 3V3_SENSORS rail, EN driven by GPIO25 (turns sensors off during deep sleep to cut leakage) |
| C1-C4 | Caps | 10uF/100nF per regulator/switch app circuit | Standard decoupling |

### MCU
| Ref | Part | Value/Part # | Notes |
|---|---|---|---|
| U1 | ESP32-WROOM-32E | — | VDD -> 3V3 (always-on rail, not switched — RTC/deep-sleep domain needs continuous power), EN/GPIO0/reset per ESP32-01 pattern |
| U5 | CP2102N (programming) | — | D+/D- to J1, or omit and use pogo-pin test points (TP1-TP4: 3V3/GND/TX/RX) to save space/power on a board this size-constrained |

### LoRa radio (SPI)
| Ref | Part | Value/Part # | Notes |
|---|---|---|---|
| U6 | LoRa transceiver module | Semtech SX1276-based module (e.g. HopeRF RFM95W, 915MHz or region-appropriate) | VCC -> 3V3 (always-on, radio needs power even during scheduled TX), GND -> GND, SCK -> GPIO18, MOSI -> GPIO23, MISO -> GPIO19, NSS/CS -> GPIO5, RST -> GPIO14, DIO0 (TX/RX done IRQ) -> GPIO26 |
| ANT1 | Antenna connector | U.FL / IPEX | U6 RF pin -> 50ohm trace -> ANT1; use an external antenna, not a PCB trace antenna, for real range |
| C5 | Cap | 100nF | U6 VCC decoupling, placed at the pin |

### Sensors (I2C, on switched rail)
| Ref | Part | Value/Part # | Notes |
|---|---|---|---|
| U7 | BME280 | — | VDD -> 3V3_SENSORS, SCL -> GPIO22, SDA -> GPIO21 |
| U8 | Light sensor | BH1750 | VCC -> 3V3_SENSORS, SCL -> GPIO22, SDA -> GPIO21 (shared bus, addr 0x23) |
| R1,R2 | I2C pull-ups | 4.7k | To 3V3_SENSORS (not the always-on rail — bus is only active when sensors are powered) |

### User I/O / status
| Ref | Part | Value/Part # | Notes |
|---|---|---|---|
| D1 | Status LED | Blue 0603 | GPIO2 -> R3 (330R) -> D1 -> GND |
| SW1 | Wake/user button | — | GPIO33 (RTC-capable pin) -> SW1 -> GND, used as `esp_sleep_enable_ext0_wakeup` source |
| SW2,SW3 | RESET/BOOT | — | Standard, per ESP32-01 |

## 2. PCB layout plan

- **Board size/shape:** 40mm x 60mm, 2-layer (4-layer optional if RF
  performance needs a solid ground reference under the LoRa module —
  recommended if you have the budget). Antenna keepout for both the ESP32
  WiFi/BT antenna and the LoRa module's RF section — treat both as "no
  copper, no components" zones extending ~15mm.
- **Placement:** LoRa module (U6) and its U.FL connector (ANT1) placed at
  one board edge, oriented so the RF trace to ANT1 is a straight, short run
  (<15mm) with no vias. Battery/charger circuitry grouped at the opposite
  edge. Sensors (U7/U8) placed away from the LoRa module's RF section and
  away from the buck-boost regulator's switching node (EMI source) — a
  buck-boost's inductor should have its own local ground area with a
  slotted/isolated pour if noise-sensitive sensors are nearby.
- **Routing notes:**
  - RF trace from U6 to ANT1: 50ohm single-ended microstrip, calculated
    for your stackup (roughly 0.3mm wide on 1.6mm FR4 top layer with full
    ground plane below) — length and impedance matter here.
  - Keep the buck-boost inductor's switching node (U3) as a small, isolated
    copper island — do not route sensitive signals underneath or nearby.
  - Two power domains: route "always-on 3V3" and "3V3_SENSORS" as visibly
    separate nets/planes with a clear physical split, joined only through
    U4 (the load switch), to avoid accidentally shorting them together
    during layout.
  - GND plane split only under the RF section if using 4 layers with a
    dedicated RF ground; otherwise single continuous GND pour with heavy
    stitching around U6.
- **Layer stackup:** 2-layer default (top signal+components, bottom GND
  pour); 4-layer upgrade path = signal / GND / power / signal for cleaner
  RF and lower noise into the sensor rail.

## 3. Bill of materials

| Qty | Ref | Part | Footprint | Example distributor P/N |
|---|---|---|---|---|
| 1 | U1 | ESP32-WROOM-32E | SMD module | Digi-Key 1904-1021-1-ND |
| 1 | U2 | MCP73831T-2ACI/OT | SOT-23-5 | Digi-Key MCP73831T-2ACI/OTCT-ND |
| 1 | U3 | TPS63020DSJR | WSON-10 | Digi-Key 296-37019-1-ND |
| 1 | U4 | TPS22918DBVR | SOT-23-6 | Digi-Key 296-42287-1-ND |
| 1 | U5 | CP2102N-A02-GQFN28 (optional) | QFN-28 | Digi-Key 336-3773-1-ND |
| 1 | U6 | RFM95W (SX1276, region-matched freq) | SMD module | Digi-Key 1738-1010-ND |
| 1 | ANT1 | U.FL connector | SMD | Digi-Key WM17123-ND |
| 1 | U7 | BME280 | LGA-8 | Digi-Key 828-1063-1-ND |
| 1 | U8 | BH1750FVI | SOP-6 | Digi-Key 425-2871-1-ND |
| 1 | J1 | USB-C receptacle | SMD | Digi-Key 538-105450-0621-ND |
| 1 | BT1 | JST-PH 2-pin | THT | Digi-Key 455-1719-ND |
| 3 | SW1-SW3 | Tactile switch 6x6mm | SMD | Digi-Key 450-1650-ND |
| 2 | R1,R2 | 4.7k resistor | 0603 | Digi-Key any 0603 |
| 1 | R3 | 330R resistor | 0603 | Digi-Key any 0603 |
| 1 | D1 | LED 0603 | 0603 | Digi-Key any 0603 |
| ~6 | C1-C5 | 10uF/100nF ceramic (per app circuits) | 0603/0805 | Digi-Key per value |
| 1 | Battery | 1S LiPo | 500-2000mAh | Adafruit/SparkFun LiPo |
| 1 | Antenna | 868/915MHz whip, U.FL | — | Digi-Key/generic LoRa antenna |

## Firmware

[`firmware/lora_sensor_node.ino`](firmware/lora_sensor_node.ino) —
Arduino framework. On each wake: powers up the switched sensor rail,
reads BME280 + BH1750 over I2C, transmits a compact text payload over
LoRa, powers the sensor rail back down, and deep-sleeps for 5 minutes (or
wakes early on SW1). Requires "Adafruit BME280 Library" + "Adafruit
Unified Sensor", "BH1750" (Christopher Laws), and "LoRa"
(sandeepmistry/arduino-LoRa) from the Library Manager. Set
`LORA_FREQUENCY` to your region's ISM band.

Compiles clean with the BME280/BH1750/LoRa libraries installed — 320,688
bytes flash (24%), 23,932 bytes RAM (7%). The sensor-rail power sequencing
(enable -> settle -> read -> disable -> sleep) is the core idea behind
this board's power budget.
