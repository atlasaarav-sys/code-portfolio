"""Tiny Redis-like key-value store over a line-based TCP protocol."""

import argparse
import socket
import threading
import time


class KVStore:
    def __init__(self):
        self._data: dict[str, str] = {}
        self._expiry: dict[str, float] = {}
        self._lock = threading.Lock()

    def set(self, key, value):
        with self._lock:
            self._data[key] = value
            self._expiry.pop(key, None)

    def get(self, key):
        with self._lock:
            self._expire_if_needed(key)
            return self._data.get(key)

    def delete(self, key):
        with self._lock:
            existed = key in self._data
            self._data.pop(key, None)
            self._expiry.pop(key, None)
            return existed

    def expire(self, key, seconds):
        with self._lock:
            if key not in self._data:
                return False
            self._expiry[key] = time.time() + seconds
            return True

    def keys(self):
        with self._lock:
            now = time.time()
            return [k for k in self._data if self._expiry.get(k, now + 1) > now]

    def _expire_if_needed(self, key):
        exp = self._expiry.get(key)
        if exp is not None and exp <= time.time():
            self._data.pop(key, None)
            self._expiry.pop(key, None)

    def sweep_expired(self):
        with self._lock:
            now = time.time()
            expired = [k for k, exp in self._expiry.items() if exp <= now]
            for k in expired:
                self._data.pop(k, None)
                self._expiry.pop(k, None)


def handle_client(conn: socket.socket, store: KVStore):
    with conn, conn.makefile("r", encoding="utf-8") as reader:
        for line in reader:
            line = line.strip()
            if not line:
                continue
            parts = line.split(" ", 2)
            cmd = parts[0].upper()

            if cmd == "SET" and len(parts) == 3:
                store.set(parts[1], parts[2])
                response = "OK"
            elif cmd == "GET" and len(parts) == 2:
                value = store.get(parts[1])
                response = value if value is not None else "(nil)"
            elif cmd == "DEL" and len(parts) == 2:
                response = "1" if store.delete(parts[1]) else "0"
            elif cmd == "EXPIRE" and len(parts) == 3:
                ok = store.expire(parts[1], float(parts[2]))
                response = "OK" if ok else "(nil)"
            elif cmd == "KEYS":
                response = " ".join(store.keys())
            else:
                response = "ERR unknown command or wrong arg count"

            conn.sendall((response + "\n").encode("utf-8"))


def sweep_loop(store: KVStore, interval: float = 1.0, stop_event: threading.Event = None):
    while not (stop_event and stop_event.is_set()):
        store.sweep_expired()
        time.sleep(interval)


def run_server(host="localhost", port=9090):
    store = KVStore()
    stop_event = threading.Event()
    sweeper = threading.Thread(target=sweep_loop, args=(store, 1.0, stop_event), daemon=True)
    sweeper.start()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen()
    actual_port = server_socket.getsockname()[1]
    print(f"KV store listening on {host}:{actual_port}")

    return server_socket, store, stop_event


def serve_forever(server_socket, store):
    while True:
        try:
            conn, _ = server_socket.accept()
        except OSError:
            break
        threading.Thread(target=handle_client, args=(conn, store), daemon=True).start()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=9090)
    args = parser.parse_args()

    server_socket, store, _ = run_server(args.host, args.port)
    try:
        serve_forever(server_socket, store)
    except KeyboardInterrupt:
        server_socket.close()


if __name__ == "__main__":
    main()
