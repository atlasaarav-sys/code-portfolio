# ESP32-07 — WiFi/MQTT Telemetry Node

**Level:** Intermediate
**Protocol focus:** WiFi + MQTT (publish telemetry, subscribe to commands)
**Stack:** Arduino framework (ESP32 core), `PubSubClient`, `ArduinoJson`

## Purpose

A wireless sensor node: reads a light level (LDR) and reports it as a
JSON payload to an MQTT broker over WiFi every 5 seconds, while
subscribing to a command topic that can remotely switch a relay — the
canonical "ESP32 as an IoT sensor+actuator node" pattern, with automatic
WiFi/MQTT reconnect handling (the part that actually breaks in the field
when a router hiccups, which naive tutorials skip).

## Wiring / pinout

| ESP32 pin | Connects to | Notes |
|---|---|---|
| GPIO34 (ADC1_CH6, input-only) | LDR voltage divider | Light sensor reading, 0-4095 raw ADC |
| GPIO26 | Relay module IN | Remotely controlled via the `esp32/telemetry_node/cmd` MQTT topic |
| GPIO2 | Status LED (through ~330R) | Off = no WiFi, blinking = WiFi but no MQTT, solid = fully connected |
| 3V3 | LDR divider top, relay module VCC (if 3.3V-logic relay) | Use an opto-isolated relay module rated for your relay's coil voltage |
| GND | LDR divider bottom, relay module GND | Common ground |

## Setup instructions

1. Install libraries via Arduino Library Manager: `PubSubClient` (Nick
   O'Leary), `ArduinoJson` (Benoit Blanchon).
2. Edit the config block at the top of
   [`firmware/mqtt_telemetry_node.ino`](firmware/mqtt_telemetry_node.ino):
   `WIFI_SSID`, `WIFI_PASSWORD`, `MQTT_BROKER`, `MQTT_PORT`.
3. Run a broker to test against if you don't have one — the quickest path
   is a public test broker (e.g. `test.mosquitto.org`, no auth, not for
   anything sensitive) or `docker run -p 1883:1883 eclipse-mosquitto` on
   your own network.
4. Flash the firmware, then subscribe to `esp32/telemetry_node/data` with
   any MQTT client (`mosquitto_sub -h <broker> -t 'esp32/telemetry_node/#'
   -v`) to watch telemetry arrive, and publish `"ON"`/`"OFF"` to
   `esp32/telemetry_node/cmd` to toggle the relay remotely.

Compiles clean with PubSubClient + ArduinoJson pulled in — 907,748 bytes
flash (69%, WiFi/MQTT/JSON add up fast on a bare WROOM-32), 46,880 bytes
RAM (14%).

## Photos / demo

*(placeholder — add a photo of the wired breadboard and/or a terminal
screen-recording GIF of `mosquitto_sub` showing live telemetry)*

## What I learned / why this matters

The reconnect logic is most of the real engineering here: `PubSubClient`
silently stops delivering messages if the connection drops and you don't
notice, so `ensureMqttConnected()` checks `client.connected()` every loop
iteration and re-subscribes on reconnect (subscriptions don't survive a
disconnect on most brokers). WiFi itself needs the same treatment — this
firmware checks `WiFi.status()` and re-runs `WiFi.begin()` if the link
drops, rather than assuming a one-time `setup()` connection lasts forever,
which is the assumption that makes IoT demos work on a bench and then die
in the field the first time a router reboots.
