# Threaded Chat Server

**Stack:** Python 3, raw TCP sockets + `threading` (stdlib only)

A multi-client TCP chat server: each connection gets its own handler
thread, a shared client registry (protected by a lock) is used to
broadcast messages to everyone else, `/nick <name>` sets a display name,
and `/quit` disconnects cleanly with a leave announcement to the room.

## Files

- `chat_server.py` — connection accept loop, per-client handler thread,
  broadcast logic
- `chat_client.py` — scriptable client used by the test (and usable as a
  base for a real interactive client)
- `test_chat_server.py` — connects three scripted clients, verifies
  messages from one client are broadcast to the *other* two (not
  echoed back to the sender), verifies `/nick` changes the displayed name
  on subsequent messages, and verifies a join/leave announcement fires

## How to run

```bash
python chat_server.py --port 9092
```

From multiple terminals: `nc localhost 9092`, type `/nick alice`, then
just type messages.

Run tests:

```bash
python -m unittest test_chat_server.py
```
