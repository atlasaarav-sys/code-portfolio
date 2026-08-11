# Edge Detection From Scratch

**Stack:** Python 3, `numpy`, `Pillow` (image I/O only — no `cv2` in the
detection logic itself)

Implements Sobel gradient edge detection and a simplified Canny pipeline
(Gaussian blur -> Sobel gradients -> non-maximum suppression -> double
threshold + hysteresis) entirely with numpy array operations — the point
is understanding what `cv2.Canny` actually does internally, not calling it.

## Files

- `edge_detection.py` — `gaussian_blur`, `sobel_gradients`, `non_max_suppression`,
  `hysteresis_threshold`, and `canny_edge_detect` (composes all four)
- `generate_test_image.py` — synthesizes a test image (shapes with clean
  edges) so the pipeline has something deterministic to run against
- `main.py` — runs the pipeline on the synthetic image, saves the edge map,
  and prints a sanity check (edges detected exactly at the known shape
  boundaries)

## How to run

```bash
python main.py
```

Writes `test_image.png` and `edges_output.png` to this directory.

## Verification

Ran the full pipeline against a synthesized 200x200 image containing a
filled rectangle and a filled circle on a flat background. Verified:
- edge pixels cluster tightly around the known rectangle/circle boundaries
  (within a few pixels, matching the expected blur-kernel spread)
- flat interior/background regions produce zero edge pixels
- pixel counts: see the printed sanity-check output for exact numbers from
  the run

## Notes

This is a real (if simplified) Canny implementation — Gaussian smoothing,
Sobel gradient magnitude/direction, thinning via non-max suppression along
the gradient direction, and hysteresis linking of weak edges to strong
ones. It's slower than `cv2.Canny` (pure Python loops in a few places
where vectorizing would obscure the algorithm) — not meant to replace it,
meant to show what it's doing.
