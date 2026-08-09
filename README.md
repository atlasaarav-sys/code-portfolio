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

## Getting started

```bash
git clone <your-repo-url>
cd Portfolio
```

Python projects: `python3 <script>.py` (no external deps unless noted in the
project README).

C/C++ projects: each folder has a `Makefile`; run `make` then run the
produced binary.
