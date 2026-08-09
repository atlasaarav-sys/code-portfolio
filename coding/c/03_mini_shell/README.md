# 03 — Mini Shell

**Language:** C (C11, POSIX)
**Level:** Advanced (for this track)

## What this demonstrates

- `fork()`/`execvp()`/`waitpid()` process control
- Parsing a command line into argv
- Built-in commands (`cd`, `exit`) vs. external commands
- Basic single-pipe support (`cmd1 | cmd2`)

## Platform note

This project uses POSIX APIs (`unistd.h`, `sys/wait.h`) and will **not**
compile with MSVC on Windows. Build it under WSL, Linux, or macOS, or with
MinGW/Cygwin's POSIX layer on Windows.

## Files

- `shell.c` — the whole shell (single file, deliberately kept simple)

## How to run

```bash
make
./mini_shell
```

Example session:

```
mini_shell> ls -la
mini_shell> echo hello | wc -w
mini_shell> cd ..
mini_shell> exit
```

## Notes

Intentionally minimal — no job control, no quoting/escaping, no multi-pipe
chains. That's the natural "next step" if extending this further.
