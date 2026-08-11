# STM32-01 — Blue Pill Style Dev Board

**Level:** Beginner
**Goal:** Minimal STM32F103C8T6 breakout, "Blue Pill" style: SWD programming
header, USB for power + serial, one user LED, one user button, all GPIOs
brought to 0.1" headers.

## 1. Schematic — component & connection list

### Power
| Ref | Part | Value/Part # | Notes |
|---|---|---|---|
| J1 | USB Micro-B or USB-C receptacle | Molex 47346 (Micro-B) or 105450 (C) | VBUS -> U2 IN, GND -> GND |
| U2 | LDO regulator | AMS1117-3.3 | IN = 5V, OUT = 3V3 |
| C1,C2 | Caps | 10uF | U2 in/out |
| C3 | Cap | 100nF | 3V3 decoupling at U1 VDD pins |
| D1 | Power LED | Green 0603 | 3V3 -> R1 (1k) -> D1 -> GND |

### MCU
| Ref | Part | Value/Part # | Notes |
|---|---|---|---|
| U1 | STM32F103C8T6 | LQFP-48 | VDD (pins 1,24,36,48) -> 3V3, VSS (pins 8,23,35,47) -> GND, VDDA -> 3V3 (via ferrite bead FB1 for analog isolation), VSSA -> GND, VBAT -> 3V3 (tie to VDD if no coin cell backup), BOOT0 -> R2 (10k) to GND (normal boot from flash), BOOT1 (PB2) -> R3 (10k) to GND |
| Y1 | Crystal | 8MHz HC-49 SMD | Between OSC_IN (PD0)/OSC_OUT (PD1), C4/C5 = 20pF load caps to GND each |
| Y2 | Crystal (optional) | 32.768kHz | Between OSC32_IN (PC14)/OSC32_OUT (PC15), C6/C7 = 6-12pF load caps, for RTC accuracy — omit if not using RTC |
| FB1 | Ferrite bead | 600R @ 100MHz | VDD to VDDA, standard analog supply filtering |
| SW1 | Tactile button | Reset | NRST -> SW1 -> GND, with R4 (10k) NRST to 3V3 pull-up and C8 (100nF) NRST to GND |

### Programming (SWD)
| Ref | Part | Value/Part # | Notes |
|---|---|---|---|
| J2 | 2x2 header, 2.54mm (or Tag-Connect footprint) | — | Pin1=3V3, Pin2=SWDIO(PA13), Pin3=SWCLK(PA14), Pin4=GND |

### User I/O
| Ref | Part | Value/Part # | Notes |
|---|---|---|---|
| D2 | User LED | Blue 0603 | PC13 -> R5 (330R) -> D2 -> 3V3 (active-low, matches real Blue Pill convention) |
| SW2 | User button | — | PA0 -> SW2 -> GND, R6 (10k) PA0 to 3V3 pull-up |
| J3,J4 | 1x20 headers, 2.54mm | — | Break out all remaining GPIOs (PA0-PA15 minus used pins, PB0-PB15, PC13-PC15) |

## 2. PCB layout plan

- **Board size/shape:** 53mm x 23mm (classic Blue Pill form factor), 2-layer.
- **Placement:** U1 centered on the board with the two long GPIO headers
  (J3/J4) running along both long edges — this is the defining layout
  constraint of this form factor. Crystal Y1 placed as close to U1's OSC
  pins as possible (within 5mm), with its load caps right at the crystal
  pins, not at the MCU. USB connector and SWD header both placed on the
  same short edge for easy bench access.
- **Routing notes:**
  - Crystal traces (OSC_IN/OSC_OUT) kept short, symmetric, and away from
    any switching/digital traces — this is the most sensitive analog
    routing on the board despite the overall simplicity.
  - VDDA/VSSA routed as a distinct, filtered branch off the main 3V3/GND
    (through FB1), not just tapped off the digital 3V3 plane directly.
  - NRST trace kept short with its RC filter (R4/C8) placed right at the
    pin.
  - GND poured on bottom layer; a few strategic top-layer GND fill areas
    in the space between the two GPIO header rows.
- **Layer stackup:** 2-layer, 1.6mm FR4.

## 3. Bill of materials

| Qty | Ref | Part | Footprint | Example distributor P/N |
|---|---|---|---|---|
| 1 | U1 | STM32F103C8T6 | LQFP-48 | Digi-Key 497-6063-ND |
| 1 | U2 | AMS1117-3.3 | SOT-223 | Digi-Key AMS1117-3.3DICT-ND |
| 1 | Y1 | 8MHz crystal HC-49 SMD | SMD 5x3.2mm | Digi-Key 535-9159-1-ND |
| 1 | Y2 | 32.768kHz crystal (optional) | SMD 3.2x1.5mm | Digi-Key 535-10336-1-ND |
| 1 | FB1 | Ferrite bead 600R | 0603 | Digi-Key 240-2263-1-ND |
| 1 | J1 | USB Micro-B or USB-C | SMD | Digi-Key 609-4618-1-ND (Micro-B) |
| 1 | J2 | 2x2 header 2.54mm | THT | Digi-Key any |
| 2 | J3,J4 | 1x20 header 2.54mm | THT | Digi-Key any |
| 2 | SW1,SW2 | Tactile switch 6x6mm | SMD | Digi-Key 450-1650-ND |
| 2 | D1,D2 | LED 0603 | 0603 | Digi-Key any 0603 |
| 6 | R1-R6 | 330R-10k assorted | 0603 | Digi-Key any 0603 |
| 8 | C1-C8 | 20pF/100nF/10uF assorted | 0603/0805 | Digi-Key per value |

## Firmware

[`firmware/main.c`](firmware/main.c) — STM32 HAL, structured for a
CubeMX-generated STM32F103C8T6 project. Debounced-polls the user button
(PA0) and blinks the active-low user LED (PC13), with the button toggling
between two blink rates. `MX_GPIO_Init()` (pin mode/clock config) is left
as CubeMX boilerplate since it's board-config-specific; the polling loop
is the actual firmware logic. Program via SWD with an ST-Link (J2).

I haven't actually built this one — no STM32CubeIDE project scaffold or
ST-Link on hand, and the HAL calls need CubeMX's generated init code to
even link. Since this board is the reference every other STM32 project
in this repo physically builds on, it's the one I'd bring up on a bench
first if I got hardware in hand.
