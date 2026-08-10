"""Minimal client for the line-based KV store protocol."""

import socket


class KVClient:
    def __init__(self, host, port, timeout=5.0):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(timeout)
        self.sock.connect((host, port))
        self.reader = self.sock.makefile("r", encoding="utf-8")

    def _send(self, line: str) -> str:
        self.sock.sendall((line + "\n").encode("utf-8"))
        return self.reader.readline().rstrip("\n")

    def set(self, key, value):
        return self._send(f"SET {key} {value}")

    def get(self, key):
        result = self._send(f"GET {key}")
        return None if result == "(nil)" else result

    def delete(self, key):
        return self._send(f"DEL {key}") == "1"

    def expire(self, key, seconds):
        return self._send(f"EXPIRE {key} {seconds}") == "OK"

    def keys(self):
        result = self._send("KEYS")
        return result.split() if result else []

    def close(self):
        self.sock.close()
