# Python Apps

Eleven small, real applications — networking, persistence, cryptography
basics, text processing, and a data/LLM pipeline — written mostly using
just the Python standard library so every one of them is runnable as-is
(app 11 optionally uses the Anthropic API). Each was actually executed
while building this repo, not just written and hoped to work.

## Apps

| # | App | What it does |
|---|---|---|
| 1 | [Markdown Static Site Generator](01_markdown_static_site_generator) | converts a folder of `.md` files into a styled HTML site |
| 2 | [Expense Tracker (SQLite)](02_expense_tracker_sqlite) | CLI expense log with categories, `sqlite3` backend, monthly reports |
| 3 | [File Deduplicator](03_file_deduplicator) | finds duplicate files by content hash, with a dry-run/delete mode |
| 4 | [URL Shortener Service](04_url_shortener_service) | `http.server`-based REST API backed by SQLite |
| 5 | [Markov Text Generator](05_markov_text_generator) | trains an n-gram Markov chain on a text corpus, generates new text |
| 6 | [Key-Value Store Server](06_key_value_store_server) | tiny Redis-like server over raw sockets, `GET`/`SET`/`DEL`/`EXPIRE` |
| 7 | [Socket Tic-Tac-Toe](07_socket_tic_tac_toe) | two-player game over TCP sockets, server enforces turns/win detection |
| 8 | [Password Manager CLI](08_password_manager_cli) | local encrypted vault, PBKDF2-derived key, master password |
| 9 | [RSS Feed Aggregator](09_rss_feed_aggregator) | fetches and parses RSS/Atom feeds with `urllib` + `xml.etree`, dedupes entries |
| 10 | [Threaded Chat Server](10_threaded_chat_server) | multi-client TCP chat server, one thread per connection |
| 11 | [AI-Assisted Telemetry Diagnostics](11_ai_telemetry_diagnostics) | ingests CAN-bus/sensor telemetry CSVs, runs anomaly detection, generates plain-language diagnostic summaries (LLM-backed with a rule-based offline fallback) |

## Notes

Every project's `README.md` has exact run commands. Server/client apps
(4, 6, 7, 10) were tested by starting the server and driving it with a
scripted client in the same session; see each README for the specific test
transcript.
