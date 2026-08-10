import threading
import time
import unittest

from kv_server import run_server, serve_forever
from kv_client import KVClient


class TestKVServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server_socket, cls.store, _ = run_server(port=0)
        cls.port = cls.server_socket.getsockname()[1]
        cls.thread = threading.Thread(target=serve_forever, args=(cls.server_socket, cls.store), daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server_socket.close()

    def client(self):
        return KVClient("localhost", self.port)

    def test_set_and_get(self):
        c = self.client()
        c.set("foo", "bar")
        self.assertEqual(c.get("foo"), "bar")
        c.close()

    def test_get_missing_key(self):
        c = self.client()
        self.assertIsNone(c.get("does_not_exist"))
        c.close()

    def test_delete(self):
        c = self.client()
        c.set("temp", "1")
        self.assertTrue(c.delete("temp"))
        self.assertIsNone(c.get("temp"))
        self.assertFalse(c.delete("temp"))  # already gone
        c.close()

    def test_expire(self):
        c = self.client()
        c.set("short_lived", "value")
        self.assertTrue(c.expire("short_lived", 0.2))
        self.assertEqual(c.get("short_lived"), "value")  # not expired yet
        time.sleep(0.4)
        self.assertIsNone(c.get("short_lived"))  # expired now
        c.close()

    def test_keys(self):
        c = self.client()
        c.set("a", "1")
        c.set("b", "2")
        keys = set(c.keys())
        self.assertIn("a", keys)
        self.assertIn("b", keys)
        c.close()


if __name__ == "__main__":
    unittest.main()
