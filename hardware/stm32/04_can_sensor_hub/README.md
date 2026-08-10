# STM32-04 — CAN + USB-C Sensor Hub

**Level:** Advanced
**Goal:** The capstone board: STM32F405 with a CAN bus interface (for
automotive/industrial-style networking), USB-C with PD-negotiated 5V input,
multiple sensor interfaces (I2C + SPI), and an SD card — a general-purpose
"sensor hub" node that could sit on a CAN network alongside other nodes.

## 1. Schematic — component & connection list

### Power (USB-C with basic PD sink negotiation)
| Ref | Part | Value/Part # | Notes |
|---|---|---|---|
| J1 | USB-C receptacle | Molex 105450 | VBUS -> U5 IN, CC1/CC2 -> U6 (PD sink controller) |
| U6 | USB-PD sink controller | FUSB302BMPX or a fixed-5V CC-resistor approach (5.1k CC to GND for basic 5V-only, no full PD IC needed unless you want to negotiate 9V/12V) | For 5V-only operation: 5.1k resistors on CC1/CC2 to GND is sufficient and skips U6 entirely — simpler advanced-board option is documented here for reference if higher voltage input is wanted |
| U5 | Buck regulator (5V input tolerant) | MP2307 or TPS54331 | VBUS(5V) -> 3V3 |
| C1,C2 | Caps | 10uF/22uF | U5 in/out |
| C3 | Cap | 100nF | 3V3 decoupling at U1 |
| FB1 | Ferrite bead | 600R @ 100MHz | Digital 3V3 to VDDA |
| C4,C5 | Caps | 1uF, 100nF | VDDA decoupling |

### MCU
| Ref | Part | Value/Part # | Notes |
|---|---|---|---|
| U1 | STM32F405RGT6 | LQFP-64 | Standard power/reset/crystal per STM32-03. BOOT0 -> R1 (10k) to GND, NRST -> SW1 -> GND with RC network |
| Y1 | 8MHz crystal | HC-49 SMD | HSE, C6/C7 = 20pF load caps |
| J2 | 2x2 SWD header | — | 3V3/SWDIO/SWCLK/GND |

### CAN bus
| Ref | Part | Value/Part # | Notes |
|---|---|---|---|
| U2 | CAN transceiver | TJA1051T/3 | VCC -> 3V3, GND -> GND, TXD -> PB9 (CAN1_TX), RXD -> PB8 (CAN1_RX), CANH/CANL -> J3 |
| J3 | 2-pin terminal block or DB9 | — | CANH, CANL to the bus |
| R2 | Termination resistor | 120R | Across CANH/CANL, populate only if this board is a bus endpoint (add a jumper JP1 to disconnect it if mid-bus) |
| JP1 | 2-pin jumper | — | In series with R2, so termination can be disabled |

### Sensor interfaces
| Ref | Part | Value/Part # | Notes |
|---|---|---|---|
| J4 | 4-pin header (I2C) | — | 3V3/GND/SCL(PB6)/SDA(PB7), R3/R4 (4.7k) pull-ups to 3V3 |
| J5 | 5-pin header (SPI) | — | 3V3/GND/SCK(PA5)/MISO(PA6)/MOSI(PA7), plus a spare CS on PA4 |
| U3 | IMU (example onboard sensor) | ICM-42688-P | VDD -> 3V3, GND -> GND, SCL/SDA on the shared I2C bus (addr 0x68), INT -> PC0 |

### microSD (SDIO)
| Ref | Part | Value/Part # | Notes |
|---|---|---|---|
| J6 | microSD push-push slot | Molex 47215 | Same SDIO mapping as STM32-03 (PC8-PC12, PD2) |
| R5-R9 | Pull-ups | 47k | CMD/D0-D3 to 3V3 |

### Programming/debug (USB, secondary to CAN as primary interface)
| Ref | Part | Value/Part # | Notes |
|---|---|---|---|
| — | Native USB FS | — | U1 D+/D- (PA11/PA12) -> J1 USB data pins, for firmware update / USB-CDC debug console alongside the CAN interface |

### User I/O
| Ref | Part | Value/Part # | Notes |
|---|---|---|---|
| D1,D2 | Status LEDs (CAN activity / power) | 0603 | PC13/PC14 -> R10/R11 (330R) -> LEDs -> GND |
| SW2 | User/config button | — | PC15 -> SW2 -> GND, R12 (10k) pull-up |

