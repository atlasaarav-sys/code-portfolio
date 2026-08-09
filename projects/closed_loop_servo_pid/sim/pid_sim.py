"""Simulate open-loop vs. closed-loop PID step response on the same plant,
at the 50 Hz loop rate the firmware runs at, and report rise time,
overshoot, settling time, and steady-state error for each.
"""

import csv

from pid_controller import PIDController
from plant_model import DCServoPlant

HZ = 50.0
DT = 1.0 / HZ
SIM_SECONDS = 4.0
SETPOINT_DEG = 90.0
EFFORT_MAX = 255.0

# Same gains as firmware/servo_pid_arduino.ino and servo_pid_stm32.c
KP, KI, KD = 4.0, 0.5, 0.15


def closed_loop_response():
    plant = DCServoPlant()
    pid = PIDController(KP, KI, KD, -EFFORT_MAX, EFFORT_MAX)
    positions, times = [], []

    steps = int(SIM_SECONDS / DT)
    for i in range(steps):
        t = i * DT
        effort = pid.update(SETPOINT_DEG, plant.position, DT)
        plant.step(effort, DT)
        positions.append(plant.position)
        times.append(t)

    return times, positions


def open_loop_response():
    """No feedback: apply full effort toward the target, cut power at an
    estimated (uncorrected) time-to-target, then coast. Models what happens
    if you command a motor without ever reading the position sensor.
    """
    plant = DCServoPlant()
    positions, times = [], []

    # Estimate steady-state velocity at full effort (theta_ddot = 0):
    # 0 = Kt*u - B*v_ss  =>  v_ss = Kt*u / B
    v_ss = (plant.Kt * EFFORT_MAX) / plant.B
    # Naive time estimate ignoring acceleration ramp-up.
    t_cutoff = SETPOINT_DEG / v_ss

    steps = int(SIM_SECONDS / DT)
    for i in range(steps):
        t = i * DT
        effort = EFFORT_MAX if t < t_cutoff else 0.0
        plant.step(effort, DT)
        positions.append(plant.position)
        times.append(t)

    return times, positions


def compute_metrics(times, positions, setpoint):
    final = positions[-1]
    peak = max(positions)
    overshoot_pct = max(0.0, (peak - setpoint) / setpoint * 100.0)

    # Rise time: time to first reach 90% of setpoint.
    rise_time = None
    for t, p in zip(times, positions):
        if p >= 0.9 * setpoint:
            rise_time = t
            break

    # Settling time: first time after which the response stays within +-2%
    # of setpoint for the remainder of the simulation.
    band = 0.02 * setpoint
    settling_time = times[-1]
    for i in range(len(positions) - 1, -1, -1):
        if abs(positions[i] - setpoint) > band:
            settling_time = times[min(i + 1, len(times) - 1)]
            break
    else:
        settling_time = 0.0

    steady_state_error = abs(setpoint - final)

    return {
        "rise_time_s": rise_time,
        "overshoot_pct": overshoot_pct,
        "settling_time_s": settling_time,
        "steady_state_error_deg": steady_state_error,
        "final_position_deg": final,
    }


def main():
    ol_times, ol_positions = open_loop_response()
    cl_times, cl_positions = closed_loop_response()

    ol_metrics = compute_metrics(ol_times, ol_positions, SETPOINT_DEG)
    cl_metrics = compute_metrics(cl_times, cl_positions, SETPOINT_DEG)

    print(f"Setpoint: {SETPOINT_DEG} deg, loop rate: {HZ} Hz\n")
    print(f"{'Metric':<26}{'Open-loop':>14}{'Closed-loop PID':>18}")
    for key, label in [
        ("rise_time_s", "Rise time (s)"),
        ("overshoot_pct", "Overshoot (%)"),
        ("settling_time_s", "Settling time (s)"),
        ("steady_state_error_deg", "Steady-state error (deg)"),
    ]:
        ol_val = ol_metrics[key]
        cl_val = cl_metrics[key]
        ol_str = f"{ol_val:.3f}" if ol_val is not None else "n/a"
        cl_str = f"{cl_val:.3f}" if cl_val is not None else "n/a"
        print(f"{label:<26}{ol_str:>14}{cl_str:>18}")

    if ol_metrics["overshoot_pct"] > 0:
        overshoot_reduction = (
            (ol_metrics["overshoot_pct"] - cl_metrics["overshoot_pct"])
            / ol_metrics["overshoot_pct"] * 100.0
        )
        print(f"\nOvershoot reduction vs. open-loop: {overshoot_reduction:.1f}%")
    settling_reduction = (
        (ol_metrics["settling_time_s"] - cl_metrics["settling_time_s"])
        / ol_metrics["settling_time_s"] * 100.0
    )
    print(f"Settling time reduction vs. open-loop: {settling_reduction:.1f}%")

    with open("step_response.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["t", "open_loop_position_deg", "closed_loop_position_deg", "setpoint_deg"])
        for t, ol, cl in zip(ol_times, ol_positions, cl_positions):
            writer.writerow([round(t, 3), round(ol, 3), round(cl, 3), SETPOINT_DEG])
    print("\nWrote step_response.csv")


if __name__ == "__main__":
    main()
