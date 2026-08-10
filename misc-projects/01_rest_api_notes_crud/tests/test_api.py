import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app import create_app


class TestNotesApi(unittest.TestCase):
    def setUp(self):
        self.app = create_app(db_path=":memory:")
        self.client = self.app.test_client()

    def test_full_crud_lifecycle(self):
        # Create
        resp = self.client.post("/notes", json={"title": "Buy milk", "body": "2%"})
        self.assertEqual(resp.status_code, 201)
        note = resp.get_json()
        note_id = note["id"]
        self.assertEqual(note["title"], "Buy milk")

        # Read (single)
        resp = self.client.get(f"/notes/{note_id}")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["body"], "2%")

        # Read (list)
        resp = self.client.get("/notes")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.get_json()), 1)

        # Update
        resp = self.client.put(f"/notes/{note_id}", json={"title": "Buy milk", "body": "whole milk"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["body"], "whole milk")

        # Delete
        resp = self.client.delete(f"/notes/{note_id}")
        self.assertEqual(resp.status_code, 204)

        resp = self.client.get(f"/notes/{note_id}")
        self.assertEqual(resp.status_code, 404)

    def test_create_without_title_returns_400(self):
        resp = self.client.post("/notes", json={"body": "no title here"})
        self.assertEqual(resp.status_code, 400)

    def test_get_nonexistent_note_returns_404(self):
        resp = self.client.get("/notes/999")
        self.assertEqual(resp.status_code, 404)

    def test_update_nonexistent_note_returns_404(self):
        resp = self.client.put("/notes/999", json={"title": "x", "body": "y"})
        self.assertEqual(resp.status_code, 404)

    def test_search_filters_by_title(self):
        self.client.post("/notes", json={"title": "groceries", "body": ""})
        self.client.post("/notes", json={"title": "taxes", "body": ""})

        resp = self.client.get("/notes?q=groc")
        results = resp.get_json()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "groceries")


if __name__ == "__main__":
    unittest.main()
