# Aarav Artham — Coding & Hardware Portfolio

Personal practice repo combining software (Python / C / C++), machine
learning / computer vision, hardware (ESP32 / STM32 / Arduino), and a set
of featured projects rebuilding my resume's Project Experience entries as
working prototypes.

## Structure

```
software/
  python/       01_basics_syntax -> 02_data_structures -> 03_todo_cli_app, plus apps/ (10 real stdlib apps)
  c/            01_basics_syntax -> 02_data_structures -> 03_mini_shell
  cpp/          01_basics_syntax -> 02_data_structures -> 03_bank_system, plus advanced/ (10 systems-level projects)

machine-learning/
  computer-vision/   10 projects: classical CV (tested) + deep learning (written, untested)

hardware/
  esp32/        4 projects, beginner -> advanced (schematics, PCB plan, BOM)
  stm32/        4 projects, beginner -> advanced (schematics, PCB plan, BOM)
  arduino/      1 project (motion-tracking pan-tilt camera rig)

featured-projects/
  ai_telemetry_diagnostics/        Python + LLM telemetry diagnostics pipeline
  closed_loop_servo_pid/           embedded PID servo control (C firmware + sim)
  rpi_cluster_arduino_datacenter/  C++ task scheduler + Arduino device control/automation
  smart_energy_monitor_esp32/      ESP32 energy monitoring + relay optimization
```

Each project folder has its own `README.md` with a description, what it
demonstrates, and how to build/run it. New fundamentals-track projects
should follow the same template (see `TEMPLATE_README.md`).

## Software

**Python, C, and C++ fundamentals** — three projects each, increasing
difficulty (basics/syntax -> data structures -> a small app):

| Language | Level 1 | Level 2 | Level 3 |
|---|---|---|---|
| Python | basics/syntax | data structures (stack/queue/BST) | Todo CLI app (JSON persistence) |
| C | basics/syntax | linked list + hash table | mini shell (fork/exec, pipes) |
| C++ | basics/syntax (OOP) | data structures (templates, smart ptrs) | bank account system (classes, files) |

**[software/python/apps](software/python/apps)** — 10 real applications
using only the Python standard library: a Markdown static site generator,
a SQLite expense tracker, a file deduplicator, a URL shortener REST
service, a Markov text generator, a Redis-like key-value store server,
socket-based tic-tac-toe, an encrypted password manager CLI, an RSS feed
aggregator, and a threaded chat server. All 10 were actually run
(including starting servers and driving them with scripted clients) while
building this repo.

**[software/cpp/advanced](software/cpp/advanced)** — 10 systems-level
C++17 projects: a pool allocator, a lock-free SPSC ring buffer, a
work-stealing thread pool, an LRU cache, a JSON parser, a regex engine
(Thompson NFA), an AVL tree, graph algorithms, a shunting-yard expression
evaluator, and custom `unique_ptr`/`shared_ptr`. Not machine-compiled in
the authoring environment — each has a `Makefile`, build locally with
`make`.

## Machine learning / computer vision

**[machine-learning/computer-vision](machine-learning/computer-vision)** —
10 projects: edge detection and k-means segmentation from scratch in
numpy, Haar cascade face detection, Lucas-Kanade optical flow tracking,
ORB-based panorama stitching, a from-scratch numpy neural net trained on
real handwritten digit data (98%+ test accuracy), GrabCut background
removal, license plate localization + OCR, a PyTorch CNN classifier, and
neural style transfer. The classical CV and numpy-ML projects were
actually run and verified against known ground truth; the two PyTorch
deep-learning projects are written but untested (no PyTorch install in
this environment) — each README says exactly which category it's in.

## Hardware

See [hardware/esp32](hardware/esp32), [hardware/stm32](hardware/stm32), and
[hardware/arduino](hardware/arduino) for full write-ups. Each includes a
component/connection list (schematic), a PCB layout plan (placement,
routing, stackup), and a bill of materials.

## Featured projects

**[featured-projects/](featured-projects)** rebuilds the four Project
Experience entries from my resume, each with a working prototype (not
just a description):

- [ai_telemetry_diagnostics](featured-projects/ai_telemetry_diagnostics) — Python pipeline that ingests CAN-bus/sensor telemetry CSVs, runs statistical anomaly detection, and generates plain-language diagnostic summaries (LLM-backed, with a rule-based offline fallback).
- [closed_loop_servo_pid](featured-projects/closed_loop_servo_pid) — portable C PID controller core (Arduino + STM32 HAL integration sketches) plus a Python simulator that validates the overshoot/settling-time improvement from closed-loop control vs. open-loop.
- [rpi_cluster_arduino_datacenter](featured-projects/rpi_cluster_arduino_datacenter) — C++ thread-pool task scheduler (stands in for a 5-node Pi cluster), Arduino sketches for remote device control and scheduled automation, and a Python cluster logging/diagnostics tool.
- [smart_energy_monitor_esp32](featured-projects/smart_energy_monitor_esp32) — ESP32 firmware reading light/temperature, filtering + hysteresis decision logic driving a relay, OLED display, and a Python simulator quantifying the false-trigger reduction and estimated energy savings.

## Getting started

```bash
git clone <your-repo-url>
cd Portfolio
```

Python projects: `python3 <script>.py` (no external deps unless noted in
the project README).

C/C++ projects: each folder has a `Makefile`; run `make` then run the
produced binary.
