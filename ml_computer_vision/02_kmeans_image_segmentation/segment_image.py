"""Loads/produces an image, runs k-means, recolors pixels by cluster."""

import numpy as np

from kmeans import kmeans_fit


def segment(image: np.ndarray, k: int, seed: int = 42):
    h, w, c = image.shape
    pixels = image.reshape(-1, c)

    centroids, labels, iterations = kmeans_fit(pixels, k, seed=seed)

    segmented_pixels = centroids[labels].astype(np.uint8)
    segmented_image = segmented_pixels.reshape(h, w, c)

    return segmented_image, centroids, iterations
