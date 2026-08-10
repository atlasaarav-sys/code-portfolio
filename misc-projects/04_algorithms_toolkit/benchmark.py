"""Empirically measures sort runtime growth against input size."""

import random
import time

from algorithms.sorting import quicksort, mergesort, heapsort

ALGORITHMS = {"quicksort": quicksort, "mergesort": mergesort, "heapsort": heapsort}
SIZES = [1000, 2000, 4000, 8000, 16000]


def time_sort(algorithm, data):
    start = time.perf_counter()
    algorithm(data)
    return time.perf_counter() - start


def main():
    rng = random.Random(42)

    print(f"{'Algorithm':<12}{'n':>8}{'time (s)':>12}{'ratio vs prev':>16}")
    for name, algorithm in ALGORITHMS.items():
        prev_time = None
        for n in SIZES:
            data = rng.sample(range(n * 10), n)
            elapsed = time_sort(algorithm, data)
            ratio_str = f"{elapsed / prev_time:.2f}" if prev_time else "-"
            print(f"{name:<12}{n:>8}{elapsed:>12.4f}{ratio_str:>16}")
            prev_time = elapsed
        print()

    print("For an O(n log n) algorithm, doubling n should roughly double the\n"
          "time (ratio ~2.0-2.3, since log grows slowly) -- not ~2x per doubling\n"
          "squared (~4x, which would indicate O(n^2) instead).")


if __name__ == "__main__":
    main()
