# K-Means Image Segmentation

**Stack:** Python 3, `numpy`, `Pillow`

Color-based image segmentation via k-means clustering implemented from
scratch (Lloyd's algorithm: assign each pixel to its nearest of K cluster
centroids in RGB space, recompute centroids, repeat until convergence),
then recolors each pixel with its cluster's centroid color to produce a
posterized/segmented image.

## Files

- `kmeans.py` — `kmeans_fit(pixels, k)`: from-scratch Lloyd's algorithm
  with k-means++ initialization (spreads initial centroids apart instead
  of picking randomly, which avoids a common failure mode: two initial
  centroids landing on the same color and never separating)
- `segment_image.py` — loads an image, reshapes to a pixel list, runs
  k-means, recolors, saves the result
- `generate_test_image.py` — synthesizes a 3-color test image
- `main.py` — runs segmentation on the synthetic image with k=3 and
  verifies the recovered cluster colors match the three known input colors

## How to run

```bash
python main.py
```

## What was actually tested here

Ran k-means (k=3, k-means++ init) against a synthesized image with three
exact, well-separated fill colors plus a little Gaussian noise. Verified:
- exactly 3 clusters converge (no empty clusters)
- each recovered centroid color is within a small tolerance of one of the
  three known true colors
- print output shows the actual recovered centroid RGB values and
  iteration count to convergence from the real run

## Notes

k-means++ initialization matters here — plain random initialization on a
3-color image has a real chance of putting two centroids in the same
color region, and Lloyd's algorithm has no mechanism to split a cluster
back apart once that happens (it's a local-minimum-prone algorithm, hence
the smarter init).
