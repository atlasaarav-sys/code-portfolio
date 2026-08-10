import tempfile
import unittest
from pathlib import Path

from dedup import find_duplicates


class TestDedup(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)

    def tearDown(self):
        self.tmpdir.cleanup()

    def write(self, name, content):
        path = self.root / name
        path.write_text(content)
        return path

    def test_no_duplicates(self):
        self.write("a.txt", "hello")
        self.write("b.txt", "world")
        self.assertEqual(find_duplicates(self.root), {})

    def test_finds_exact_duplicates(self):
        self.write("a.txt", "same content")
        self.write("b.txt", "same content")
        self.write("c.txt", "different")

        duplicates = find_duplicates(self.root)
        self.assertEqual(len(duplicates), 1)
        group = list(duplicates.values())[0]
        self.assertEqual(len(group), 2)

    def test_same_size_different_content_not_flagged(self):
        # Same length but different content -- must not be flagged as duplicates
        # (this is exactly why the size pre-filter can't be the only check).
        self.write("a.txt", "aaaa")
        self.write("b.txt", "bbbb")
        self.assertEqual(find_duplicates(self.root), {})

    def test_three_way_duplicate_group(self):
        self.write("a.txt", "triplicate")
        self.write("b.txt", "triplicate")
        self.write("c.txt", "triplicate")

        duplicates = find_duplicates(self.root)
        self.assertEqual(len(duplicates), 1)
        self.assertEqual(len(list(duplicates.values())[0]), 3)


if __name__ == "__main__":
    unittest.main()
