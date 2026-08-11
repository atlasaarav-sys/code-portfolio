# Aarav Artham — Coding & Hardware Portfolio

Personal practice repo, organized into exactly two top-level categories —
**software** and **hardware** — covering language fundamentals, deeper
software tracks (systems C++, real applications, machine learning/computer
vision), and embedded firmware/board designs for ESP32, STM32, and
Arduino.

## Structure

```
software/
  python/
    01_basics_syntax -> 02_data_structures -> 03_todo_cli_app   (fundamentals)
    apps/                                                        (11 real applications)
  c/
    01_basics_syntax -> 02_data_structures -> 03_mini_shell      (fundamentals)
  cpp/
    01_basics_syntax -> 02_data_structures -> 03_bank_system     (fundamentals)
    advanced/                                                     (10 systems-level projects)
  machine-learning/
    computer-vision/                                              (10 projects)
  misc-projects/                                                   (5 projects: REST API, CLI, full-stack, DSA, CI/CD)
  portfolio-website/                                               (personal portfolio site, single-file HTML/CSS/JS)

hardware/
  esp32/               9 projects, beginner -> advanced (GPIO/I2C/SPI/UART/WiFi/MQTT/BLE)
  stm32/               4 projects, beginner -> advanced (GPIO/PWM/SDIO+USB/CAN)
  arduino/             1 project (motion-tracking pan-tilt camera rig)
  embedded-projects/   2 projects that pair custom firmware with a PC-side app/sim
  3d-models/           original SolidWorks CAD work (differential gearbox, 4-cyl engine, battle bot) + portfolio deck
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

**[software/python/apps](software/python/apps)** — 11 real applications,
mostly stdlib-only:

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
| AI-assisted telemetry diagnostics | Python, LLM (optional), statistical anomaly detection |

Every one of these was actually run (including starting servers and
driving them with scripted clients) while building this repo.

**[software/cpp/advanced](software/cpp/advanced)** — 10 systems-level
C++17 projects: a pool allocator, a lock-free SPSC ring buffer, a
work-stealing thread pool, an LRU cache, a JSON parser, a regex engine
(Thompson NFA), an AVL tree, graph algorithms, a shunting-yard expression
evaluator, and custom `unique_ptr`/`shared_ptr`. Not machine-compiled in
the authoring environment — each has a `Makefile`, build locally with
`make`.

**[software/machine-learning/computer-vision](software/machine-learning/computer-vision)**
— 10 projects: edge detection and k-means segmentation from scratch in
numpy, Haar cascade face detection, Lucas-Kanade optical flow tracking,
ORB-based panorama stitching, a from-scratch numpy neural net trained on
real handwritten digit data (98%+ test accuracy), GrabCut background
removal, license plate localization + OCR, a PyTorch CNN classifier, and
neural style transfer.

**[software/misc-projects](software/misc-projects)** — five projects
covering the fundamentals employers screen for day-to-day, each with a
real, actually-run test suite:

| Project | One-liner | Tech tags |
|---|---|---|
| [01_rest_api_notes_crud](software/misc-projects/01_rest_api_notes_crud) | Full CRUD REST API for a notes resource | Python, Flask, SQLite |
| [02_cli_git_changelog](software/misc-projects/02_cli_git_changelog) | Generates a grouped CHANGELOG.md from git log | Python, stdlib, Conventional Commits |
| [03_fullstack_bookmarks_app](software/misc-projects/03_fullstack_bookmarks_app) | Multi-user bookmarks app with session auth | Python, Flask, SQLite, Docker |
| [04_algorithms_toolkit](software/misc-projects/04_algorithms_toolkit) | Sorting/searching/graph algorithms with tests + empirical benchmark | Python, `unittest` |
| [05_dockerized_url_monitor](software/misc-projects/05_dockerized_url_monitor) | Uptime monitor with a live status page | Python, Docker, GitHub Actions |

**[software/portfolio-website](software/portfolio-website)** — this
portfolio's own personal site: a single-file, dark-themed, mobile-first
HTML/CSS/JS page (Home/About/Projects, smooth-scroll nav, scroll-reveal
animation) with no build step or framework.

## Hardware

Sixteen projects across ESP32, STM32, Arduino, and cross-platform embedded
builds — see [hardware/README.md](hardware/README.md) for the full index,
per-project protocol tags, a protocol-diversity map (I2C/UART/SPI/
WiFi-MQTT/BLE/CAN, one flagship project per protocol, no repeats), and
firmware status notes. Every project has a component/connection list,
most have a PCB layout plan + BOM, and **every project has real firmware
source code** in a `firmware/` subfolder (written and reviewed, not
flashed/compiled in this environment — see each README's Firmware section
for specifics).

| Track | Projects | Protocols covered |
|---|---|---|
| [ESP32](hardware/esp32) | 9 (beginner -> advanced) | GPIO, I2C, SPI, WiFi, WiFi+MQTT, UART, BLE |
| [STM32](hardware/stm32) | 4 (beginner -> advanced) | GPIO, PWM/Timer, SDIO+USB, CAN+I2C |
| [Arduino](hardware/arduino) | 1 | Serial (USB), OpenCV motion tracking |
| [Embedded projects](hardware/embedded-projects) | 2 | Firmware + PC-side app/simulator pairs |

**[hardware/embedded-projects](hardware/embedded-projects)** — two
projects where the firmware is only half the story:

- [closed_loop_servo_pid](hardware/embedded-projects/closed_loop_servo_pid) — portable C PID controller core (Arduino + STM32 HAL integration sketches) plus a Python simulator that validates the overshoot/settling-time improvement from closed-loop control vs. open-loop.
- [rpi_cluster_arduino_datacenter](hardware/embedded-projects/rpi_cluster_arduino_datacenter) — C++ thread-pool task scheduler (stands in for a 5-node Pi cluster), Arduino sketches for remote device control and scheduled automation, and a Python cluster logging/diagnostics tool.

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
