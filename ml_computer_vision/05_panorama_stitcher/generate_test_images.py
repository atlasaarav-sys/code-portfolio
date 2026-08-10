"""Splits a synthetic textured image into two overlapping halves."""

import numpy as np
import cv2


def make_textured_image(w=400, h=250, seed=1):
    rng = np.random.default_rng(seed)
    img = np.zeros((h, w, 3), dtype=np.uint8)

    # Random textured blobs give ORB real corners/features to detect,
    # unlike a flat gradient which is nearly featureless.
    for _ in range(60):
        cx, cy = rng.integers(0, w), rng.integers(0, h)
        radius = rng.integers(5, 20)
        color = tuple(int(c) for c in rng.integers(0, 255, 3))
        cv2.circle(img, (cx, cy), radius, color, -1)

    return img


def split_overlapping(img, overlap=100):
    h, w = img.shape[:2]
    mid = w // 2
    left = img[:, : mid + overlap // 2]
    right = img[:, mid - overlap // 2:]
    return left, right
