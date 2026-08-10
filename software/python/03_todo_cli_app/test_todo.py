"""Unit tests for the todo app's storage layer."""

import unittest
from pathlib import Path

from storage import Task, load_tasks, save_tasks, next_id

TEST_PATH = Path(__file__).parent / "test_tasks.json"


class TestStorage(unittest.TestCase):
    def tearDown(self):
        if TEST_PATH.exists():
            TEST_PATH.unlink()

    def test_save_and_load_round_trip(self):
        tasks = [Task(id=1, title="Test task", priority="high", done=False)]
        save_tasks(tasks, TEST_PATH)
        loaded = load_tasks(TEST_PATH)
        self.assertEqual(loaded, tasks)

    def test_load_missing_file_returns_empty(self):
        self.assertEqual(load_tasks(TEST_PATH), [])

    def test_next_id_empty(self):
        self.assertEqual(next_id([]), 1)

    def test_next_id_increments(self):
        tasks = [Task(id=1, title="a"), Task(id=5, title="b")]
        self.assertEqual(next_id(tasks), 6)


if __name__ == "__main__":
    unittest.main()
