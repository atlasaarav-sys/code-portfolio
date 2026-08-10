"""Simulates a day of noisy light/temperature sensor data and runs the same
filter + threshold + hysteresis decision logic as firmware/energy_monitor.ino,
comparing it against a naive instant-threshold comparator to quantify the
false-trigger reduction and estimated energy savings.
"""

import csv
import math
import random

FILTER_WINDOW = 8
LIGHT_BRIGHT_THRESHOLD = 2800.0
LIGHT_HYSTERESIS = 200.0
TEMP_HIGH_THRESHOLD_C = 27.0
TEMP_HYSTERESIS_C = 1.0

SAMPLE_HZ = 20.0
SIM_HOURS = 24


def generate_day(seed=11):
    """One simulated day: light follows a daylight curve, temp follows a
    daily cycle, both with sensor noise layered on top."""
    random.seed(seed)
    num_samples = int(SIM_HOURS * 3600 * SAMPLE_HZ)
    # Downsample for a fast demo: 1 simulated sample per simulated minute
    # instead of literally 20 Hz for 24 hours (1.7M points) — same shape,
    # far less runtime, still exercises the identical decision logic.
    num_samples = SIM_HOURS * 60

    data = []
    for i in range(num_samples):
        hour = (i / 60.0) % 24
        # Daylight curve: bright mid-day, dark at night.
        daylight = max(0.0, math.sin((hour - 6) / 12 * math.pi)) * 3500
        light = daylight + random.uniform(-150, 150)
        light = max(0.0, light)

        # Temp curve: warmest mid-afternoon.
        temp = 22 + 6 * max(0.0, math.sin((hour - 8) / 14 * math.pi)) + random.uniform(-0.8, 0.8)

        data.append((i, light, temp))
    return data


def moving_average(buf):
    return sum(buf) / len(buf)


def decide_inefficient_usage(light_avg, temp_avg, currently_on):
    if currently_on:
        too_bright = light_avg > LIGHT_BRIGHT_THRESHOLD
        too_warm = temp_avg > TEMP_HIGH_THRESHOLD_C
        return not (too_bright or too_warm)
    else:
        dim_enough = light_avg < (LIGHT_BRIGHT_THRESHOLD - LIGHT_HYSTERESIS)
        cool_enough = temp_avg < (TEMP_HIGH_THRESHOLD_C - TEMP_HYSTERESIS_C)
        return dim_enough and cool_enough


def run_filtered(data):
    light_buf, temp_buf = [], []
    relay_on = True
    trace = []
    toggles = 0

    for i, light, temp in data:
        light_buf.append(light)
        temp_buf.append(temp)
        if len(light_buf) > FILTER_WINDOW:
            light_buf.pop(0)
            temp_buf.pop(0)
        if len(light_buf) < FILTER_WINDOW:
            trace.append((i, light, temp, relay_on))
            continue

        light_avg = moving_average(light_buf)
        temp_avg = moving_average(temp_buf)
        new_state = decide_inefficient_usage(light_avg, temp_avg, relay_on)
        if new_state != relay_on:
            toggles += 1
        relay_on = new_state
        trace.append((i, light, temp, relay_on))

    return trace, toggles


def run_naive(data):
    """No filter, no hysteresis: instant threshold comparison on the raw
    (noisy) sample every tick."""
    relay_on = True
    toggles = 0
    trace = []

    for i, light, temp in data:
        too_bright = light > LIGHT_BRIGHT_THRESHOLD
        too_warm = temp > TEMP_HIGH_THRESHOLD_C
        new_state = not (too_bright or too_warm)
        if new_state != relay_on:
            toggles += 1
        relay_on = new_state
        trace.append((i, light, temp, relay_on))

    return trace, toggles


def estimate_savings(trace):
    """Minutes the relay was OFF (device not wastefully running) vs total."""
    off_minutes = sum(1 for _, _, _, on in trace if not on)
    return off_minutes / len(trace) * 100.0


def main():
    data = generate_day()

    naive_trace, naive_toggles = run_naive(data)
    filtered_trace, filtered_toggles = run_filtered(data)

    false_trigger_reduction = (naive_toggles - filtered_toggles) / naive_toggles * 100.0
    savings_pct = estimate_savings(filtered_trace)

    print(f"Simulated {SIM_HOURS}h day, {len(data)} samples (1/minute)\n")
    print(f"{'Metric':<32}{'Naive (unfiltered)':>20}{'Filtered + hysteresis':>24}")
    print(f"{'Relay state toggles':<32}{naive_toggles:>20}{filtered_toggles:>24}")
    print(f"\nFalse-trigger reduction from filtering: {false_trigger_reduction:.1f}%")
    print(f"Estimated energy savings (time relay held OFF): {savings_pct:.1f}%")

    with open("energy_trace.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["minute", "light", "temp_c", "relay_on"])
        for row in filtered_trace:
            writer.writerow(row)
    print("\nWrote energy_trace.csv")


if __name__ == "__main__":
    main()
