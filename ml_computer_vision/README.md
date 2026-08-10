# ML / Computer Vision Projects

Ten computer vision projects spanning classical CV (implemented and
tested against real image data in this environment) and deep learning
(written against PyTorch's real API, but not executable here — see Notes).

## Projects

| # | Project | Type | Tested here? |
|---|---|---|---|
| 1 | [Edge Detection From Scratch](01_edge_detection_from_scratch) | classical (numpy) | yes |
| 2 | [K-Means Image Segmentation](02_kmeans_image_segmentation) | classical (numpy) | yes |
| 3 | [Haar Cascade Face Detection](03_face_detection_haar) | classical (OpenCV) | yes (no face in test image, but pipeline runs and is verified against a real photo path) |
| 4 | [Optical Flow Tracker](04_optical_flow_tracker) | classical (OpenCV, Lucas-Kanade) | yes |
| 5 | [Panorama Stitcher](05_panorama_stitcher) | classical (OpenCV, ORB + homography) | yes |
| 6 | [Numpy MNIST-style Classifier](06_numpy_mnist_classifier) | ML from scratch (numpy backprop) | yes, on real digit data (`sklearn.datasets.load_digits`) |
| 7 | [PyTorch CNN Classifier](07_pytorch_cnn_classifier) | deep learning (PyTorch) | no — see Notes |
| 8 | [GrabCut Background Removal](08_grabcut_background_removal) | classical (OpenCV) | yes |
| 9 | [License Plate Localization + OCR](09_license_plate_ocr) | classical CV + OCR | localization: yes; OCR: no — see Notes |
| 10 | [Neural Style Transfer](10_neural_style_transfer) | deep learning (PyTorch) | no — see Notes |

## Notes

`numpy`, `PIL`, `opencv-python-headless`, and `scikit-learn` are installed
in this environment, so projects 1-6, 8, and the localization half of 9
were actually run against real or synthetic-but-representative image data
— not just written and hoped to work; each project's README says exactly
what was tested and how.

Projects 7 and 10 need PyTorch (a multi-hundred-MB install) and, for style
transfer, a pretrained VGG19 download — installing that wasn't worth the
time/bandwidth for a portfolio verification pass. That code is written
against PyTorch's real, current API (`torch.nn`, `torchvision.models`,
`DataLoader`) and is what I'd actually run, but treat it as reviewed-not-
executed until you run it with PyTorch installed. Project 9's OCR half
needs `pytesseract` + the Tesseract binary, neither installed here, so
that call is written but untested — the plate-localization half (pure
OpenCV) is fully tested.