## 2. PCB layout plan

- **Board size/shape:** 65mm x 50mm, 4-layer (signal/GND/power/signal) —
  CAN and USB both benefit from a solid reference plane, and this board has
  the most mixed traffic of the set.
- **Placement:** CAN transceiver (U2) and its terminal block (J3) placed at
  one edge, with the 120R termination (R2/JP1) right at the connector. USB-C
  (J1) and its power circuitry (U5/U6) at another edge. MCU (U1) central.
  Sensor headers (J4/J5) and the IMU (U3) grouped together, away from the
  CAN transceiver's bus-driving output stage (can inject noise) and away
  from the buck regulator's switching node.
- **Routing notes:**
  - CANH/CANL routed as a differential pair as much as practical, kept away
    from the crystal and from the buck regulator's switch node; the 120R
    termination directly across the pair at the connector, not mid-trace.
  - USB D+/D- matched differential pair, 90ohm, short run to J1.
  - SDIO bus grouped/length-matched as in STM32-03.
  - I2C bus pull-ups placed once, near the connector or near U1, not
    duplicated at every sensor.
  - Keep digital switching noise (buck regulator, SDIO) away from the CAN
    transceiver's analog CANH/CANL output stage — transceivers are
    sensitive to nearby EMI on the bus lines.
- **Layer stackup:** 4-layer: L1 signal, L2 GND, L3 power, L4 signal.

## 3. Bill of materials

| Qty | Ref | Part | Footprint | Example distributor P/N |
|---|---|---|---|---|
| 1 | U1 | STM32F405RGT6 | LQFP-64 | Digi-Key 497-15948-ND |
| 1 | U2 | TJA1051T/3 | SOIC-8 | Digi-Key 568-9836-1-ND |
| 1 | U3 | ICM-42688-P | LGA-14 | Digi-Key 1428-1103-1-ND |
| 1 | U5 | MP2307DN | SOIC-8 | Digi-Key MP2307DN-LF-Z-ND |
| 1 | U6 | FUSB302BMPX (optional, full PD) | QFN-10 | Digi-Key FUSB302BMPXCT-ND |
| 1 | Y1 | 8MHz crystal | HC-49 SMD | Digi-Key 535-9159-1-ND |
| 1 | J1 | USB-C receptacle | SMD | Digi-Key 538-105450-0621-ND |
| 1 | J3 | 2-pin terminal block, CAN | THT | Digi-Key ED2609-ND |
| 1 | J6 | microSD push-push slot | SMD | Digi-Key WM17109-ND |
| 1 | J2 | 2x2 header 2.54mm | THT | Digi-Key any |
| 2 | J4,J5 | 4-5 pin headers | THT | Digi-Key any |
| 1 | R2 | 120R resistor | 0805 | Digi-Key any 0805 |
| 1 | JP1 | 2-pin jumper + shunt | THT | Digi-Key any |
| 2 | SW1,SW2 | Tactile switch 6x6mm | SMD | Digi-Key 450-1650-ND |
| 2 | D1,D2 | LED 0603 | 0603 | Digi-Key any 0603 |
| ~15 | R1-R12 | Assorted resistors | 0603 | Digi-Key any 0603 |
| ~10 | C1-C7 | Assorted caps | 0603/0805 | Digi-Key per value |

## Firmware

[`firmware/main.c`](firmware/main.c) — STM32 HAL + bxCAN + USB-CDC,
structured for a CubeMX-generated STM32F405 project. Reads the ICM-42688-P
IMU over I2C at 50Hz, broadcasts each reading as a standard CAN frame
(`HAL_CAN_AddTxMessage`), and mirrors the same data to a USB-CDC debug
console. Peripheral/middleware init (`MX_CAN1_Init`, `MX_I2C1_Init`,
`MX_USB_DEVICE_Init`) is CubeMX boilerplate, left as comments — the CAN
framing and I2C read logic is the real content.

**Status:** written and reviewed, not compiled/flashed here (needs a real
CubeMX bxCAN+USB_DEVICE project to build, and no CAN transceiver/IMU
hardware or a second CAN node to test against in this environment) — CAN
bus work specifically needs a second node (or a USB-CAN adapter + candump)
to verify frames are actually landing on the bus correctly, which isn't
something to skip before trusting this.
