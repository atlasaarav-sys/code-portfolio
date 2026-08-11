# Hardware Projects

Sixteen hardware projects, beginner to advanced, across ESP32, STM32,
Arduino, and cross-platform embedded builds, plus a CAD/3D-models track
of original SolidWorks mechanical design work. Each firmware project
folder contains a `README.md` covering:

1. **Schematic (component/connection list)** — every part, its value/part
   number, and exactly what pin connects to what. This is what you'd
   translate into a KiCad schematic sheet.
2. **PCB layout plan** — placement strategy, routing notes (trace widths,
   keepouts, decoupling placement), and layer stackup. (Projects 05-08 in
   the ESP32 track are breadboard/module builds documented with a wiring
   table instead — no custom PCB, so no layout plan section.)
3. **Bill of materials** — a table with part, value/footprint, qty, and a
   typical distributor part number (Digi-Key/Mouser/LCSC) you can search.
4. **Firmware** — every project has real source code in a `firmware/`
   subfolder. The ESP32 and Arduino sketches compile clean against their
   real cores/libraries via `arduino-cli` (each README lists the actual
   flash/RAM numbers). STM32 firmware targets a CubeMX-generated project.

## ESP32 track (beginner -> advanced)

| # | Project | Level | Protocol focus | Highlights |
|---|---|---|---|---|
| 1 | [Blink + Button Dev Board](esp32/01_blink_button/README.md) | Beginner | GPIO | Bare ESP32-WROOM-32 board, USB-UART, one LED, one button |
| 2 | [Environmental Logger](esp32/02_environmental_logger/README.md) | Beginner-Intermediate | **I2C** | BME280 + OLED, LiPo charging, deep sleep |
| 3 | [WiFi Weather Station](esp32/03_wifi_weather_station/README.md) | Intermediate | SPI + I2C + **WiFi** | TFT display, DS3231 RTC, microSD logging, NTP sync |
| 4 | [LoRa IoT Sensor Node](esp32/04_lora_iot_node/README.md) | Advanced | SPI + I2C | LoRa radio, multi-sensor, deep-sleep power management |
| 5 | [UART GPS Logger](esp32/05_uart_gps_logger/README.md) | Intermediate | **UART** | NMEA parsing, OLED live fix, LittleFS track log |
| 6 | [SPI SD Card Data Logger](esp32/06_spi_sd_data_logger/README.md) | Intermediate | **SPI** | BME280 + microSD CSV logging, start/stop button |
| 7 | [WiFi/MQTT Telemetry Node](esp32/07_wifi_mqtt_telemetry_node/README.md) | Intermediate | **WiFi + MQTT** | Publishes sensor JSON, subscribes to remote relay control |
| 8 | [BLE Sensor Beacon](esp32/08_ble_sensor_beacon/README.md) | Intermediate | **BLE** | GATT notify characteristic + remote LED control, testable via nRF Connect |
| 9 | [Smart Energy Monitor](esp32/09_smart_energy_monitor/README.md) | Intermediate | I2C-adjacent (analog + relay) | Light/temp-based relay optimization, filtered threshold + hysteresis logic, OLED |

