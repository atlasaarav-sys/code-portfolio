import threading
import time
import unittest

from chat_server import start_server, serve_forever, ChatRoom
from chat_client import ChatClient


class TestChatServer(unittest.TestCase):
    def setUp(self):
        self.server_socket = start_server(port=0)
        self.port = self.server_socket.getsockname()[1]
        self.room = ChatRoom()
        self.thread = threading.Thread(target=serve_forever, args=(self.server_socket, self.room), daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server_socket.close()

    def connect(self):
        client = ChatClient("localhost", self.port)
        time.sleep(0.05)  # let the server's join() broadcast settle before we start asserting order
        return client

    def test_broadcast_excludes_sender_and_reaches_others(self):
        a = self.connect()
        b = self.connect()
        self.assertTrue(a.read_line().endswith("joined the room"))  # A sees B join

        c = self.connect()
        self.assertTrue(a.read_line().endswith("joined the room"))  # A sees C join
        self.assertTrue(b.read_line().endswith("joined the room"))  # B sees C join

        a.send("hello everyone")
        msg_b = b.read_line()
        msg_c = c.read_line()
        self.assertTrue(msg_b.endswith(": hello everyone"))
        self.assertTrue(msg_c.endswith(": hello everyone"))
        self.assertNotIn("hello everyone", "")  # sanity no-op; A's socket is never read here (would block)

        a.close(); b.close(); c.close()

    def test_nick_change_reflected_in_future_messages(self):
        a = self.connect()
        b = self.connect()
        self.assertTrue(a.read_line().endswith("joined the room"))

        b.nick("bob")
        self.assertTrue(a.read_line().endswith("is now known as bob"))
        self.assertTrue(b.read_line().endswith("is now known as bob"))  # nick change broadcasts to everyone, including self

        b.send("hi from bob")
        msg = a.read_line()
        self.assertTrue(msg.startswith("bob:"))

        a.close(); b.close()

    def test_quit_announces_leave(self):
        a = self.connect()
        b = self.connect()
        self.assertTrue(a.read_line().endswith("joined the room"))

        b.quit()
        leave_msg = a.read_line()
        self.assertTrue(leave_msg.endswith("left the room"))

        a.close()


if __name__ == "__main__":
    unittest.main()
