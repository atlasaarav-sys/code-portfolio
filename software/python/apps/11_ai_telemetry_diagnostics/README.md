# AI-Assisted Telemetry Diagnostics Tool

**Stack:** Python (stdlib for the core pipeline, optional Anthropic API for
LLM summaries)

Ingests CAN-bus / sensor telemetry logs from a bench-test session, runs
statistical anomaly detection per signal, and produces a plain-language
diagnostic summary — either via an LLM (if `ANTHROPIC_API_KEY` is set) or a
deterministic rule-based fallback so the tool works with zero external
dependencies.

## Why this exists

Bench-test sessions produce large CSV logs (10,000+ rows at up to 50 Hz
across multiple CAN/sensor channels). Manually scanning that data for a
subsystem fault takes a while. This tool automates the first pass: flag
anything statistically out of range, then hand a human (or an LLM) a short,
readable summary instead of a raw CSV.

## Pipeline stages

1. **Ingest** (`telemetry_pipeline.py`) — parse a CSV log into per-signal
   time series, using only `csv` + stdlib (no pandas dependency required).
2. **Detect** (`anomaly_detector.py`) — rolling z-score + static threshold
   detector per signal; flags points beyond a configurable sigma
   (default 3.0) or outside an explicit min/max band, and reports
   out-of-range streaks (a real fault, not one noisy sample) as
   higher-severity events.
3. **Summarize** (`llm_summarizer.py`) — turns the anomaly list + per-signal
   stats into a plain-language report. Uses the Anthropic API if
   `ANTHROPIC_API_KEY` is set and `anthropic` is installed; otherwise falls
   back to a template-based summary so the tool is always usable offline.

## Files

- `generate_sample_data.py` — synthesizes a realistic bench-test CSV
  (speed, battery_voltage, battery_current, motor_temp_c, motor_rpm) at
  50 Hz with a few injected faults, so the pipeline has something to run on
- `telemetry_pipeline.py` — CSV ingestion + per-signal stats
- `anomaly_detector.py` — z-score/threshold/streak anomaly detection
- `llm_summarizer.py` — plain-language summary generation (LLM or fallback)
- `main.py` — CLI entry point wiring the three stages together
- `tests/test_anomaly_detector.py` — unit tests for the detector

## How to run

```bash
python generate_sample_data.py --rows 12000 --hz 50 --out sample_data.csv
python main.py sample_data.csv
```

To use the LLM summarizer instead of the rule-based fallback:

```bash
export ANTHROPIC_API_KEY=sk-...
pip install anthropic
python main.py sample_data.csv --llm
```

Run tests:

```bash
python -m unittest tests/test_anomaly_detector.py
```

## Notes

Signal thresholds (`SIGNAL_SPECS` in `anomaly_detector.py`) are
illustrative defaults for a solar-vehicle-style telemetry set, not tuned
against real hardware data — swap them for your own sensor ranges.
