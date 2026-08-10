"""CSV ingestion for bench-test telemetry logs, using only the stdlib."""

import csv
import statistics
from dataclasses import dataclass, field


@dataclass
class SignalSeries:
    name: str
    timestamps: list = field(default_factory=list)
    values: list = field(default_factory=list)

    def stats(self):
        if not self.values:
            return {"count": 0}
        return {
            "count": len(self.values),
            "mean": statistics.fmean(self.values),
            "stdev": statistics.pstdev(self.values) if len(self.values) > 1 else 0.0,
            "min": min(self.values),
            "max": max(self.values),
        }


def load_telemetry(path: str) -> dict[str, SignalSeries]:
    """Load a telemetry CSV into a dict of signal name -> SignalSeries.

    Expects a 't' (timestamp) column plus one column per signal.
    """
    series: dict[str, SignalSeries] = {}

    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError(f"{path} appears to be empty")
        signal_names = [c for c in reader.fieldnames if c != "t"]
        for name in signal_names:
            series[name] = SignalSeries(name=name)

        for row in reader:
            t = float(row["t"])
            for name in signal_names:
                raw = row[name]
                if raw == "":
                    continue
                series[name].timestamps.append(t)
                series[name].values.append(float(raw))

    return series
