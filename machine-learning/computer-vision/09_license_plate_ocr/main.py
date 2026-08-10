import cv2
import numpy as np

from plate_localizer import find_plate_candidates, crop_box


def make_test_image(size=300, seed=3):
    rng = np.random.default_rng(seed)
    img = rng.integers(100, 140, (size, size, 3), dtype=np.uint8)  # textured "road/car" background

    # A plate-shaped rectangle (~3:1 aspect ratio, matches real plates) in a distinct color.
    plate_w, plate_h = 120, 40
    px, py = size // 2 - plate_w // 2, size // 2 - plate_h // 2
    cv2.rectangle(img, (px, py), (px + plate_w, py + plate_h), (230, 230, 230), -1)
    cv2.rectangle(img, (px, py), (px + plate_w, py + plate_h), (20, 20, 20), 2)

    # Dark marks to simulate characters (gives Canny/contours real edges to find inside the plate too).
    for i in range(6):
        x = px + 10 + i * 17
        cv2.rectangle(img, (x, py + 8), (x + 10, py + 32), (30, 30, 30), -1)

    return img, (px, py, plate_w, plate_h)


def iou(box_a, box_b):
    ax, ay, aw, ah = box_a
    bx, by, bw, bh = box_b
    ix1, iy1 = max(ax, bx), max(ay, by)
    ix2, iy2 = min(ax + aw, bx + bw), min(ay + ah, by + bh)
    inter = max(0, ix2 - ix1) * max(0, iy2 - iy1)
    union = aw * ah + bw * bh - inter
    return inter / union if union > 0 else 0


def main():
    img, true_box = make_test_image()
    cv2.imwrite("test_image.png", img)

    candidates = find_plate_candidates(img)
    print(f"Found {len(candidates)} plate-shaped candidates")

    assert candidates, "expected at least one candidate region"
    best = candidates[0]
    print(f"Top candidate box: {best['box']}  rectangularity={best['rectangularity']:.3f}")
    print(f"True plate box:    {true_box}")

    overlap = iou(best["box"], true_box)
    print(f"IoU with true plate location: {overlap:.3f}")
    assert overlap > 0.85, f"top candidate should closely match the known plate location, got IoU={overlap:.3f}"
    print("Localization matches known ground-truth location.")

    cropped = crop_box(img, best["box"])
    cv2.imwrite("plate_crop.png", cropped)

    try:
        from plate_ocr import read_plate_text
        text = read_plate_text(cropped)
        print(f"\nOCR result: '{text}'")
    except ImportError:
        print("\nOCR skipped: pytesseract is not installed in this environment "
              "(see README.md -- localization above is the tested part).")


if __name__ == "__main__":
    main()
