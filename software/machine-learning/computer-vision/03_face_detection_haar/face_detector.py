"""Haar cascade face detection wrapper."""

from pathlib import Path

import cv2

CASCADE_PATH = Path(__file__).parent / "haarcascade_frontalface_default.xml"


def load_cascade(path=CASCADE_PATH) -> cv2.CascadeClassifier:
    cascade = cv2.CascadeClassifier(str(path))
    if cascade.empty():
        raise RuntimeError(f"Failed to load cascade from {path}")
    return cascade


def detect_faces(image_bgr, cascade: cv2.CascadeClassifier,
                  scale_factor: float = 1.1, min_neighbors: int = 5, min_size=(30, 30)):
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)  # improves detection under uneven lighting
    faces = cascade.detectMultiScale(
        gray, scaleFactor=scale_factor, minNeighbors=min_neighbors, minSize=min_size
    )
    return faces  # array of (x, y, w, h)


def draw_detections(image_bgr, faces):
    output = image_bgr.copy()
    for (x, y, w, h) in faces:
        cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return output
