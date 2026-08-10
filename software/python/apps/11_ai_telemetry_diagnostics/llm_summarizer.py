"""Plain-language diagnostic summary generation.

Uses the Anthropic API if ANTHROPIC_API_KEY is set and the `anthropic`
package is installed; otherwise falls back to a deterministic, template
based summary so the tool works fully offline.
"""

import os

from anomaly_detector import Anomaly
from telemetry_pipeline import SignalSeries


def _format_anomalies_for_prompt(anomalies: list[Anomaly]) -> str:
    lines = []
    for a in anomalies:
        lines.append(
            f"- [{a.severity.upper()}] {a.signal}: {a.num_points} consecutive "
            f"samples out of range between t={a.start_t:.2f}s and t={a.end_t:.2f}s "
            f"(peak value {a.peak_value:.2f}), reason: {a.reason}"
        )
    return "\n".join(lines) if lines else "No anomalies detected."


def summarize_rule_based(series_map: dict[str, SignalSeries], anomalies: list[Anomaly]) -> str:
    """Deterministic fallback summary — no external API required."""
    lines = ["=== Telemetry Diagnostic Summary (rule-based) ==="]

    total_points = sum(s.stats().get("count", 0) for s in series_map.values())
    lines.append(f"Session: {len(series_map)} signals, {total_points} total samples logged.")
    lines.append("")

    if not anomalies:
        lines.append("No anomalies detected across any monitored signal — "
                      "all values stayed within statistical and operating bounds.")
        return "\n".join(lines)

    critical = [a for a in anomalies if a.severity == "critical"]
    warnings = [a for a in anomalies if a.severity == "warning"]
    lines.append(f"Found {len(anomalies)} anomaly event(s): "
                 f"{len(critical)} critical, {len(warnings)} warning.")
    lines.append("")

    by_signal: dict[str, list[Anomaly]] = {}
    for a in anomalies:
        by_signal.setdefault(a.signal, []).append(a)

    for signal, events in by_signal.items():
        stats = series_map[signal].stats()
        lines.append(f"Signal: {signal}")
        lines.append(
            f"  mean={stats['mean']:.2f}, stdev={stats['stdev']:.2f}, "
            f"range=[{stats['min']:.2f}, {stats['max']:.2f}]"
        )
        for a in events:
            lines.append(
                f"  -> [{a.severity.upper()}] {a.num_points} samples out of range "
                f"from t={a.start_t:.2f}s to t={a.end_t:.2f}s, peak={a.peak_value:.2f}. "
                f"Likely subsystem: {_guess_subsystem(signal)}."
            )
        lines.append("")

    return "\n".join(lines)


def _guess_subsystem(signal: str) -> str:
    mapping = {
        "motor_temp_c": "motor / thermal management",
        "battery_voltage": "battery pack / BMS / connector",
        "battery_current": "battery pack / power electronics",
        "motor_rpm": "motor controller",
        "speed_mph": "drivetrain / wheel speed sensor",
    }
    return mapping.get(signal, "unknown subsystem")


def summarize_with_llm(series_map: dict[str, SignalSeries], anomalies: list[Anomaly],
                        model: str = "claude-sonnet-5") -> str:
    """LLM-based summary. Requires ANTHROPIC_API_KEY and the `anthropic` package.

    Falls back to the rule-based summary if the API isn't available so the
    caller never has to special-case failures.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return summarize_rule_based(series_map, anomalies) + \
            "\n\n[Note: ANTHROPIC_API_KEY not set, used rule-based summary instead of LLM.]"

    try:
        import anthropic
    except ImportError:
        return summarize_rule_based(series_map, anomalies) + \
            "\n\n[Note: `anthropic` package not installed, used rule-based summary instead of LLM.]"

    stats_lines = []
    for name, series in series_map.items():
        s = series.stats()
        if s.get("count"):
            stats_lines.append(
                f"{name}: mean={s['mean']:.2f} stdev={s['stdev']:.2f} "
                f"min={s['min']:.2f} max={s['max']:.2f}"
            )

    prompt = (
        "You are a vehicle telemetry diagnostics assistant. Given per-signal "
        "statistics and a list of detected anomalies from a bench-test session, "
        "write a short, plain-language diagnostic summary for an engineer. "
        "Call out likely subsystem faults and suggested next checks. Keep it under "
        "200 words.\n\n"
        f"Per-signal stats:\n{chr(10).join(stats_lines)}\n\n"
        f"Detected anomalies:\n{_format_anomalies_for_prompt(anomalies)}"
    )

    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model=model,
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text
