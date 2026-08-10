"""OCR on a cropped plate image via pytesseract + Tesseract.

Not installed/tested in this environment -- see README.md.
"""

import cv2


def read_plate_text(cropped_plate_bgr) -> str:
    import pytesseract  # imported here so plate_localizer.py stays usable without pytesseract installed

    gray = cv2.cvtColor(cropped_plate_bgr, cv2.COLOR_BGR2GRAY)
    # Upscale small crops -- Tesseract accuracy drops sharply below ~20px character height.
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Restrict to uppercase letters/digits, matching real plate character sets;
    # --psm 7 tells Tesseract to expect a single line of text.
    config = "--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    text = pytesseract.image_to_string(thresh, config=config)
    return text.strip()
