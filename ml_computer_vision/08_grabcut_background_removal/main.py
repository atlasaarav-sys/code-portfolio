import cv2
import numpy as np

from background_removal import remove_background


def make_test_image(size=250, seed=2):
    rng = np.random.default_rng(seed)

    # Textured background (so GrabCut has real color-distribution work to do).
    background = rng.integers(150, 180, (size, size, 3), dtype=np.uint8)
    noise = rng.integers(-15, 15, (size, size, 3))
    background = np.clip(background.astype(int) + noise, 0, 255).astype(np.uint8)

    img = background.copy()
    cy, cx, r = size // 2, size // 2, 60
    yy, xx = np.meshgrid(np.arange(size), np.arange(size), indexing="ij")
    circle_mask = (yy - cy) ** 2 + (xx - cx) ** 2 <= r ** 2
    img[circle_mask] = [40, 40, 220]  # distinct subject color (BGR: strong red)

    return img, circle_mask


def main():
    img, true_mask = make_test_image()
    cv2.imwrite("test_image.png", img)

    # Rough rect around the circle (doesn't need to be exact -- that's the point of GrabCut).
    rect = (100 - 70, 125 - 70, 140, 140)  # (x, y, w, h)

    rgba, alpha_mask = remove_background(img, rect)
    cv2.imwrite("foreground_output.png", rgba)

    predicted_fg = alpha_mask > 0

    # Overlap between predicted foreground and the known true circle.
    intersection = np.logical_and(predicted_fg, true_mask).sum()
    true_area = true_mask.sum()
    predicted_area = predicted_fg.sum()

    recall = intersection / true_area  # fraction of true circle correctly marked foreground
    precision = intersection / predicted_area if predicted_area > 0 else 0

    print(f"True circle area: {true_area} px")
    print(f"Predicted foreground area: {predicted_area} px")
    print(f"Recall (true circle correctly segmented): {recall:.3f}")
    print(f"Precision (predicted foreground that's actually the circle): {precision:.3f}")

    assert recall > 0.85, f"expected most of the true circle to be segmented as foreground, got recall={recall:.3f}"
    assert precision > 0.85, f"expected segmentation to not over-include background, got precision={precision:.3f}"
    print("\nSegmentation matches known ground-truth shape within tolerance.")


if __name__ == "__main__":
    main()
