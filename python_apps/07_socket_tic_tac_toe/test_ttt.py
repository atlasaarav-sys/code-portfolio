import socket
import threading
import unittest

from ttt_server import start_server, run_one_game
from ttt_client import TicTacToeClient


class TestTicTacToe(unittest.TestCase):
    def setUp(self):
        self.server_socket = start_server(port=0)
        self.port = self.server_socket.getsockname()[1]
        self.game_holder = {}

        def accept_one_game():
            game, t1, t2, conn_x, conn_o = run_one_game(self.server_socket)
            self.game_holder["game"] = game
            t1.join()
            t2.join()

        self.accept_thread = threading.Thread(target=accept_one_game, daemon=True)
        self.accept_thread.start()

        self.client_x = TicTacToeClient("localhost", self.port)
        self.client_o = TicTacToeClient("localhost", self.port)

        # Drain the 3 initial lines each client gets (YOU ARE / BOARD / TURN),
        # order-agnostic since broadcast and the "YOU ARE" ack can interleave.
        self._drain_initial(self.client_x)
        self._drain_initial(self.client_o)

    def tearDown(self):
        self.client_x.close()
        self.client_o.close()
        self.server_socket.close()

    def _drain_initial(self, client):
        lines = [client.read_line() for _ in range(3)]
        self.assertTrue(any(l.startswith("YOU ARE") for l in lines))
        self.assertTrue(any(l.startswith("BOARD") for l in lines))
        self.assertTrue(any(l.startswith("TURN") for l in lines))

    def _do_move(self, mover, other, position, expect_game_over=False):
        ack = mover.move(position)
        self.assertEqual(ack, "OK")
        # mover's connection: BOARD + (TURN or WIN/DRAW)
        mover_lines = [mover.read_line(), mover.read_line()]
        other_lines = [other.read_line(), other.read_line()]
        self.assertTrue(mover_lines[0].startswith("BOARD"))
        self.assertTrue(other_lines[0].startswith("BOARD"))
        return mover_lines, other_lines

    def test_x_wins_top_row(self):
        # X: 0, 1, 2 (top row)  O: 3, 4
        self._do_move(self.client_x, self.client_o, 0)
        self._do_move(self.client_o, self.client_x, 3)
        self._do_move(self.client_x, self.client_o, 1)
        self._do_move(self.client_o, self.client_x, 4)
        mover_lines, other_lines = self._do_move(self.client_x, self.client_o, 2, expect_game_over=True)

        self.assertEqual(mover_lines[1], "WIN X")
        self.assertEqual(other_lines[1], "WIN X")

    def test_rejects_out_of_turn_move(self):
        # X hasn't moved yet, O tries to move -- should be rejected.
        ack = self.client_o.move(0)
        self.assertTrue(ack.startswith("ERR"))
        self.assertIn("not your turn", ack)

    def test_rejects_move_on_occupied_square(self):
        self._do_move(self.client_x, self.client_o, 0)
        ack = self.client_o.move(0)
        self.assertTrue(ack.startswith("ERR"))
        self.assertIn("occupied", ack)


if __name__ == "__main__":
    unittest.main()
