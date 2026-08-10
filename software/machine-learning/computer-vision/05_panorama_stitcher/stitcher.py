"""Two-image panorama stitching: ORB features, ratio-test matching, RANSAC homography."""

import cv2
import numpy as np


def find_matches(img1_gray, img2_gray, ratio_thresh=0.75, n_features=2000):
    orb = cv2.ORB_create(nfeatures=n_features)
    kp1, des1 = orb.detectAndCompute(img1_gray, None)
    kp2, des2 = orb.detectAndCompute(img2_gray, None)

    matcher = cv2.BFMatcher(cv2.NORM_HAMMING)
    raw_matches = matcher.knnMatch(des1, des2, k=2)

    good_matches = []
    for pair in raw_matches:
        if len(pair) == 2:
            m, n = pair
            if m.distance < ratio_thresh * n.distance:
                good_matches.append(m)

    return kp1, kp2, good_matches


def estimate_homography(kp1, kp2, matches, ransac_thresh=5.0):
    if len(matches) < 4:
        raise ValueError(f"Need at least 4 matches to estimate a homography, got {len(matches)}")

    src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

    H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, ransac_thresh)
    return H, mask


def stitch(img1, img2, H):
    """Warps img1 into img2's frame and composites onto a shared canvas."""
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]

    corners1 = np.float32([[0, 0], [0, h1], [w1, h1], [w1, 0]]).reshape(-1, 1, 2)
    warped_corners = cv2.perspectiveTransform(corners1, H)
    all_corners = np.concatenate((warped_corners, np.float32([[0, 0], [0, h2], [w2, h2], [w2, 0]]).reshape(-1, 1, 2)))

    x_min, y_min = np.floor(all_corners.min(axis=0).ravel()).astype(int)
    x_max, y_max = np.ceil(all_corners.max(axis=0).ravel()).astype(int)

    translation = np.array([[1, 0, -x_min], [0, 1, -y_min], [0, 0, 1]], dtype=np.float64)
    canvas_size = (x_max - x_min, y_max - y_min)

    result = cv2.warpPerspective(img1, translation @ H, canvas_size)
    result[-y_min:-y_min + h2, -x_min:-x_min + w2] = img2

    return result
