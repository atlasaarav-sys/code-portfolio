# Aarav Artham — Coding & Hardware Portfolio

Personal practice repo combining software (Python / C / C++) and hardware
(ESP32 / STM32) projects, organized from beginner to advanced.

## Structure

```
coding/
  python/    01_basics_syntax -> 02_data_structures -> 03_todo_cli_app
  c/         01_basics_syntax -> 02_data_structures -> 03_mini_shell
  cpp/       01_basics_syntax -> 02_data_structures -> 03_bank_system
hardware/
  esp32/     4 projects, beginner -> advanced (schematics, PCB plan, BOM)
  stm32/     4 projects, beginner -> advanced (schematics, PCB plan, BOM)
projects/
  ai_telemetry_diagnostics/        Python + LLM telemetry diagnostics pipeline
  closed_loop_servo_pid/           embedded PID servo control (C firmware + sim)
  rpi_cluster_arduino_datacenter/  C++ task scheduler + Arduino device control/automation
  smart_energy_monitor_esp32/      ESP32 energy monitoring + relay optimization
```

Each project folder has its own `README.md` with a description, what it
demonstrates, and how to build/run it. New projects should follow the same
template (see `TEMPLATE_README.md`).

## Coding projects

| Language | Level 1 | Level 2 | Level 3 |
|---|---|---|---|
| Python | basics/syntax | data structures (stack/queue/BST) | Todo CLI app (JSON persistence) |
| C | basics/syntax | linked list + hash table | mini shell (fork/exec, pipes) |
| C++ | basics/syntax (OOP) | data structures (templates, smart ptrs) | bank account system (classes, files) |

## Hardware projects

See [hardware/esp32](hardware/esp32) and [hardware/stm32](hardware/stm32) for
full write-ups. Each includes a component/connection list (schematic), a PCB
layout plan (placement, routing, stackup), and a bill of materials.

## Resume projects

`projects/` rebuilds the four Project Experience entries from my resume,
each with a working prototype (not just a description):

- [ai_telemetry_diagnostics](projects/ai_telemetry_diagnostics) — Python pipeline that ingests CAN-bus/sensor telemetry CSVs, runs statistical anomaly detection, and generates plain-language diagnostic summaries (LLM-backed, with a rule-based offline fallback).
- [closed_loop_servo_pid](projects/closed_loop_servo_pid) — portable C PID controller core (Arduino + STM32 HAL integration sketches) plus a Python simulator that validates the overshoot/settling-time improvement from closed-loop control vs. open-loop.
- [rpi_cluster_arduino_datacenter](projects/rpi_cluster_arduino_datacenter) — C++ thread-pool task scheduler (stands in for a 5-node Pi cluster), Arduino sketches for remote device control and scheduled automation, and a Python cluster logging/diagnostics tool.
- [smart_energy_monitor_esp32](projects/smart_energy_monitor_esp32) — ESP32 firmware reading light/temperature, filtering + hysteresis decision logic driving a relay, OLED display, and a Python simulator quantifying the false-trigger reduction and estimated energy savings.

## Getting started

```bash
git clone <your-repo-url>
cd Portfolio
```

Python projects: `python3 <script>.py` (no external deps unless noted in the
project README).

C/C++ projects: each folder has a `Makefile`; run `make` then run the
produced binary.
