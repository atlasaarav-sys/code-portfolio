import cv2
import numpy as np

from flow_tracker import detect_features, track_points


def make_frame(size=300, shift=(0, 0), seed=0):
    rng = np.random.default_rng(seed)
    frame = np.zeros((size, size), dtype=np.uint8)
    # A textured patch (random noise block) gives Shi-Tomasi real corners to find,
    # unlike a flat-color shape which has no trackable texture.
    patch = rng.integers(0, 255, (80, 80), dtype=np.uint8)

    x0, y0 = 100 + shift[0], 100 + shift[1]
    frame[y0:y0 + 80, x0:x0 + 80] = patch
    return frame


def main():
    true_shift = (15, 10)  # (dx, dy)

    frame1 = make_frame(shift=(0, 0))
    frame2 = make_frame(shift=true_shift)

    points1 = detect_features(frame1)
    print(f"Detected {len(points1)} features in frame 1")

    good_prev, good_next = track_points(frame1, frame2, points1)
    print(f"Successfully tracked {len(good_next)} / {len(points1)} points into frame 2")

    displacement = good_next.reshape(-1, 2) - good_prev.reshape(-1, 2)
    mean_dx, mean_dy = displacement.mean(axis=0)
    print(f"Known shift: dx={true_shift[0]}, dy={true_shift[1]}")
    print(f"Mean tracked displacement: dx={mean_dx:.2f}, dy={mean_dy:.2f}")

    assert abs(mean_dx - true_shift[0]) < 1.0, "tracked dx doesn't match known shift"
    assert abs(mean_dy - true_shift[1]) < 1.0, "tracked dy doesn't match known shift"
    print("\nTracked displacement matches known shift within 1 pixel.")


if __name__ == "__main__":
    main()
