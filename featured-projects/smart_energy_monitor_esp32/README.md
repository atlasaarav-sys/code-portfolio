# Smart Energy Monitoring & Optimization System (Embedded IoT)

**Stack:** ESP32 (Arduino framework, C++), Python (dependency-free
simulator for the decision logic)

Reads ambient light and temperature, estimates power consumption /
inefficient-usage conditions, and actuates a relay to cut power to a
device when usage looks wasteful (e.g. a light left on in a bright room,
or HVAC running against an open window) — with an OLED showing live
readings. Rebuilt from the description on my resume.

## Files

- `firmware/energy_monitor.ino` — ESP32 Arduino sketch: reads an LDR
  (light, ADC) and a TMP36-style analog temp sensor, runs a moving-average
  filter on both (noise reduction), applies threshold + hysteresis decision
  logic to decide "usage is inefficient" -> drives a relay, and updates an
  SSD1306 OLED with live readings and relay state. Samples fast enough to
  keep decision latency under 100 ms.
- `sim/energy_sim.py` — ports the exact same filtering + threshold +
  hysteresis logic to Python and runs it against a simulated day of
  light/temperature data (with realistic sensor noise), so the two claims
  on my resume are things you can regenerate:
  - **false-trigger reduction** from adding the moving-average filter +
    hysteresis band, vs. a naive instant-threshold comparator
  - **simulated energy savings** from cutting power during detected
    inefficient-usage windows

## How to run

```bash
cd sim
python energy_sim.py
```

Prints a comparison table (naive vs. filtered decision logic: trigger
count, false-trigger count) and an estimated energy savings percentage,
and writes `energy_trace.csv` (time, light, temp, relay_state) for the run.

## Notes

`energy_monitor.ino` is not machine-compiled here (no ESP32 toolchain in
this environment) — flash it via the Arduino IDE (ESP32 board package)
before relying on it. Sensor thresholds (`LIGHT_BRIGHT_THRESHOLD`,
`TEMP_HIGH_THRESHOLD_C`) are illustrative defaults, tune them for your
actual room/sensor.
