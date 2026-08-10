"""Synthesizes a 3-color test image with a little noise."""

import numpy as np


def make_test_image(size: int = 90, seed: int = 0) -> np.ndarray:
    rng = np.random.default_rng(seed)
    img = np.zeros((size, size, 3), dtype=np.float64)

    colors = {
        "red": (200, 30, 30),
        "green": (30, 180, 30),
        "blue": (30, 30, 200),
    }

    third = size // 3
    img[:, :third] = colors["red"]
    img[:, third:2 * third] = colors["green"]
    img[:, 2 * third:] = colors["blue"]

    noise = rng.normal(0, 5, img.shape)
    img = np.clip(img + noise, 0, 255)

    return img.astype(np.uint8), colors
