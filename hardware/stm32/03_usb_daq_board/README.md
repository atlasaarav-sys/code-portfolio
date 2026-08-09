# STM32-03 — USB Data Acquisition Board

**Level:** Intermediate-Advanced
**Goal:** 4-channel analog data logger: STM32F405 sampling 4 analog inputs
through a signal-conditioning front end, streaming over USB full-speed to a
PC and simultaneously logging to microSD, with a precision voltage
reference for accurate ADC readings.

## 1. Schematic — component & connection list

### Power
| Ref | Part | Value/Part # | Notes |
|---|---|---|---|
| J1 | USB Micro-B | Molex 47346 | VBUS -> U2 IN, D+/D- -> U1 PA12/PA11 directly (F4 has native USB FS) |
| U2 | LDO regulator | AMS1117-3.3, 1A | IN = 5V, OUT = 3V3 digital rail |
| U3 | Precision voltage reference | REF3033 (3.0V) | IN -> 3V3, used as VREF+ for the ADC — far more accurate than using VDDA directly |
| C1,C2 | Caps | 10uF | U2 in/out |
| C3 | Cap | 100nF | 3V3 decoupling at U1 |
| FB1 | Ferrite bead | 600R @ 100MHz | Between digital 3V3 and VDDA (analog supply) |
| C4,C5 | Caps | 1uF, 100nF | VDDA decoupling |
| C6 | Cap | 1uF | U3 reference output decoupling, low-ESR |

### MCU
| Ref | Part | Value/Part # | Notes |
|---|---|---|---|
| U1 | STM32F405RGT6 | LQFP-64 | VDD/VSS multiple pins per datasheet -> 3V3/GND, VDDA -> filtered 3V3 (via FB1), VSSA -> GND, VREF+ -> U3 output (3.0V), BOOT0 -> R1 (10k) to GND, NRST -> SW1 -> GND with R2/C7 RC network |
| Y1 | 8MHz crystal (HSE) | HC-49 SMD | OSC_IN/OSC_OUT, C8/C9 = 20pF load caps |
| Y2 | 32.768kHz crystal (LSE, optional) | — | For accurate RTC timestamps in logged data |
| J2 | 2x2 SWD header | — | 3V3/SWDIO/SWCLK/GND |

### Analog front end (4 channels)
| Ref | Part | Value/Part # | Notes |
|---|---|---|---|
| U4 | Quad op-amp (buffer/scale) | MCP6004 (rail-to-rail I/O) | Each channel: op-amp in unity-gain buffer or 2x attenuator config, output -> ADC1 channel |
| J3 | 4x BNC or 4-pin terminal blocks | — | Analog input 1-4, each through R3-R6 (1k series, ESD/current limit) and D3-D10 (clamp diodes to 3V3 and GND, e.g. BAT54S dual Schottky per channel) |
| R7-R10 | Bias/scaling resistors | 10k (adjust per desired input range) | Voltage divider on each channel if inputs exceed 0-3V range |
| ADC mapping | — | — | CH1 -> PA0 (ADC1_IN0), CH2 -> PA1 (ADC1_IN1), CH3 -> PA2 (ADC1_IN2), CH4 -> PA3 (ADC1_IN3) |

### microSD (SDIO, native STM32 SDIO peripheral — faster than SPI)
| Ref | Part | Value/Part # | Notes |
|---|---|---|---|
| J4 | microSD push-push slot | Molex 47215 | VCC -> 3V3, GND -> GND, CLK -> PC12 (SDIO_CK), CMD -> PD2 (SDIO_CMD), D0-D3 -> PC8-PC11 (SDIO_D0-D3) |
| R11-R15 | Pull-ups | 47k | On CMD and D0-D3 lines to 3V3 per SDIO spec |

