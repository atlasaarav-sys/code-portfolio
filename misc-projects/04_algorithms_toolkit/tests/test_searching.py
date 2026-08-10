import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from algorithms.searching import binary_search, find_first, find_last


class TestSearching(unittest.TestCase):
    def test_binary_search_found_and_not_found(self):
        items = [1, 3, 5, 7, 9, 11]
        self.assertEqual(items[binary_search(items, 7)], 7)
        self.assertEqual(binary_search(items, 4), -1)

    def test_binary_search_empty_list(self):
        self.assertEqual(binary_search([], 5), -1)

    def test_find_first_and_last_with_duplicates(self):
        items = [1, 2, 2, 2, 3, 4, 4, 5]
        self.assertEqual(find_first(items, 2), 1)
        self.assertEqual(find_last(items, 2), 3)
        self.assertEqual(find_first(items, 4), 5)
        self.assertEqual(find_last(items, 4), 6)

    def test_find_first_last_not_found(self):
        items = [1, 2, 3]
        self.assertEqual(find_first(items, 99), -1)
        self.assertEqual(find_last(items, 99), -1)

    def test_single_element(self):
        self.assertEqual(find_first([5], 5), 0)
        self.assertEqual(find_last([5], 5), 0)


if __name__ == "__main__":
    unittest.main()
