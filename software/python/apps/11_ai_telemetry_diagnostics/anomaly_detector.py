"""Rolling z-score + threshold-band anomaly detection for telemetry signals."""

import statistics
from dataclasses import dataclass

from telemetry_pipeline import SignalSeries

# Illustrative min/max operating bands for a solar-vehicle-style telemetry
# set. Values outside the band are flagged regardless of z-score.
SIGNAL_SPECS = {
    "speed_mph": {"min": 0, "max": 65},
    "battery_voltage": {"min": 40, "max": 58},
    "battery_current": {"min": -5, "max": 25},
    "motor_temp_c": {"min": -10, "max": 80},
    "motor_rpm": {"min": 0, "max": 4000},
}


@dataclass
class Anomaly:
    signal: str
    start_t: float
    end_t: float
    num_points: int
    peak_value: float
    reason: str
    severity: str  # "warning" or "critical"


def _zscore_flags(series: SignalSeries, sigma: float) -> list[bool]:
    if len(series.values) < 2:
        return [False] * len(series.values)
    mean = statistics.fmean(series.values)
    stdev = statistics.pstdev(series.values)
    if stdev == 0:
        return [False] * len(series.values)
    return [abs(v - mean) > sigma * stdev for v in series.values]


def _band_flags(series: SignalSeries) -> list[bool]:
    spec = SIGNAL_SPECS.get(series.name)
    if not spec:
        return [False] * len(series.values)
    return [v < spec["min"] or v > spec["max"] for v in series.values]


def _group_streaks(flags: list[bool], timestamps: list[float], values: list[float],
                    signal_name: str, min_streak: int, reason: str) -> list[Anomaly]:
    anomalies = []
    i = 0
    n = len(flags)
    while i < n:
        if flags[i]:
            j = i
            while j < n and flags[j]:
                j += 1
            streak_len = j - i
            if streak_len >= min_streak:
                window_values = values[i:j]
                severity = "critical" if streak_len >= min_streak * 3 else "warning"
                anomalies.append(Anomaly(
                    signal=signal_name,
                    start_t=timestamps[i],
                    end_t=timestamps[j - 1],
                    num_points=streak_len,
                    peak_value=max(window_values, key=lambda v: abs(v)),
                    reason=reason,
                    severity=severity,
                ))
            i = j
        else:
            i += 1
    return anomalies


def detect_anomalies(series_map: dict[str, SignalSeries], sigma: float = 3.0,
                      min_streak: int = 3) -> list[Anomaly]:
    """Detect anomalies across all signals.

    A single noisy sample is ignored; only streaks of >= min_streak
    consecutive out-of-band samples are reported as anomalies (this models
    "a real subsystem fault" vs. one noisy reading).
    """
    all_anomalies: list[Anomaly] = []

    for name, series in series_map.items():
        if not series.values:
            continue
        z_flags = _zscore_flags(series, sigma)
        band_flags = _band_flags(series)
        combined = [z or b for z, b in zip(z_flags, band_flags)]
        all_anomalies.extend(
            _group_streaks(combined, series.timestamps, series.values, name,
                            min_streak, reason="out-of-band / statistical outlier")
        )

    all_anomalies.sort(key=lambda a: a.start_t)
    return all_anomalies
