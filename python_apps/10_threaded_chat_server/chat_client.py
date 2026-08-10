"""Minimal scriptable chat client."""

import socket


class ChatClient:
    def __init__(self, host, port, timeout=5.0):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(timeout)
        self.sock.connect((host, port))
        self.reader = self.sock.makefile("r", encoding="utf-8")

    def read_line(self) -> str:
        return self.reader.readline().rstrip("\n")

    def send(self, message: str):
        self.sock.sendall((message + "\n").encode("utf-8"))

    def nick(self, name: str):
        self.send(f"/nick {name}")

    def quit(self):
        self.send("/quit")

    def close(self):
        self.sock.close()
