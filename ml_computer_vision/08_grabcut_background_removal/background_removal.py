"""Foreground extraction via OpenCV's GrabCut."""

import cv2
import numpy as np


def remove_background(image_bgr, rect, iter_count=5):
    """rect = (x, y, w, h) rough bounding box around the foreground subject."""
    mask = np.zeros(image_bgr.shape[:2], dtype=np.uint8)
    bgd_model = np.zeros((1, 65), dtype=np.float64)
    fgd_model = np.zeros((1, 65), dtype=np.float64)

    cv2.grabCut(image_bgr, mask, rect, bgd_model, fgd_model, iter_count, cv2.GC_INIT_WITH_RECT)

    # GC_BGD=0, GC_FGD=1, GC_PR_BGD=2, GC_PR_FGD=3 -- treat both "probable"
    # and "definite" foreground as foreground for the alpha mask.
    binary_mask = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 255, 0).astype(np.uint8)

    b, g, r = cv2.split(image_bgr)
    rgba = cv2.merge([b, g, r, binary_mask])
    return rgba, binary_mask
