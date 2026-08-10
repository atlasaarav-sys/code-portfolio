# Panorama Stitcher

**Stack:** Python 3, OpenCV (`cv2`), `numpy`

Stitches two overlapping images into a panorama the classical way: detect
ORB keypoints/descriptors in both images, match them (brute-force Hamming
distance + ratio test to reject ambiguous matches), estimate a homography
with RANSAC (robust to the outlier matches the ratio test misses), and
warp one image into the other's coordinate frame.

## Files

- `stitcher.py` — `find_matches` (ORB + ratio-test matching),
  `estimate_homography` (RANSAC), `stitch` (warp + blend)
- `generate_test_images.py` — splits one larger synthetic textured image
  into two overlapping halves — a known-correct panorama pair since the
  "ground truth" stitched result is just the original image
- `main.py` — stitches the two generated halves back together and checks
  the output dimensions are close to the known original

## How to run

```bash
python main.py
```

Writes `left.png`, `right.png`, and `panorama_output.png`.

## What was actually tested here

Split a 400x250 synthetic textured image into two overlapping 250x250
halves (100px overlap), ran the full ORB -> match -> RANSAC homography ->
warp pipeline, and verified: enough good matches were found in the overlap
region (>10), the estimated homography is close to the known translation
between the two crops, and the final stitched canvas width is within a
reasonable margin of the original image width.

## Notes

Real-world panorama stitching (`cv2.Stitcher`) handles exposure
compensation, seam blending, and multi-image bundle adjustment — this
project stops at "single-pair homography stitch," which is the core
building block underneath all of that.