### User I/O
| Ref | Part | Value/Part # | Notes |
|---|---|---|---|
| D1,D2 | Status LEDs (logging/USB) | 0603 | PB0/PB1 -> R16/R17 (330R) -> LEDs -> GND |
| SW2 | Start/stop logging button | — | PB2 -> SW2 -> GND, R18 (10k) pull-up |

## 2. PCB layout plan

- **Board size/shape:** 70mm x 55mm, 4-layer recommended (signal / GND /
  power / signal) given the mixed analog+digital+USB nature — a solid
  ground plane matters a lot for ADC accuracy here.
- **Placement:** Analog front end (U4, input connectors J3, protection
  diodes) grouped on one side of the board, physically separated from the
  digital section (MCU, USB, SD card) — treat it as two zones with a
  visible split in placement, even if the ground plane is continuous. VREF
  circuitry (U3 + C6) placed close to U1's VREF+ pin. Crystal Y1 close to
  U1 OSC pins. USB connector (J1) at a board edge with ESD/common-mode
  choke placement room if you add one later.
- **Routing notes:**
  - Analog input traces kept short, guarded by GND pour on both sides
    where possible; avoid routing digital/SDIO signals underneath analog
    traces.
  - VDDA/VREF+ path: dedicated trace from FB1/U3 straight to U1, not
    tapped mid-plane — this directly affects ADC noise floor.
  - USB D+/D- as a matched differential pair, 90ohm impedance, routed away
    from the crystal and SDIO bus.
  - SDIO bus (CLK/CMD/D0-D3) routed as a tight group with length-matching
    on D0-D3 (they're sampled together).
  - Single-point analog/digital ground join near U1's VSSA, per standard
    mixed-signal layout practice — do not split the ground plane
    arbitrarily elsewhere.
- **Layer stackup:** 4-layer, 1.6mm total: L1 signal, L2 GND, L3 power
  (3V3/analog), L4 signal. (2-layer is workable for a first prototype but
  expect a noisier ADC floor.)

## 3. Bill of materials

| Qty | Ref | Part | Footprint | Example distributor P/N |
|---|---|---|---|---|
| 1 | U1 | STM32F405RGT6 | LQFP-64 | Digi-Key 497-15948-ND |
| 1 | U2 | AMS1117-3.3, 1A | SOT-223 | Digi-Key AMS1117-3.3DICT-ND |
| 1 | U3 | REF3030 or REF3033 | SOT-23-6 | Digi-Key REF3030AIDBZT-ND |
| 1 | U4 | MCP6004 quad op-amp | SOIC-14 | Digi-Key MCP6004-I/SL-ND |
| 1 | Y1 | 8MHz crystal | HC-49 SMD | Digi-Key 535-9159-1-ND |
| 1 | Y2 | 32.768kHz crystal | SMD | Digi-Key 535-10336-1-ND |
| 1 | J1 | USB Micro-B | SMD | Digi-Key 609-4618-1-ND |
| 1 | J4 | microSD push-push slot | SMD | Digi-Key WM17109-ND |
| 1 | J2 | 2x2 header 2.54mm | THT | Digi-Key any |
| 4 | J3 | BNC or terminal block, per channel | THT | Digi-Key per type |
| 4 | D3-D10 pairs | BAT54S dual Schottky clamp | SOT-23 | Digi-Key BAT54SLT1GOSCT-ND |
| 1 | SW1,SW2 | Tactile switch 6x6mm | SMD | Digi-Key 450-1650-ND |
| 2 | D1,D2 | LED 0603 | 0603 | Digi-Key any 0603 |
| ~20 | R1-R18 | Assorted 1k-47k | 0603 | Digi-Key any 0603 |
| ~10 | C1-C9 | Assorted 20pF-10uF | 0603/0805 | Digi-Key per value |

## Firmware note

USB CDC (virtual COM) or USB composite CDC+MSC for live streaming, DMA-fed
ADC sampling triggered by a timer for consistent sample rate, SDIO+FatFs
for on-board logging — this board is a good "systems" project pairing
analog design care with USB/DMA/filesystem firmware.
