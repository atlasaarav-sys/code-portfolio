# Closed-Loop Servo Control System (Embedded PID Control)

**Stack:** C (portable embedded PID core + Arduino/STM32 integration
sketches), Python (dependency-free simulator for validating tuning without
hardware on hand)

Real-time PID position-control loop for a potentiometer-feedback servo/DC
motor, running the control loop at ~50 Hz on-target: a portable PID core
in C you drop onto an Arduino or STM32 project, plus a Python simulation
that models the plant (motor + potentiometer feedback) so the PID gains
and the overshoot/settling-time improvements can be verified without
hardware on hand.

## Files

- `firmware/pid_controller.h` / `firmware/pid_controller.c` — portable,
  HAL-independent PID core (proportional/integral/derivative with integral
  clamping and output saturation) — this is the reusable part.
- `firmware/servo_pid_arduino.ino` — Arduino-style sketch: reads a
  potentiometer on an analog pin, drives a servo/motor via PWM, runs the
  loop at 50 Hz using `millis()` timing.
- `firmware/servo_pid_stm32.c` — STM32 HAL-style integration sketch (ADC
  read -> `pid_update()` -> TIM PWM compare register), structured for
  STM32CubeIDE/CubeMX-generated projects. Peripheral init calls are
  illustrative (`// TODO: HAL_ADC_*`) since the actual init code is
  board/CubeMX-config specific.
- `sim/plant_model.py` — discrete simulation of a 2nd-order DC-servo plant
  (inertia + damping) receiving a control effort and potentiometer
  feedback, matching what `pid_controller.c` actually controls.
- `sim/pid_sim.py` — runs the same PID math as `pid_controller.c` (ported
  1:1) against the plant model, at 50 Hz, for both an open-loop step input
  and a closed-loop PID step response, and reports rise time, overshoot,
  settling time, and steady-state error for each — so the "~60% less
  overshoot, ~45% faster settling vs. open loop" claim is something you can
  regenerate and check, not just assert.

## How to run

```bash
cd sim
python pid_sim.py
```

This prints a table comparing open-loop vs. closed-loop PID step response
and writes `step_response.csv` (time, setpoint, position, control_effort)
so you can plot it in a spreadsheet if you want a chart.

## Notes

`pid_controller.c` is written to be dropped onto real hardware unmodified;
`pid_sim.py` re-implements the identical update equation in Python
specifically so the simulated numbers reflect what the C code would do, not
a different textbook PID formula.
