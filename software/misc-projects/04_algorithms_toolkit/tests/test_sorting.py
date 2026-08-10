import os
import random
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from algorithms.sorting import quicksort, mergesort, heapsort

ALGORITHMS = {"quicksort": quicksort, "mergesort": mergesort, "heapsort": heapsort}


class TestSorting(unittest.TestCase):
    def test_all_algorithms_against_builtin_sorted(self):
        cases = [
            [],
            [1],
            [3, 1, 2],
            [5, 4, 3, 2, 1],  # reverse-sorted
            [1, 2, 3, 4, 5],  # already sorted
            [2, 2, 2, 1, 1, 3],  # duplicates
            list(random.Random(0).sample(range(1000), 200)),
        ]
        for name, algorithm in ALGORITHMS.items():
            for case in cases:
                with self.subTest(algorithm=name, case=case[:5]):
                    self.assertEqual(algorithm(case), sorted(case))

    def test_does_not_mutate_input(self):
        original = [3, 1, 2]
        for algorithm in ALGORITHMS.values():
            copy = list(original)
            algorithm(copy)
            self.assertEqual(copy, original)


if __name__ == "__main__":
    unittest.main()
