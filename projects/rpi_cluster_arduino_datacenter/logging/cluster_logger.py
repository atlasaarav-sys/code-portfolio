"""Simulates a cluster run (5 Pi nodes + 6 Arduino devices), logs every
task/communication event, and produces a diagnostic report.

Event schema matches what you'd parse from real serial output
(device_control.ino / automation_routine.ino print similar lines) or from
a Pi node's task scheduler logs — this tool's job is turning a stream of
raw events into "what failed, how often, and how fast did we notice."
"""

import random
import time
from dataclasses import dataclass, field


@dataclass
class Event:
    t: float
    device: str
    kind: str  # "task_dispatch", "task_complete", "comm_failure", "heartbeat"
    detail: str = ""


@dataclass
class ClusterRun:
    events: list = field(default_factory=list)

    def log(self, t, device, kind, detail=""):
        self.events.append(Event(t, device, kind, detail))


def simulate_run(seed=7, duration_s=60.0, failure_rate=0.05):
    random.seed(seed)
    run = ClusterRun()

    nodes = [f"pi-node-{i}" for i in range(1, 6)]
    devices = [f"arduino-{i}" for i in range(1, 7)]

    t = 0.0
    task_id = 0
    while t < duration_s:
        node = random.choice(nodes)
        device = random.choice(devices)

        run.log(t, node, "task_dispatch", detail=f"task-{task_id} -> {device}")

        if random.random() < failure_rate:
            # Communication failure: dispatched but never acknowledged for a while.
            detect_delay = random.uniform(0.5, 4.0)
            run.log(t + detect_delay, device, "comm_failure",
                    detail=f"task-{task_id} timed out (no ack)")
        else:
            complete_delay = random.uniform(0.05, 1.5)
            run.log(t + complete_delay, device, "task_complete", detail=f"task-{task_id}")

        task_id += 1
        t += random.uniform(0.2, 1.5)

    run.events.sort(key=lambda e: e.t)
    return run


def diagnostic_report(run: ClusterRun) -> str:
    lines = ["=== Cluster Diagnostic Report ==="]

    total_tasks = sum(1 for e in run.events if e.kind == "task_dispatch")
    completed = sum(1 for e in run.events if e.kind == "task_complete")
    failed = sum(1 for e in run.events if e.kind == "comm_failure")

    lines.append(f"Total tasks dispatched: {total_tasks}")
    lines.append(f"Completed: {completed} ({completed / total_tasks * 100:.1f}%)")
    lines.append(f"Communication failures: {failed} ({failed / total_tasks * 100:.1f}%)")
    lines.append("")

    failures_by_device = {}
    for e in run.events:
        if e.kind == "comm_failure":
            failures_by_device[e.device] = failures_by_device.get(e.device, 0) + 1

    if failures_by_device:
        lines.append("Failures by device:")
        for device, count in sorted(failures_by_device.items(), key=lambda kv: -kv[1]):
            lines.append(f"  {device}: {count}")
    else:
        lines.append("No communication failures recorded.")

    return "\n".join(lines)


def main():
    start = time.perf_counter()
    run = simulate_run()
    report = diagnostic_report(run)
    elapsed_ms = (time.perf_counter() - start) * 1000

    print(report)
    print(f"\nDiagnostic pass over {len(run.events)} events completed in {elapsed_ms:.2f} ms "
          f"(vs. manually scanning a raw serial log, which is the point of this tool).")


if __name__ == "__main__":
    main()
