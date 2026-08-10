"""CLI entry point: ingest -> detect -> summarize."""

import argparse
import time

from telemetry_pipeline import load_telemetry
from anomaly_detector import detect_anomalies
from llm_summarizer import summarize_rule_based, summarize_with_llm


def main():
    parser = argparse.ArgumentParser(description="Telemetry diagnostics pipeline")
    parser.add_argument("csv_path", help="Path to a telemetry CSV log")
    parser.add_argument("--sigma", type=float, default=3.0, help="Z-score threshold")
    parser.add_argument("--min-streak", type=int, default=3,
                         help="Minimum consecutive out-of-band samples to count as an anomaly")
    parser.add_argument("--llm", action="store_true", help="Use the LLM summarizer instead of rule-based")
    args = parser.parse_args()

    start = time.perf_counter()
    series_map = load_telemetry(args.csv_path)
    anomalies = detect_anomalies(series_map, sigma=args.sigma, min_streak=args.min_streak)
    elapsed = time.perf_counter() - start

    if args.llm:
        summary = summarize_with_llm(series_map, anomalies)
    else:
        summary = summarize_rule_based(series_map, anomalies)

    print(summary)
    print(f"\n(Pipeline ran in {elapsed*1000:.1f} ms)")


if __name__ == "__main__":
    main()
