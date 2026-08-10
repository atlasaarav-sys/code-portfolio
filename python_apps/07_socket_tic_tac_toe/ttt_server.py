"""Two-player tic-tac-toe over TCP; server holds authoritative game state."""

import argparse
import socket
import threading

WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
    (0, 4, 8), (2, 4, 6),             # diagonals
]


class Game:
    def __init__(self, conn_x, conn_y):
        self.conns = {"X": conn_x, "O": conn_y}
        self.board = ["."] * 9
        self.turn = "X"
        self.lock = threading.Lock()
        self.over = False
        self._pending_result = None

    def winner(self):
        for a, b, c in WIN_LINES:
            if self.board[a] != "." and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]
        if "." not in self.board:
            return "DRAW"
        return None

    def broadcast(self, message):
        for conn in self.conns.values():
            try:
                conn.sendall((message + "\n").encode("utf-8"))
            except OSError:
                pass

    def send_state(self):
        self.broadcast("BOARD " + "".join(self.board))
        self.broadcast("TURN " + self.turn)

    def apply_move(self, player, position):
        """Mutates state and returns (ok, reason). Does NOT broadcast --
        the caller sends the direct ack first, then calls
        broadcast_after_move() so the mover's own connection sees its ack
        before the board-state broadcast, keeping wire order deterministic.
        """
        with self.lock:
            if self.over:
                return False, "game already over"
            if player != self.turn:
                return False, "not your turn"
            if not (0 <= position <= 8):
                return False, "position out of range"
            if self.board[position] != ".":
                return False, "square occupied"

            self.board[position] = player
            result = self.winner()
            if result:
                self.over = True
                self._pending_result = result
            else:
                self.turn = "O" if self.turn == "X" else "X"
                self._pending_result = None
            return True, "OK"

    def broadcast_after_move(self):
        self.broadcast("BOARD " + "".join(self.board))
        if self._pending_result:
            self.broadcast("DRAW" if self._pending_result == "DRAW" else f"WIN {self._pending_result}")
        else:
            self.broadcast("TURN " + self.turn)


def handle_player(conn, player, game):
    conn.sendall(f"YOU ARE {player}\n".encode("utf-8"))
    with conn.makefile("r", encoding="utf-8") as reader:
        for line in reader:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) == 2 and parts[0].upper() == "MOVE":
                try:
                    pos = int(parts[1])
                except ValueError:
                    conn.sendall(b"ERR invalid move format\n")
                    continue
                ok, reason = game.apply_move(player, pos)
                conn.sendall((("OK" if ok else f"ERR {reason}") + "\n").encode("utf-8"))
                if ok:
                    game.broadcast_after_move()
                if game.over:
                    return
            else:
                conn.sendall(b"ERR unknown command\n")


def run_one_game(server_socket):
    """Accepts exactly two connections and runs one game to completion."""
    conn_x, _ = server_socket.accept()
    conn_o, _ = server_socket.accept()

    game = Game(conn_x, conn_o)
    game.send_state()

    t1 = threading.Thread(target=handle_player, args=(conn_x, "X", game))
    t2 = threading.Thread(target=handle_player, args=(conn_o, "O", game))
    t1.start()
    t2.start()
    return game, t1, t2, conn_x, conn_o


def start_server(host="localhost", port=9091):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"Tic-tac-toe server listening on {host}:{server_socket.getsockname()[1]}")
    return server_socket


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=9091)
    args = parser.parse_args()

    server_socket = start_server(args.host, args.port)
    try:
        while True:
            print("Waiting for two players...")
            run_one_game(server_socket)
    except KeyboardInterrupt:
        server_socket.close()


if __name__ == "__main__":
    main()
