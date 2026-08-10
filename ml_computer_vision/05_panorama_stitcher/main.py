import cv2

from generate_test_images import make_textured_image, split_overlapping
from stitcher import find_matches, estimate_homography, stitch


def main():
    original = make_textured_image()
    left, right = split_overlapping(original, overlap=100)
    cv2.imwrite("left.png", left)
    cv2.imwrite("right.png", right)

    left_gray = cv2.cvtColor(left, cv2.COLOR_BGR2GRAY)
    right_gray = cv2.cvtColor(right, cv2.COLOR_BGR2GRAY)

    kp1, kp2, matches = find_matches(left_gray, right_gray)
    print(f"ORB keypoints: left={len(kp1)} right={len(kp2)}")
    print(f"Good matches after ratio test: {len(matches)}")
    assert len(matches) > 10, "expected a healthy number of matches in the overlap region"

    H, mask = estimate_homography(kp1, kp2, matches)
    inliers = int(mask.sum())
    print(f"RANSAC inliers: {inliers} / {len(matches)}")

    panorama = stitch(left, right, H)
    cv2.imwrite("panorama_output.png", panorama)

    print(f"\nOriginal image size: {original.shape[1]}x{original.shape[0]}")
    print(f"Left/right crop sizes: {left.shape[1]}x{left.shape[0]} / {right.shape[1]}x{right.shape[0]}")
    print(f"Stitched panorama size: {panorama.shape[1]}x{panorama.shape[0]}")

    # The stitched panorama should be close to the original image's width
    # (it was built by splitting that exact image with a known overlap).
    width_diff = abs(panorama.shape[1] - original.shape[1])
    print(f"Width difference from original: {width_diff}px")
    assert width_diff < 40, "stitched panorama width is unexpectedly far from the original"
    print("\nStitching pipeline validated against known ground-truth geometry.")


if __name__ == "__main__":
    main()
