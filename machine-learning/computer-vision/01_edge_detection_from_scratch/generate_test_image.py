"""Synthesizes a test image with known, clean-edged shapes."""

import numpy as np


def make_test_image(size: int = 200) -> np.ndarray:
    img = np.full((size, size), 30, dtype=np.uint8)  # dark background

    # Filled rectangle
    img[30:90, 30:120] = 220

    # Filled circle
    cy, cx, r = 140, 140, 40
    yy, xx = np.meshgrid(np.arange(size), np.arange(size), indexing="ij")
    circle_mask = (yy - cy) ** 2 + (xx - cx) ** 2 <= r ** 2
    img[circle_mask] = 200

    return img
