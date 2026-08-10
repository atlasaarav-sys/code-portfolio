"""Canny-style edge detection built from scratch with numpy."""

import numpy as np


def gaussian_kernel(size: int = 5, sigma: float = 1.4) -> np.ndarray:
    ax = np.arange(-size // 2 + 1, size // 2 + 1)
    xx, yy = np.meshgrid(ax, ax)
    kernel = np.exp(-(xx**2 + yy**2) / (2.0 * sigma**2))
    return kernel / kernel.sum()


def convolve2d(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    kh, kw = kernel.shape
    pad_h, pad_w = kh // 2, kw // 2
    padded = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode="edge")
    out = np.zeros_like(image, dtype=np.float64)

    flipped = np.flipud(np.fliplr(kernel))  # true convolution, not correlation
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            region = padded[i:i + kh, j:j + kw]
            out[i, j] = np.sum(region * flipped)
    return out


def gaussian_blur(image: np.ndarray, size: int = 5, sigma: float = 1.4) -> np.ndarray:
    return convolve2d(image, gaussian_kernel(size, sigma))


def sobel_gradients(image: np.ndarray):
    sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float64)
    sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float64)

    gx = convolve2d(image, sobel_x)
    gy = convolve2d(image, sobel_y)

    magnitude = np.hypot(gx, gy)
    direction = np.arctan2(gy, gx)
    return magnitude, direction


def non_max_suppression(magnitude: np.ndarray, direction: np.ndarray) -> np.ndarray:
    h, w = magnitude.shape
    result = np.zeros((h, w), dtype=np.float64)
    angle = np.rad2deg(direction) % 180

    for i in range(1, h - 1):
        for j in range(1, w - 1):
            a = angle[i, j]
            # Quantize direction to one of 4 sectors and compare against
            # the two neighbors along the gradient direction.
            if a < 22.5 or a >= 157.5:
                neighbors = (magnitude[i, j - 1], magnitude[i, j + 1])
            elif a < 67.5:
                neighbors = (magnitude[i - 1, j + 1], magnitude[i + 1, j - 1])
            elif a < 112.5:
                neighbors = (magnitude[i - 1, j], magnitude[i + 1, j])
            else:
                neighbors = (magnitude[i - 1, j - 1], magnitude[i + 1, j + 1])

            if magnitude[i, j] >= max(neighbors):
                result[i, j] = magnitude[i, j]
    return result


def hysteresis_threshold(image: np.ndarray, low_ratio: float = 0.05, high_ratio: float = 0.15) -> np.ndarray:
    high_thresh = image.max() * high_ratio
    low_thresh = high_thresh * low_ratio / high_ratio if high_ratio else 0
    low_thresh = image.max() * low_ratio

    strong = image >= high_thresh
    weak = (image >= low_thresh) & ~strong

    result = np.zeros_like(image, dtype=np.uint8)
    result[strong] = 255

    h, w = image.shape
    changed = True
    weak_coords = set(zip(*np.where(weak)))
    strong_coords = set(zip(*np.where(strong)))

    # Iteratively promote weak edges connected (8-neighborhood) to a strong edge.
    while changed:
        changed = False
        newly_strong = set()
        for (i, j) in weak_coords:
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    ni, nj = i + di, j + dj
                    if 0 <= ni < h and 0 <= nj < w and (ni, nj) in strong_coords:
                        newly_strong.add((i, j))
                        break
                if (i, j) in newly_strong:
                    break
        if newly_strong:
            changed = True
            for coord in newly_strong:
                result[coord] = 255
                strong_coords.add(coord)
            weak_coords -= newly_strong

    return result


def canny_edge_detect(image: np.ndarray, blur_size: int = 5, sigma: float = 1.4,
                       low_ratio: float = 0.05, high_ratio: float = 0.15) -> np.ndarray:
    blurred = gaussian_blur(image.astype(np.float64), blur_size, sigma)
    magnitude, direction = sobel_gradients(blurred)
    thinned = non_max_suppression(magnitude, direction)
    edges = hysteresis_threshold(thinned, low_ratio, high_ratio)
    return edges
