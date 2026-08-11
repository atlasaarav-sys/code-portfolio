# ESP32-05 — UART GPS Logger

**Level:** Intermediate
**Protocol focus:** UART (hardware serial, NMEA sentence parsing)
**Stack:** Arduino framework (ESP32 core), `TinyGPS++`, `Adafruit_SSD1306`

## Purpose

A standalone GPS tracker: reads NMEA sentences from a GPS module over a
dedicated hardware UART, parses them into lat/lon/altitude/speed/satellite
count, shows a live fix on an OLED, and appends each fix to a CSV track
log in onboard flash (LittleFS) — a real "why is my UART parser dropping
sentences" project, not a blink-an-LED demo.

## Wiring / pinout

| ESP32 pin | Connects to | Notes |
|---|---|---|
| GPIO16 (UART2 RX) | GPS module TX | ESP32 receives NMEA sentences here |
| GPIO17 (UART2 TX) | GPS module RX | Only needed if you send config commands to the GPS; read-only use can leave this unconnected |
| GPIO21 (I2C SDA) | OLED SDA | Shared with GPIO22 for the display bus |
| GPIO22 (I2C SCL) | OLED SCL | |
| GPIO2 | Status LED (through ~330R) | Blinks once per second while waiting for a fix, solid once fixed |
| 3V3 | GPS module VCC, OLED VCC | Most NEO-6M/NEO-M8N modules run fine at 3.3V — check your specific module |
| GND | GPS module GND, OLED GND | Common ground |

Tested against a u-blox NEO-6M breakout (9600 baud default) and a
128x64 SSD1306 OLED; any NMEA-0183 GPS module and I2C SSD1306/SH1106
display should work with minor tweaks.

## Setup instructions

1. Install libraries via Arduino Library Manager: `TinyGPSPlus` (mikalhart),
   `Adafruit SSD1306`, `Adafruit GFX Library`.
2. Wire per the table above.
3. Flash [`firmware/gps_logger.ino`](firmware/gps_logger.ino).
4. Take the board outside (GPS needs sky visibility) and watch the OLED —
   it'll show "Waiting for fix..." until it acquires satellites (can take
   30s-2min cold start), then live lat/lon/speed/sat count.
5. Fixes are appended to `/track_log.csv` in LittleFS; pull it via a
   companion sketch or `esptool.py` if you want to extract logged tracks.

Compiles clean against the ESP32 core with the libraries above installed
— 349,772 bytes flash (26%), 24,132 bytes RAM (7%).

## Photos / demo

*(placeholder — add a photo of the assembled board and/or a GIF of the
OLED updating with a live fix once you've built one)*

## What I learned / why this matters

UART is deceptively simple until you're parsing a continuous stream of
variable-length, checksummed sentences arriving asynchronously to your
main loop — `TinyGPS++`'s character-at-a-time `encode()` API is a good
lesson in why you don't want to `Serial.readStringUntil('\n')` your way
through a real streaming protocol (you'll miss bytes that arrive between
loop iterations). This is also the most direct "point-to-point serial
link between two independent devices" project in this repo — most other
UART usage here is either a USB-serial debug console or wrapped inside a
library (LoRa/CAN), so this is the one that's just raw NMEA-over-UART.
