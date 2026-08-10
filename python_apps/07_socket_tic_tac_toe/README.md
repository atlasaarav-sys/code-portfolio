# Socket Tic-Tac-Toe

**Stack:** Python 3, raw TCP sockets (stdlib only)

Two-player tic-tac-toe over TCP: the server holds authoritative game state
(board, whose turn it is), both clients connect and are assigned X or O,
and the server rejects out-of-turn or illegal moves rather than trusting
the client.

## Protocol

```
Server -> client on connect:  "YOU ARE X" or "YOU ARE O"
Server -> both clients each turn: "BOARD <9 chars, . for empty>" then "TURN X" or "TURN O"
Client -> server: "MOVE <0-8>"        (board position, row-major)
Server -> client: "OK" | "ERR <reason>"
Server -> both clients on end: "WIN X" | "WIN O" | "DRAW"
```

## Files

- `ttt_server.py` — game state machine + two-connection game loop
  (blocks accepting a 3rd connection until a game slot frees up)
- `ttt_client.py` — a scriptable client (`TicTacToeClient`) used by the
  automated test and usable as a basis for a real interactive client
- `test_ttt.py` — starts the server, connects two scripted clients,
  plays a full game (X wins via top row), and asserts the server reports
  the win, rejects an out-of-turn move, and rejects a move on an occupied
  square

## How to run

```bash
python ttt_server.py --port 9091
```

From two other terminals, connect with `nc localhost 9091` and send
`MOVE <0-8>` lines, or use `ttt_client.py` programmatically.

Run tests:

```bash
python -m unittest test_ttt.py
```
