import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from telemetry_pipeline import SignalSeries
from anomaly_detector import detect_anomalies


class TestAnomalyDetector(unittest.TestCase):
    def test_no_anomalies_on_flat_signal(self):
        series = SignalSeries(name="speed_mph", timestamps=list(range(20)), values=[20.0] * 20)
        anomalies = detect_anomalies({"speed_mph": series})
        self.assertEqual(anomalies, [])

    def test_detects_sustained_out_of_band_streak(self):
        values = [45.0] * 20 + [120.0] * 10 + [45.0] * 20  # motor_temp_c spikes above band
        timestamps = list(range(len(values)))
        series = SignalSeries(name="motor_temp_c", timestamps=timestamps, values=values)
        anomalies = detect_anomalies({"motor_temp_c": series}, min_streak=3)
        self.assertEqual(len(anomalies), 1)
        self.assertEqual(anomalies[0].signal, "motor_temp_c")
        self.assertEqual(anomalies[0].num_points, 10)

    def test_ignores_single_sample_noise(self):
        values = [45.0] * 20 + [46.0] + [45.0] * 20
        timestamps = list(range(len(values)))
        series = SignalSeries(name="motor_temp_c", timestamps=timestamps, values=values)
        anomalies = detect_anomalies({"motor_temp_c": series}, min_streak=3)
        self.assertEqual(anomalies, [])

    def test_empty_series_no_crash(self):
        series = SignalSeries(name="speed_mph", timestamps=[], values=[])
        anomalies = detect_anomalies({"speed_mph": series})
        self.assertEqual(anomalies, [])


if __name__ == "__main__":
    unittest.main()
