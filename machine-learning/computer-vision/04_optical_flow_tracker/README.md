# Optical Flow Tracker (Lucas-Kanade)

**Stack:** Python 3, OpenCV (`cv2`), `numpy`

Sparse optical flow point tracking: detect good-to-track corner features
(`cv2.goodFeaturesToTrack`, Shi-Tomasi) in a frame, then track them into
the next frame with pyramidal Lucas-Kanade (`cv2.calcOpticalFlowPyrLK`) —
the same building block behind most classical (non-deep-learning) video
object tracking.

## Files

- `flow_tracker.py` — `detect_features`, `track_points` (one LK step),
  `track_video` (runs LK across a whole video, drawing motion trails)
- `main.py` — synthesizes two frames with a known, exact pixel shift
  (simulating an object moving diagonally), tracks points between them,
  and checks the tracked displacement matches the known shift

## How to run

```bash
python main.py
```

For a real video: `flow_tracker.track_video(cv2.VideoCapture("video.mp4"))`.

## What was actually tested here

Generated two 300x300 synthetic frames: frame 1 has a textured patch at a
known location, frame 2 has the identical patch shifted by exactly
(+15, +10) pixels. Ran Shi-Tomasi corner detection on frame 1, tracked
those points into frame 2 with `calcOpticalFlowPyrLK`, and verified the
mean tracked displacement matches (+15, +10) within ~1 pixel — a real,
numerically-checked correctness test of the tracking math, not just "it
ran without crashing."
