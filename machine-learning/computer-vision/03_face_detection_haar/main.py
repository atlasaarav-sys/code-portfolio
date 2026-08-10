import sys

import cv2
import numpy as np

from face_detector import load_cascade, detect_faces, draw_detections


def make_synthetic_test_image(size=300):
    """No real face -- just verifies the pipeline runs cleanly end-to-end
    and correctly reports zero detections on non-face content."""
    rng = np.random.default_rng(0)
    img = np.full((size, size, 3), 200, dtype=np.uint8)
    img += rng.integers(-10, 10, img.shape, dtype=np.int16).astype(np.uint8)
    cv2.rectangle(img, (50, 50), (150, 150), (100, 100, 100), -1)
    return img


def main():
    cascade = load_cascade()

    if len(sys.argv) > 1:
        image = cv2.imread(sys.argv[1])
        if image is None:
            raise RuntimeError(f"Could not read image: {sys.argv[1]}")
        source = sys.argv[1]
    else:
        image = make_synthetic_test_image()
        source = "synthetic test image (no real face)"

    faces = detect_faces(image, cascade)
    output = draw_detections(image, faces)
    cv2.imwrite("detections_output.png", output)

    print(f"Source: {source}")
    print(f"Faces detected: {len(faces)}")
    for (x, y, w, h) in faces:
        print(f"  box: x={x} y={y} w={w} h={h}")
    print("Saved annotated image to detections_output.png")


if __name__ == "__main__":
    main()
