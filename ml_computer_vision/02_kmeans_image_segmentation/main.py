import numpy as np
from PIL import Image

from generate_test_image import make_test_image
from segment_image import segment


def main():
    img, true_colors = make_test_image()
    Image.fromarray(img).save("test_image.png")

    segmented, centroids, iterations = segment(img, k=3)
    Image.fromarray(segmented).save("segmented_output.png")

    print(f"Converged in {iterations} iterations.")
    print("Recovered centroid colors (RGB):")
    for c in centroids:
        print(f"  {c.astype(int)}")

    true_color_array = np.array(list(true_colors.values()), dtype=np.float64)
    for centroid in centroids:
        dists = np.linalg.norm(true_color_array - centroid, axis=1)
        closest = dists.min()
        assert closest < 15, f"centroid {centroid} not close to any true color (min dist {closest:.1f})"

    print("\nAll recovered centroids matched a known true color within tolerance.")


if __name__ == "__main__":
    main()
