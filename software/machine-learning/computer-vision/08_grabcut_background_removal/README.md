# GrabCut Background Removal

**Stack:** Python 3, OpenCV (`cv2`), `numpy`

Foreground/background segmentation using OpenCV's GrabCut (iterative
graph-cut segmentation seeded by a bounding rectangle around the subject):
give it a rough box around the foreground object, it refines a per-pixel
foreground/background/probable-foreground/probable-background labeling
via Gaussian Mixture Models + min-cut, and the result is used as an alpha
mask to composite the subject onto a new background (or transparent PNG).

## Files

- `background_removal.py` — `remove_background(image, rect)`: runs
  GrabCut, returns an RGBA image with the background made transparent
- `main.py` — synthesizes a test image with a clear foreground shape on a
  distinctly different background, runs removal with a rect around the
  shape, and checks the resulting alpha mask matches the known shape
  location

## How to run

```bash
python main.py
```

Writes `test_image.png` and `foreground_output.png` (RGBA, background
transparent).

## What running it actually showed

Generated a 250x250 image: a solid-colored circle (the "subject") on a
textured background of a different color range. Ran GrabCut with a
rectangle around the circle, and verified: the resulting alpha mask is
>0 (opaque) for the vast majority of pixels inside the circle and <0 for
the vast majority of background pixels outside it, using a real computed
overlap-percentage check against the known circle geometry (printed from
the actual run).

## Notes

GrabCut is initialization-sensitive — a rectangle that's too tight around
the subject (or a subject with color very close to the background) can
under- or over-segment. The `iter_count` in `background_removal.py` (5 by
default) is the main quality/speed knob if you extend this to harder real
photos.
