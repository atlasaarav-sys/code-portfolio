# Haar Cascade Face Detection

**Stack:** Python 3, OpenCV (`cv2`)

Classic Viola-Jones face detection via OpenCV's pretrained Haar cascade —
not a from-scratch reimplementation (Haar cascades are a whole
training pipeline of their own), but a correct, working detection script:
load the cascade, convert to grayscale, run
`detectMultiScale` with tuned `scaleFactor`/`minNeighbors`, draw boxes,
and (optionally) run on a live webcam feed.

## Files

- `face_detector.py` — `detect_faces(image, cascade)` wrapper +
  `draw_detections` for visualization
- `webcam_demo.py` — live webcam loop (`cv2.VideoCapture(0)`), draws boxes
  in real time, `q` to quit — the "real" way to use this
- `haarcascade_frontalface_default.xml` — OpenCV's pretrained frontal-face
  cascade (BSD-licensed, from the
  [opencv/opencv](https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml)
  `data/haarcascades/` directory — `opencv-python-headless` doesn't bundle
  cascade files the way the full `opencv-python` package does, so this is
  vendored locally)
- `main.py` — runs detection against a static test image and reports
  detection count/boxes

## How to run

```bash
python webcam_demo.py          # live webcam
python main.py your_photo.jpg  # static image
```

## Test results

`main.py` was run against a synthetic (no real face) test image to verify
the pipeline executes end-to-end without error and correctly reports zero
detections on an image with no face-like pattern — that's a real,
meaningful test of the *code path*, but not a test of detection accuracy,
which requires an actual photo of a face (Haar cascades need real facial
structure, not synthetic shapes). Point it at a real photo to see it
actually detect a face.
