# Hardware Projects

Eight hardware projects, beginner to advanced, split across ESP32 and STM32.
Each project folder contains a single `README.md` with three sections:

1. **Schematic (component/connection list)** — every part, its value/part
   number, and exactly what pin connects to what. This is what you'd
   translate into a KiCad schematic sheet.
2. **PCB layout plan** — placement strategy, routing notes (trace widths,
   keepouts, decoupling placement), and layer stackup.
3. **Bill of materials** — a table with part, value/footprint, qty, and a
   typical distributor part number (Digi-Key/Mouser/LCSC) you can search.

None of these have been fabricated or bench-tested — treat them as a solid
first-pass design to build in KiCad and review (especially power budgets and
decoupling) before ordering boards.

## ESP32 track (beginner -> advanced)

| # | Project | Level | Highlights |
|---|---|---|---|
| 1 | [Blink + Button Dev Board](esp32/01_blink_button/README.md) | Beginner | Bare ESP32-WROOM-32 board, USB-UART, one LED, one button |
| 2 | [Environmental Logger](esp32/02_environmental_logger/README.md) | Beginner-Intermediate | I2C BME280 + OLED, LiPo charging, on/off switch |
| 3 | [WiFi Weather Station](esp32/03_wifi_weather_station/README.md) | Intermediate | TFT display, RTC, microSD logging, WiFi |
| 4 | [LoRa IoT Sensor Node](esp32/04_lora_iot_node/README.md) | Advanced | LoRa radio, multi-sensor, deep-sleep power management, USB-C |

## STM32 track (beginner -> advanced)

| # | Project | Level | Highlights |
|---|---|---|---|
| 1 | [Blue Pill Style Dev Board](stm32/01_blue_pill_dev_board/README.md) | Beginner | STM32F103C8T6, SWD header, LED, button, 3.3V reg |
| 2 | [Dual Motor Driver Board](stm32/02_motor_driver_board/README.md) | Intermediate | STM32F401, DRV8833 dual H-bridge, quadrature encoder inputs |
| 3 | [USB Data Acquisition Board](stm32/03_usb_daq_board/README.md) | Intermediate-Advanced | STM32F405, USB FS, microSD logging, multi-channel ADC front end |
| 4 | [CAN + USB-C Sensor Hub](stm32/04_can_sensor_hub/README.md) | Advanced | STM32F405, CAN transceiver, USB-C (PD-negotiated 5V), multi-sensor |

## KiCad files

I tried scripting a real `.kicad_sch` for the simplest board (ESP32-01) by
hand-assembling the s-expression format and pulling real symbols from the
installed KiCad 10 library (`RF_Module:ESP32-WROOM-32E`, `Device:R`,
`Device:LED`, etc.). Running KiCad's own `kicad-cli sch erc` against the
result surfaced 38 wiring/dangling-endpoint violations from small
pin-rotation and coordinate errors that are hard to get exactly right
without iterating in the live schematic editor. Rather than hand you a file
that opens in KiCad and *looks* legit but is subtly wrong, I dropped that
approach.

Practical path instead: every project's component/connection list below
already gives you the exact part, value, and pin mapping — that's normally
a 20-60 minute job to lay out directly in KiCad's schematic editor per
board, and you'll end up with a schematic you've actually verified yourself
rather than one generated blind.
