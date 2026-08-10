"""K-means clustering from scratch (Lloyd's algorithm + k-means++ init)."""

import numpy as np


def kmeans_plus_plus_init(points: np.ndarray, k: int, rng: np.random.Generator) -> np.ndarray:
    n = points.shape[0]
    centroids = [points[rng.integers(n)]]

    for _ in range(1, k):
        dists = np.min(
            [np.sum((points - c) ** 2, axis=1) for c in centroids], axis=0
        )
        probs = dists / dists.sum()
        next_idx = rng.choice(n, p=probs)
        centroids.append(points[next_idx])

    return np.array(centroids, dtype=np.float64)


def kmeans_fit(points: np.ndarray, k: int, max_iters: int = 100, tol: float = 1e-4, seed: int = 42):
    rng = np.random.default_rng(seed)
    points = points.astype(np.float64)
    centroids = kmeans_plus_plus_init(points, k, rng)

    for iteration in range(max_iters):
        dists = np.linalg.norm(points[:, None, :] - centroids[None, :, :], axis=2)
        labels = np.argmin(dists, axis=1)

        new_centroids = np.zeros_like(centroids)
        for i in range(k):
            cluster_points = points[labels == i]
            if len(cluster_points) > 0:
                new_centroids[i] = cluster_points.mean(axis=0)
            else:
                new_centroids[i] = centroids[i]  # keep empty clusters in place

        shift = np.linalg.norm(new_centroids - centroids)
        centroids = new_centroids
        if shift < tol:
            return centroids, labels, iteration + 1

    return centroids, labels, max_iters
