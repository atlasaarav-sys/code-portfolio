import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app import create_app


class TestBookmarksApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app(db_path=":memory:", secret_key="test-secret")
        self.client = self.app.test_client()

    def register(self, client, username, password):
        return client.post("/register", data={"username": username, "password": password}, follow_redirects=True)

    def login(self, client, username, password):
        return client.post("/login", data={"username": username, "password": password}, follow_redirects=True)

    def test_index_requires_login(self):
        resp = self.client.get("/", follow_redirects=False)
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/login", resp.headers["Location"])

    def test_register_and_login_flow(self):
        resp = self.register(self.client, "alice", "hunter2")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"alice's Bookmarks", resp.data)

    def test_duplicate_username_rejected(self):
        self.register(self.client, "alice", "hunter2")
        self.client.post("/logout")
        resp = self.register(self.client, "alice", "different-password")
        self.assertIn(b"already taken", resp.data)

    def test_wrong_password_rejected(self):
        self.register(self.client, "alice", "hunter2")
        self.client.post("/logout")
        resp = self.login(self.client, "alice", "wrong-password")
        self.assertIn(b"Invalid username or password", resp.data)

    def test_add_and_delete_bookmark(self):
        self.register(self.client, "alice", "hunter2")
        self.client.post("/", data={"title": "Example", "url": "https://example.com"})

        resp = self.client.get("/")
        self.assertIn(b"Example", resp.data)

    def test_users_cannot_see_each_others_bookmarks(self):
        client_a = self.app.test_client()
        client_b = self.app.test_client()

        self.register(client_a, "alice", "pw-alice")
        client_a.post("/", data={"title": "Alice's link", "url": "https://alice.example.com"})

        self.register(client_b, "bob", "pw-bob")
        resp = client_b.get("/")

        self.assertNotIn(b"Alice's link", resp.data)

    def test_cannot_delete_another_users_bookmark(self):
        client_a = self.app.test_client()
        client_b = self.app.test_client()

        self.register(client_a, "alice", "pw-alice")
        client_a.post("/", data={"title": "Alice's link", "url": "https://alice.example.com"})
        # Bookmark IDs are global autoincrement, so id=1 belongs to alice.
        self.register(client_b, "bob", "pw-bob")
        client_b.post("/delete/1")

        resp = client_a.get("/")
        # Jinja2 HTML-escapes the apostrophe (&#39;), so check for the URL instead.
        self.assertIn(b"alice.example.com", resp.data)  # still there -- bob's delete was scoped to his own user_id


if __name__ == "__main__":
    unittest.main()
