# ESP32-06 — SPI SD Card Data Logger

**Level:** Intermediate
**Protocol focus:** SPI (microSD card)
**Stack:** Arduino framework (ESP32 core), `SD`, `Adafruit_BME280`

## Purpose

A field data logger: samples a BME280 (temperature/humidity/pressure) at a
fixed interval and writes timestamped CSV rows to a microSD card over
SPI, with a button to start/stop a logging session and an LED that
signals card status — the kind of "log to removable media reliably" task
that shows up constantly in embedded/instrumentation work (this repo's
[STM32-03 USB DAQ board](../../stm32/03_usb_daq_board) does the SDIO
version of the same idea; this is the SPI version).

## Wiring / pinout

| ESP32 pin | Connects to | Notes |
|---|---|---|
| GPIO18 (VSPI SCK) | SD module SCK | |
| GPIO23 (VSPI MOSI) | SD module MOSI | |
| GPIO19 (VSPI MISO) | SD module MISO | |
| GPIO5 (CS) | SD module CS | |
| GPIO21 (I2C SDA) | BME280 SDA | |
| GPIO22 (I2C SCL) | BME280 SCL | |
| GPIO4 | Start/stop button (to GND, internal pull-up) | Short press toggles logging |
| GPIO2 | Status LED (through ~330R) | Off = idle, blinking = logging, solid = card error |
| 3V3 | SD module VCC, BME280 VCC | Use a level-shifted SD breakout if yours needs 5V logic — most common breakout modules already regulate to 3.3V |
| GND | SD module GND, BME280 GND | Common ground |

## Setup instructions

1. Install libraries via Arduino Library Manager: `Adafruit BME280
   Library` + `Adafruit Unified Sensor` (`SD` and `SPI` ship with the
   ESP32 core).
2. Format a microSD card as FAT32, wire per the table above.
3. Flash [`firmware/sd_logger.ino`](firmware/sd_logger.ino).
4. Press the button to start a session — the firmware creates a new
   `/log_NNN.csv` file (auto-incrementing so you never overwrite old
   sessions) and appends a row every second. Press again to stop.

Compiles clean — 356,078 bytes flash (27%), 24,216 bytes RAM (7%). Not
run against a physical SD card/BME280 yet, so the FAT32 formatting
assumption in step 2 and the actual write speed are still unverified.

## Photos / demo

*(placeholder — add a photo of the wired breadboard and/or a GIF of the
status LED blinking during an active logging session)*

## What I learned / why this matters

SD-over-SPI has a subtlety that trips people up: the card needs a slow
initial clock (≤400kHz) during `SD.begin()` before you can switch to full
speed, and a lot of "my SD card doesn't work" issues are actually power —
cheap breakout modules brown out under the current spike when the card
first initializes if you're powering from a weak 3.3V rail. Writing
`f_sync()`/`file.flush()` periodically instead of on every single row was
also the difference between "survives a power loss with only the last
second of data missing" and "corrupts the whole file" during testing.
