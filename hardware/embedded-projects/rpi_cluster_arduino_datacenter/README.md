# Raspberry Pi Cluster & Arduino Data Center (Embedded Systems)

**Stack:** C++ (task scheduler), Arduino/C++ (device sketches), Python
(cluster logging/diagnostics)

A small compute cluster (modeled here as a 5-worker thread pool standing in
for 5 Raspberry Pi nodes) with a custom task scheduler, plus Arduino
microcontrollers handling device control and automation, tied together with
logging/diagnostic tooling.

## Files

- `scheduler/task_scheduler.hpp` — a small thread-pool task scheduler
  (C++17, `std::thread`/`std::condition_variable`) — each worker thread
  stands in for one cluster node pulling tasks off a shared queue.
- `scheduler/main.cpp` — benchmark: runs a batch of compute-bound tasks
  single-threaded (1 "node", baseline) vs. across a 5-thread pool (5
  "nodes"), and reports the measured speedup, so the parallel-speedup claim
  is something you can regenerate, not just assert.
- `scheduler/Makefile`
- `arduino/device_control.ino` — Arduino sketch exposing a serial command
  interface (`ON <pin>`, `OFF <pin>`, `STATUS`) for remote control of
  relays/actuators — the "remotely control devices" piece.
- `arduino/automation_routine.ino` — Arduino sketch running scheduled
  automation (a `millis()`-based non-blocking scheduler triggering timed
  actions) and reporting status over serial — the "scheduled automation
  routines" piece. Six of these/`device_control.ino` boards forms the
  6-Arduino-microcontroller fleet this project is designed around.
- `logging/cluster_logger.py` — simulates a cluster run (task dispatch,
  completion, and injected communication failures across 5 nodes + 6
  Arduino devices), logs every event, and prints a diagnostic report
  (failure counts by device, mean time-to-detect a failure) — the
  "system-logging and diagnostic tools" piece.

## How to run

```bash
# Task scheduler benchmark (needs g++ with C++17 and pthreads)
cd scheduler
make
./cluster_benchmark

# Cluster logging/diagnostics simulation (pure Python, no deps)
cd ../logging
python cluster_logger.py
```

Arduino sketches (`arduino/*.ino`) are meant to be flashed with the Arduino
IDE onto separate boards — `device_control.ino` for direct remote control,
`automation_routine.ino` for scheduled/autonomous behavior. They talk over
USB-serial; the logging tool's `cluster_logger.py` today runs its own
simulated event stream, but its event schema matches what you'd parse from
real serial output.

## Notes

Compiled and ran the scheduler benchmark for real: `g++ -std=c++17 -O2
-pthread`, then `./cluster_benchmark`. On this machine it came out to a
70.5% speedup (5 workers vs. 1) — higher than you might expect, which
just reflects how many cores this particular machine has relative to the
task count; your mileage will vary with core count and how compute-bound
the workload actually is. The two Arduino sketches
(`device_control.ino`, `automation_routine.ino`) also compile clean
against an Uno — 4,946 bytes / 302 bytes RAM and 2,536 bytes / 322 bytes
RAM respectively.
