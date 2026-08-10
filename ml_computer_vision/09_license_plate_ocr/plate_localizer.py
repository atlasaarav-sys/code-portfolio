"""Classical (non-deep-learning) license plate region localization."""

import cv2
import numpy as np


def find_plate_candidates(image_bgr, min_aspect=2.0, max_aspect=5.5, min_area=500):
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    blurred = cv2.bilateralFilter(gray, 11, 17, 17)  # smooths noise, keeps edges sharp
    edges = cv2.Canny(blurred, 30, 200)

    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    candidates = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if h == 0:
            continue
        aspect = w / h
        area = w * h
        if area < min_area or not (min_aspect <= aspect <= max_aspect):
            continue

        contour_area = cv2.contourArea(contour)
        rectangularity = contour_area / area if area > 0 else 0
        candidates.append({"box": (x, y, w, h), "rectangularity": rectangularity, "area": area})

    candidates.sort(key=lambda c: c["rectangularity"], reverse=True)
    return candidates


def crop_box(image, box):
    x, y, w, h = box
    return image[y:y + h, x:x + w]
