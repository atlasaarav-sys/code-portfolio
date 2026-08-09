"""Synthesize a bench-test telemetry CSV (CAN-bus style channels) with a
few injected faults, so the diagnostics pipeline has real data to run on.
"""

import argparse
import csv
import math
import random


def generate_rows(num_rows: int, hz: float):
    dt = 1.0 / hz
    t = 0.0

    # Injected fault windows (row index ranges) -> which signal, and how.
    faults = {
        "motor_temp_c": range(int(num_rows * 0.40), int(num_rows * 0.42)),
        "battery_voltage": range(int(num_rows * 0.75), int(num_rows * 0.755)),
    }

    for i in range(num_rows):
        speed = 20 + 5 * math.sin(i / 200.0) + random.uniform(-0.5, 0.5)
        battery_voltage = 48 + 0.5 * math.sin(i / 500.0) + random.uniform(-0.1, 0.1)
        battery_current = 8 + 2 * math.sin(i / 150.0) + random.uniform(-0.3, 0.3)
        motor_temp_c = 45 + 3 * math.sin(i / 300.0) + random.uniform(-0.5, 0.5)
        motor_rpm = 2000 + 150 * math.sin(i / 180.0) + random.uniform(-10, 10)

        if i in faults["motor_temp_c"]:
            motor_temp_c += 40  # overheating event
        if i in faults["battery_voltage"]:
            battery_voltage -= 12  # brownout / connector dropout

        yield {
            "t": round(t, 3),
            "speed_mph": round(speed, 2),
            "battery_voltage": round(battery_voltage, 2),
            "battery_current": round(battery_current, 2),
            "motor_temp_c": round(motor_temp_c, 2),
            "motor_rpm": round(motor_rpm, 1),
        }
        t += dt


def main():
    parser = argparse.ArgumentParser(description="Generate synthetic telemetry CSV")
    parser.add_argument("--rows", type=int, default=12000)
    parser.add_argument("--hz", type=float, default=50.0)
    parser.add_argument("--out", default="sample_data.csv")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    random.seed(args.seed)

    fieldnames = ["t", "speed_mph", "battery_voltage", "battery_current", "motor_temp_c", "motor_rpm"]
    with open(args.out, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in generate_rows(args.rows, args.hz):
            writer.writerow(row)

    print(f"Wrote {args.rows} rows at {args.hz} Hz to {args.out}")


if __name__ == "__main__":
    main()
