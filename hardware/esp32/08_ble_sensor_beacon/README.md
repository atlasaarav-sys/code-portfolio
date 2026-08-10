# ESP32-08 — BLE Sensor Beacon

**Level:** Intermediate
**Protocol focus:** Bluetooth Low Energy (GATT server, notify characteristic)
**Stack:** Arduino framework (ESP32 core), built-in `BLEDevice`/`BLEServer`
(from `esp32-BLE-Arduino`, bundled with the ESP32 board package)

## Purpose

A wireless sensor beacon with no WiFi network required: exposes a
potentiometer (standing in for any analog sensor) as a BLE GATT
characteristic that notifies subscribed clients whenever the value
changes by more than a threshold, plus a second read/write characteristic
for remote LED control — the "phone app talks directly to the board over
Bluetooth" pattern, testable with a generic tool (nRF Connect) with no
custom app or broker needed.

## Wiring / pinout

| ESP32 pin | Connects to | Notes |
|---|---|---|
| GPIO34 (ADC1_CH6, input-only) | Potentiometer wiper | Sensor value exposed as a BLE notify characteristic |
| GPIO2 | Onboard/status LED (through ~330R) | Controlled remotely via the BLE write characteristic; also blinks to show advertising state |
| 3V3 | Potentiometer one outer pin | |
| GND | Potentiometer other outer pin | |

## Setup instructions

1. No extra libraries needed — `BLEDevice`, `BLEServer`, `BLEUtils`, and
   `BLE2902` ship with the ESP32 Arduino board package.
2. Flash [`firmware/ble_sensor_beacon.ino`](firmware/ble_sensor_beacon.ino).
3. On a phone, install **nRF Connect for Mobile** (Nordic Semiconductor,
   free), scan for `ESP32-SensorBeacon`, connect, and:
   - Enable notifications on the sensor characteristic
     (`4a981234-...-...-...-000000000001`) to watch live values as you
     turn the potentiometer.
   - Write `01` or `00` (as a byte) to the LED characteristic
     (`...-000000000002`) to turn the onboard LED on/off remotely.

## Photos / demo

*(placeholder — add a screen-recording GIF of nRF Connect showing live
notification values as the potentiometer is turned)*

## What I learned / why this matters

BLE's GATT model (services containing characteristics, each with
read/write/notify properties) is a genuinely different mental model from
WiFi/MQTT's pub-sub — instead of pushing to a broker, you're exposing a
typed "remote variable" that clients discover and subscribe to directly.
The `BLE2902` descriptor is the easy thing to forget: without registering
it on a characteristic, `notify()` calls silently do nothing because the
client never actually enabled notifications at the protocol level — that
descriptor *is* the "please notify me" switch, and missing it is the
single most common reason a first BLE notify project "doesn't work."
