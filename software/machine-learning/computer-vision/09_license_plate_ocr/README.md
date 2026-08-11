# License Plate Localization + OCR

**Stack:** Python 3, OpenCV (`cv2`) for localization; `pytesseract` +
Tesseract OCR binary for text recognition

Two-stage pipeline: (1) **localization** — find the license-plate-shaped
region in an image using classical CV (grayscale -> edge detection ->
contour finding -> filter contours by aspect ratio and rectangularity,
the way plate localization worked before anyone used a CNN for it), then
(2) **OCR** — crop that region, threshold/clean it up, and run Tesseract
to read the characters.

## Files

- `plate_localizer.py` — `find_plate_candidates(image)`: edge detection +
  contour filtering by aspect ratio (~2:1 to ~5:1, matching real plate
  proportions) and minimum area, returns candidate bounding boxes ranked
  by "rectangularity" (contour area / bounding-box area)
- `plate_ocr.py` — `read_plate_text(cropped_plate_image)`: grayscale,
  adaptive threshold, then `pytesseract.image_to_string` with a
  character-whitelist config (alphanumeric only, matching real plates)
- `main.py` — synthesizes a test image with a plate-shaped rectangle (with
  text-like dark marks on it) on a textured background, runs localization,
  and checks the detected box matches the known plate location; OCR is
  called but the result isn't asserted on (see Notes)

## How to run

```bash
pip install pytesseract  # plus install the Tesseract binary separately
python main.py
```

## Testing notes

**Localization** (`plate_localizer.py`) was run against a synthesized test
image with a known plate-shaped rectangle (correct aspect ratio, distinct
from the background) — verified the top-ranked candidate's bounding box
overlaps the true plate location by >90% IoU, using OpenCV that's actually
installed and working here.

**OCR** (`plate_ocr.py`) was **not** run — `pytesseract` isn't installed
and the Tesseract binary isn't present in this environment. The call is
written against the real `pytesseract` API and is what I'd run, but
`main.py` catches the import error and skips that step with a printed
note rather than silently pretending it succeeded.
