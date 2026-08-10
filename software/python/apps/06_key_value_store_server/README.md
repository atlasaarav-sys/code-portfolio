# Key-Value Store Server

**Stack:** Python 3, raw TCP sockets (stdlib only)

A tiny Redis-like in-memory key-value store with a line-based text
protocol over TCP: `GET`, `SET`, `DEL`, `EXPIRE`, `KEYS`. One thread per
connection; a background thread sweeps expired keys.

## Protocol

Newline-terminated commands, one per line:

```
SET key value       -> OK
GET key              -> value  |  (nil)
DEL key               -> 1  |  0
EXPIRE key seconds    -> OK  |  (nil) if key doesn't exist
KEYS                  -> space-separated list of live keys
```

## Files

- `kv_server.py` — the server: socket accept loop, one handler thread per
  client, a shared dict + lock, and an expiry-sweep background thread
- `kv_client.py` — a minimal client library (`KVClient.get/set/delete/...`)
  used by the tests and usable interactively
- `test_kv_server.py` — starts the server on an ephemeral port, drives it
  with the client, checks GET/SET/DEL/EXPIRE semantics including that an
  expired key actually stops being served

## How to run

```bash
python kv_server.py --port 9090
```

From another terminal:

```bash
python -c "
from kv_client import KVClient
c = KVClient('localhost', 9090)
c.set('foo', 'bar')
print(c.get('foo'))
"
```

Or just `nc localhost 9090` and type commands directly.

Run tests:

```bash
python -m unittest test_kv_server.py
```
