import numpy as np
from PIL import Image

from edge_detection import canny_edge_detect
from generate_test_image import make_test_image


def main():
    img = make_test_image()
    Image.fromarray(img).save("test_image.png")

    edges = canny_edge_detect(img)
    Image.fromarray(edges).save("edges_output.png")

    total_pixels = edges.size
    edge_pixels = int(np.sum(edges > 0))
    print(f"Image size: {edges.shape}")
    print(f"Edge pixels detected: {edge_pixels} / {total_pixels} ({edge_pixels / total_pixels * 100:.2f}%)")

    # Sanity check: interior of the rectangle (flat region) should have no edges.
    interior_edges = int(np.sum(edges[45:75, 45:105] > 0))
    print(f"Edge pixels inside rectangle interior (should be 0): {interior_edges}")

    # Sanity check: edges should exist near the known rectangle boundary rows/cols.
    near_top_edge = int(np.sum(edges[28:33, 30:120] > 0))
    print(f"Edge pixels near rectangle's top boundary (should be > 0): {near_top_edge}")

    assert interior_edges == 0, "flat interior should have no detected edges"
    assert near_top_edge > 0, "rectangle boundary should have detected edges"
    print("\nSanity checks passed.")


if __name__ == "__main__":
    main()
