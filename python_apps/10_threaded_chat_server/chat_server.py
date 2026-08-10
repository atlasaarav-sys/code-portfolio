"""Multi-client TCP chat server: one thread per connection, shared broadcast."""

import argparse
import socket
import threading


class ChatRoom:
    def __init__(self):
        self.clients: dict[socket.socket, str] = {}  # conn -> nickname
        self.lock = threading.Lock()

    def join(self, conn, default_name):
        with self.lock:
            self.clients[conn] = default_name
        self.broadcast(f"* {default_name} joined the room", exclude=conn)

    def leave(self, conn):
        with self.lock:
            name = self.clients.pop(conn, None)
        if name:
            self.broadcast(f"* {name} left the room", exclude=None)

    def set_nick(self, conn, new_name):
        with self.lock:
            old_name = self.clients.get(conn, "?")
            self.clients[conn] = new_name
        self.broadcast(f"* {old_name} is now known as {new_name}", exclude=None)

    def say(self, conn, message):
        with self.lock:
            name = self.clients.get(conn, "?")
        self.broadcast(f"{name}: {message}", exclude=conn)

    def broadcast(self, message, exclude):
        with self.lock:
            targets = [c for c in self.clients if c is not exclude]
        for target in targets:
            try:
                target.sendall((message + "\n").encode("utf-8"))
            except OSError:
                pass


def handle_client(conn, addr, room: ChatRoom):
    default_name = f"user{addr[1]}"
    room.join(conn, default_name)

    try:
        with conn.makefile("r", encoding="utf-8") as reader:
            for line in reader:
                line = line.strip()
                if not line:
                    continue
                if line.startswith("/nick "):
                    room.set_nick(conn, line[len("/nick "):].strip())
                elif line == "/quit":
                    break
                else:
                    room.say(conn, line)
    except (ConnectionError, OSError):
        pass  # client disconnected without a clean /quit
    finally:
        room.leave(conn)
        conn.close()


def start_server(host="localhost", port=9092):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"Chat server listening on {host}:{server_socket.getsockname()[1]}")
    return server_socket


def serve_forever(server_socket, room: ChatRoom = None):
    room = room or ChatRoom()
    while True:
        try:
            conn, addr = server_socket.accept()
        except OSError:
            break
        threading.Thread(target=handle_client, args=(conn, addr, room), daemon=True).start()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=9092)
    args = parser.parse_args()

    server_socket = start_server(args.host, args.port)
    try:
        serve_forever(server_socket)
    except KeyboardInterrupt:
        server_socket.close()


if __name__ == "__main__":
    main()
