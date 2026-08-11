# STM32-02 — Dual Motor Driver Board

**Level:** Intermediate
**Goal:** Small robotics controller: STM32F401 driving two DC motors via a
dual H-bridge, reading quadrature encoders for closed-loop speed/position
control, powered from a separate motor supply (e.g. 2S/3S LiPo) with a
regulated logic rail.

## 1. Schematic — component & connection list

### Power (dual-rail: VMOTOR for the H-bridge, 3V3 for logic)
| Ref | Part | Value/Part # | Notes |
|---|---|---|---|
| J1 | 2-pin terminal block or JST-XH | — | VMOTOR (7-12V, e.g. 2S-3S LiPo) input, reverse-polarity protected by D1 |
| D1 | Schottky diode | SS34 | In series with VMOTOR+ input, protects against reversed battery |
| U2 | Buck regulator | MP2307 or similar 3.3V buck (more efficient than LDO from a 2S+ input) | VMOTOR -> 3V3 logic rail |
| C1,C2 | Caps (buck in/out) | 10uF/22uF | Per U2 typical app circuit |
| C3 | Cap | 100nF | 3V3 decoupling at U1 |
| J2 | 2-pin terminal block | — | Separate USB-independent power input option, or use USB (J5) for logic-only bench testing (motors won't spin without VMOTOR) |
| J5 | USB Micro-B | — | For programming/logic power only, VBUS -> optional secondary LDO -> 3V3 (diode-ORed with U2 output so either source can power logic) |
| D2 | Schottky diode | SS14 | OR's USB 5V-derived 3V3 with buck output so board works from USB alone for bring-up |

### MCU
| Ref | Part | Value/Part # | Notes |
|---|---|---|---|
| U1 | STM32F401CCU6 | LQFP-48 (WeAct "Black Pill" style) | VDD -> 3V3, VSS -> GND, BOOT0 -> R1 (10k) to GND, NRST -> SW1 -> GND with R2 (10k) pull-up + C4 (100nF) |
| Y1 | 25MHz crystal | HC-49 SMD | OSC_IN/OSC_OUT, C5/C6 = 10pF load caps |
| J3 | 2x2 SWD header | — | 3V3/SWDIO(PA13)/SWCLK(PA14)/GND |

### Motor driver
| Ref | Part | Value/Part # | Notes |
|---|---|---|---|
| U3 | Dual H-bridge driver | DRV8833 | VM -> VMOTOR, GND -> GND, VCC -> 3V3, AIN1 -> TIM1_CH1 (PA8), AIN2 -> TIM1_CH2 (PA9), BIN1 -> TIM1_CH3 (PA10), BIN2 -> TIM1_CH4 (PA11), AOUT1/AOUT2 -> Motor A terminals, BOUT1/BOUT2 -> Motor B terminals, nSLEEP -> GPIO PB0 (pulled high via R3 10k, MCU can force sleep for power saving), nFAULT -> GPIO PB1 (input, pulled up via R4 10k) |
| C7,C8 | Caps | 100nF + 10uF | U3 VM decoupling, placed close to the IC |
| J4,J6 | 2-pin terminal blocks | — | Motor A / Motor B output terminals |

### Encoders (quadrature, timer-captured)
| Ref | Part | Value/Part # | Notes |
|---|---|---|---|
| J7 | 4-pin header | — | Encoder A: VCC(3V3)/GND/CH_A(PA0, TIM2_CH1)/CH_B(PA1, TIM2_CH2) |
| J8 | 4-pin header | — | Encoder B: VCC(3V3)/GND/CH_A(PB6, TIM4_CH1)/CH_B(PB7, TIM4_CH2) |
| R5-R8 | Pull-ups | 10k | On each encoder channel to 3V3 if using open-drain encoder outputs (omit if encoder module has push-pull outputs) |

### User I/O
| Ref | Part | Value/Part # | Notes |
|---|---|---|---|
| D3 | Status LED | Blue 0603 | PC13 -> R9 (330R) -> D3 -> 3V3 |
| SW2 | User button | E-stop / mode | PA15 -> SW2 -> GND, R10 (10k) pull-up |

## 2. PCB layout plan

- **Board size/shape:** 60mm x 45mm, 2-layer, with mounting holes at all 4
  corners (this board bolts into a robot chassis).
- **Placement:** Motor driver (U3) and its terminal blocks (J4/J6) placed
  at one edge, close to the VMOTOR input (J1), keeping high-current traces
  short. MCU (U1) placed centrally, away from the H-bridge's switching
  noise. Encoder headers (J7/J8) placed near the board edge closest to
  where the motors/encoders physically mount.
- **Routing notes:**
  - Motor traces (H-bridge outputs to J4/J6) sized for peak current
    (DRV8833 supports up to ~1.5A/channel continuous) — use >=30mil traces
    or a poured copper area for motor power.
  - VMOTOR and its return path routed as a low-impedance pair, ideally a
    dedicated power plane region separate from the 3V3 logic plane, joined
    only at U2 (the regulator) and at a single star-ground point.
  - Keep the STM32 crystal (Y1) and encoder input traces away from the
    H-bridge switching outputs — H-bridges generate significant EMI at PWM
    edges.
  - Add a snubber/bulk cap (C7/C8) directly at U3's VM pin, not just
    somewhere on the rail.
- **Layer stackup:** 2-layer, 2oz copper on the bottom layer if motor
  currents exceed ~1A, to reduce trace heating; otherwise standard 1oz.

## 3. Bill of materials

| Qty | Ref | Part | Footprint | Example distributor P/N |
|---|---|---|---|---|
| 1 | U1 | STM32F401CCU6 | LQFP-48 | Digi-Key 497-16321-ND |
| 1 | U2 | MP2307DN buck regulator | SOIC-8 | Digi-Key MP2307DN-LF-Z-ND |
| 1 | U3 | DRV8833PWP | TSSOP-16 (HTSSOP w/ thermal pad) | Digi-Key 296-37870-1-ND |
| 1 | Y1 | 25MHz crystal | HC-49 SMD | Digi-Key 535-9764-1-ND |
| 2 | D1,D2 | Schottky diode SS34/SS14 | SMA/SOD-123 | Digi-Key any |
| 1 | J1 | 2-pin terminal block, 5mm pitch | THT | Digi-Key ED2609-ND |
| 1 | J5 | USB Micro-B | SMD | Digi-Key 609-4618-1-ND |
| 1 | J3 | 2x2 header 2.54mm | THT | Digi-Key any |
| 4 | J4,J6-J8 | Terminal blocks / 4-pin headers | THT | Digi-Key per type |
| 2 | SW1,SW2 | Tactile switch 6x6mm | SMD | Digi-Key 450-1650-ND |
| 2 | D3 | LED 0603 | 0603 | Digi-Key any 0603 |
| ~10 | R1-R10 | 330R-10k assorted | 0603 | Digi-Key any 0603 |
| ~8 | C1-C8 | 10pF-22uF assorted | 0603/0805 | Digi-Key per value |

## Firmware

[`firmware/main.c`](firmware/main.c) — STM32 HAL, structured for a
CubeMX-generated STM32F401 project. Open-loop PWM speed/direction control
for both motors via TIM1's 4 PWM channels, quadrature position read from
TIM2/TIM4 in hardware encoder mode, plus E-stop button and DRV8833
nFAULT handling. Peripheral init (`MX_TIM1_Init`, etc.) is CubeMX
boilerplate, left as comments; the control/readback logic is real. Wiring
the encoder counts into a PID loop (position or velocity) is the natural
next step — this file stops at open-loop + readback, same as [the
closed-loop PID project](../../embedded-projects/closed_loop_servo_pid)
in this repo, which is the piece to reuse for that.

Not bench-tested — I don't have the STM32F401/DRV8833/encoder hardware to
try it on. If you build this, double-check the `setMotorSpeed` sign
convention against your actual DRV8833 wiring before trusting which
direction is "forward" — that's the kind of thing that's easy to get
backwards on paper.
