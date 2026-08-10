"""Sparse Lucas-Kanade optical flow tracking."""

import cv2
import numpy as np

FEATURE_PARAMS = dict(maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)
LK_PARAMS = dict(
    winSize=(15, 15),
    maxLevel=2,
    criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03),
)


def detect_features(gray_frame, feature_params=FEATURE_PARAMS):
    return cv2.goodFeaturesToTrack(gray_frame, mask=None, **feature_params)


def track_points(prev_gray, next_gray, prev_points, lk_params=LK_PARAMS):
    next_points, status, error = cv2.calcOpticalFlowPyrLK(prev_gray, next_gray, prev_points, None, **lk_params)
    good_prev = prev_points[status.flatten() == 1]
    good_next = next_points[status.flatten() == 1]
    return good_prev, good_next


def track_video(cap: cv2.VideoCapture, max_frames: int = None):
    """Runs LK tracking across a whole video, yielding (frame, prev_pts, next_pts) per step."""
    ret, prev_frame = cap.read()
    if not ret:
        return
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    prev_points = detect_features(prev_gray)

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret or (max_frames and frame_count >= max_frames):
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if prev_points is None or len(prev_points) < 10:
            prev_points = detect_features(gray)
            prev_gray = gray
            continue

        good_prev, good_next = track_points(prev_gray, gray, prev_points)
        yield frame, good_prev, good_next

        prev_gray = gray
        prev_points = good_next.reshape(-1, 1, 2)
        frame_count += 1