Projects 5-8 were added specifically to round out protocol coverage (UART,
SPI, WiFi/MQTT, BLE) — see [Protocol diversity](#protocol-diversity) below.

## STM32 track (beginner -> advanced)

| # | Project | Level | Protocol focus | Highlights |
|---|---|---|---|---|
| 1 | [Blue Pill Style Dev Board](stm32/01_blue_pill_dev_board/README.md) | Beginner | GPIO | STM32F103C8T6, SWD header, LED, button, 3.3V reg |
| 2 | [Dual Motor Driver Board](stm32/02_motor_driver_board/README.md) | Intermediate | PWM/Timer | STM32F401, DRV8833 dual H-bridge, quadrature encoder inputs |
| 3 | [USB Data Acquisition Board](stm32/03_usb_daq_board/README.md) | Intermediate-Advanced | SDIO + **USB** | STM32F405, DMA-fed ADC, microSD logging, USB-CDC streaming |
| 4 | [CAN + USB-C Sensor Hub](stm32/04_can_sensor_hub/README.md) | Advanced | **CAN** + I2C | STM32F405, CAN transceiver, IMU, USB-C debug console |

## Arduino track

| # | Project | Level | Protocol focus | Highlights |
|---|---|---|---|---|
| 1 | [Motion-Tracking Pan-Tilt Camera Rig](arduino/01_motion_tracking_pan_tilt_camera/README.md) | Beginner-Intermediate | Serial (USB) | Arduino Uno + 2 servos, OpenCV background-subtraction tracking, PC-to-Arduino serial control |

This one's a rebuild of code I was given (`motion_tracker.py` +
`pan_tilt_controller.ino`) rather than something designed from scratch —
the README documents the actual wiring those files assume, plus an
optional servo breakout shield PCB on top of the base Uno-and-jumper-wires
build.

## Embedded projects (cross-platform)

Two projects where the firmware is only half the story — each pairs
custom firmware with a PC-side application or simulator, and doesn't fit
neatly under a single board track since one targets multiple platforms
and the other targets a Raspberry Pi cluster rather than a single custom
board.

| Project | Level | Highlights |
|---|---|---|
| [Closed-Loop Servo PID Control](embedded-projects/closed_loop_servo_pid/README.md) | Intermediate | Portable C PID core, Arduino + STM32 HAL integration sketches, Python simulator validating overshoot/settling-time improvement |
| [Raspberry Pi Cluster & Arduino Data Center](embedded-projects/rpi_cluster_arduino_datacenter/README.md) | Intermediate-Advanced | C++ thread-pool scheduler (5-node Pi cluster stand-in), Arduino device-control/automation sketches, Python cluster logging tool |

## CAD / 3D models

Original SolidWorks mechanical design work — see
[3d-models/README.md](3d-models/README.md) for details.

| Project | Highlights |
|---|---|
| [Differential Gear Box](3d-models/differential-gear-box) | Full gearbox assembly — housing + four gears |
| [Four Cylinder Engine](3d-models/four-cylinder-engine) | Inline 4-cylinder engine assembly — piston, crankshaft, connecting rod |
| [Battle Bot](3d-models/battle-bot) | Combat robot chassis part, wheel design, and a released dimensioned drawing |
| [Portfolio Deck](3d-models/portfolio-deck) | SolidWorks design portfolio slide deck (.pptx + PDF) |

## Protocol diversity

Across the flagship set of projects, every protocol the portfolio audit
asked for is represented by at least one project, with no repeats needed:

| Protocol | Project |
|---|---|
| I2C | [ESP32-02 Environmental Logger](esp32/02_environmental_logger/README.md) — BME280 + OLED |
| UART | [ESP32-05 GPS Logger](esp32/05_uart_gps_logger/README.md) — NMEA sentence parsing |
| SPI | [ESP32-06 SD Card Data Logger](esp32/06_spi_sd_data_logger/README.md) — microSD over SPI |
| WiFi/MQTT | [ESP32-07 WiFi/MQTT Telemetry Node](esp32/07_wifi_mqtt_telemetry_node/README.md) |
| BLE | [ESP32-08 BLE Sensor Beacon](esp32/08_ble_sensor_beacon/README.md) — GATT notify characteristic |
| CAN | [STM32-04 CAN Sensor Hub](stm32/04_can_sensor_hub/README.md) — bxCAN broadcast |

(Several other projects layer in additional protocols on top of their
main focus — e.g. ESP32-03 uses SPI *and* I2C *and* WiFi, STM32-03 uses
SDIO and USB — see each project's own table for the full picture.)

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

Practical path instead: every custom-PCB project's component/connection
list already gives you the exact part, value, and pin mapping — that's
normally a 20-60 minute job to lay out directly in KiCad's schematic
editor per board, and you'll end up with a schematic you've actually
verified yourself rather than one generated blind.
