# Aarav Artham — Coding & Hardware Portfolio

Personal practice repo combining software (Python / C / C++), machine
learning / computer vision, hardware (ESP32 / STM32 / Arduino), a set of
featured projects rebuilding my resume's Project Experience entries as
working prototypes, and a handful of misc projects covering REST APIs,
CLI tooling, full-stack web, algorithms, and CI/CD.

## Structure

```
software/
  python/       01_basics_syntax -> 02_data_structures -> 03_todo_cli_app, plus apps/ (10 real stdlib apps)
  c/            01_basics_syntax -> 02_data_structures -> 03_mini_shell
  cpp/          01_basics_syntax -> 02_data_structures -> 03_bank_system, plus advanced/ (10 systems-level projects)

machine-learning/
  computer-vision/   10 projects: classical CV (tested) + deep learning (written, untested)

hardware/
  esp32/        8 projects, beginner -> advanced (I2C/UART/SPI/WiFi-MQTT/BLE)
  stm32/        4 projects, beginner -> advanced (PWM/USB/CAN)
  arduino/      1 project (motion-tracking pan-tilt camera rig)

featured-projects/
  ai_telemetry_diagnostics/        Python + LLM telemetry diagnostics pipeline
  closed_loop_servo_pid/           embedded PID servo control (C firmware + sim)
  rpi_cluster_arduino_datacenter/  C++ task scheduler + Arduino device control/automation
  smart_energy_monitor_esp32/      ESP32 energy monitoring + relay optimization

misc-projects/
  01_rest_api_notes_crud/          Flask + SQLite CRUD REST API
  02_cli_git_changelog/            git-log-to-CHANGELOG.md CLI tool
  03_fullstack_bookmarks_app/      Flask + SQLite + auth + Docker
  04_algorithms_toolkit/           sorting/searching/graph algorithms + tests + benchmark
  05_dockerized_url_monitor/       Dockerized service + GitHub Actions CI/CD
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
using only the Python standard library:

| Project | Tech tags |
|---|---|
| Markdown static site generator | Python, stdlib |
| SQLite expense tracker | Python, SQLite |
| File deduplicator | Python, hashlib |
| URL shortener REST service | Python, `http.server`, SQLite |
| Markov text generator | Python, stdlib |
| Redis-like key-value store server | Python, sockets, threading |
| Socket-based tic-tac-toe | Python, sockets, threading |
| Encrypted password manager CLI | Python, PBKDF2/HMAC |
| RSS feed aggregator | Python, `urllib`, `xml.etree` |
| Threaded chat server | Python, sockets, threading |

All 10 were actually run (including starting servers and driving them
with scripted clients) while building this repo.

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

Seventeen projects across ESP32, STM32, and Arduino — see
[hardware/README.md](hardware/README.md) for the full index, per-project
protocol tags, a protocol-diversity map (I2C/UART/SPI/WiFi-MQTT/BLE/CAN,
one flagship project per protocol, no repeats), and firmware status notes.
Every project has a component/connection list, most have a PCB layout
plan + BOM, and **every project now has real firmware source code** in a
`firmware/` subfolder (written and reviewed, not flashed/compiled in this
environment — see each README's Firmware section for specifics).

| Track | Projects | Protocols covered |
|---|---|---|
| [ESP32](hardware/esp32) | 8 (beginner -> advanced) | GPIO, I2C, SPI, WiFi, WiFi+MQTT, UART, BLE |
| [STM32](hardware/stm32) | 4 (beginner -> advanced) | GPIO, PWM/Timer, SDIO+USB, CAN+I2C |
| [Arduino](hardware/arduino) | 1 | Serial (USB), OpenCV motion tracking |

## Featured projects

**[featured-projects/](featured-projects)** rebuilds the four Project
Experience entries from my resume, each with a working prototype (not
just a description):

- [ai_telemetry_diagnostics](featured-projects/ai_telemetry_diagnostics) — Python pipeline that ingests CAN-bus/sensor telemetry CSVs, runs statistical anomaly detection, and generates plain-language diagnostic summaries (LLM-backed, with a rule-based offline fallback).
- [closed_loop_servo_pid](featured-projects/closed_loop_servo_pid) — portable C PID controller core (Arduino + STM32 HAL integration sketches) plus a Python simulator that validates the overshoot/settling-time improvement from closed-loop control vs. open-loop.
- [rpi_cluster_arduino_datacenter](featured-projects/rpi_cluster_arduino_datacenter) — C++ thread-pool task scheduler (stands in for a 5-node Pi cluster), Arduino sketches for remote device control and scheduled automation, and a Python cluster logging/diagnostics tool.
- [smart_energy_monitor_esp32](featured-projects/smart_energy_monitor_esp32) — ESP32 firmware reading light/temperature, filtering + hysteresis decision logic driving a relay, OLED display, and a Python simulator quantifying the false-trigger reduction and estimated energy savings.

## Misc projects

**[misc-projects/](misc-projects)** — five projects covering the
fundamentals employers screen for day-to-day, each with a real,
actually-run test suite:

| Project | One-liner | Tech tags |
|---|---|---|
| [01_rest_api_notes_crud](misc-projects/01_rest_api_notes_crud) | Full CRUD REST API for a notes resource | Python, Flask, SQLite |
| [02_cli_git_changelog](misc-projects/02_cli_git_changelog) | Generates a grouped CHANGELOG.md from git log | Python, stdlib, Conventional Commits |
| [03_fullstack_bookmarks_app](misc-projects/03_fullstack_bookmarks_app) | Multi-user bookmarks app with session auth | Python, Flask, SQLite, Docker |
| [04_algorithms_toolkit](misc-projects/04_algorithms_toolkit) | Sorting/searching/graph algorithms with tests + empirical benchmark | Python, `unittest` |
| [05_dockerized_url_monitor](misc-projects/05_dockerized_url_monitor) | Uptime monitor with a live status page | Python, Docker, GitHub Actions |

## Getting started

```bash
git clone <your-repo-url>
cd Portfolio
```

Python projects: `python3 <script>.py` (no external deps unless noted in
the project README).

C/C++ projects: each folder has a `Makefile`; run `make` then run the
produced binary.

Arduino/ESP32/STM32 firmware: each `firmware/` folder README says which
libraries/toolchain to install and how to flash it.
