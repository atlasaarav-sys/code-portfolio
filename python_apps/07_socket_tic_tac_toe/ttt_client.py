"""Minimal scriptable client for the tic-tac-toe server."""

import socket


class TicTacToeClient:
    def __init__(self, host, port, timeout=5.0):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(timeout)
        self.sock.connect((host, port))
        self.reader = self.sock.makefile("r", encoding="utf-8")

    def read_line(self) -> str:
        return self.reader.readline().rstrip("\n")

    def move(self, position: int) -> str:
        self.sock.sendall(f"MOVE {position}\n".encode("utf-8"))
        return self.read_line()

    def close(self):
        self.sock.close()
