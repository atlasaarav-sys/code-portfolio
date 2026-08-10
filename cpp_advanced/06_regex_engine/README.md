# Regex Engine (Thompson NFA)

**Level:** Advanced | **Concepts:** NFA construction, Thompson's construction, non-backtracking matching

A small regex engine supporting literals, `.` (any char), `*`, `+`, `?`,
`|` (alternation), and `(...)` grouping — built the way `grep`/`re2`-style
engines are built: parse to an AST, compile the AST to a Thompson NFA
(states + epsilon transitions), then simulate the NFA by tracking the
*set* of possible states at each input position (Thompson's original
algorithm) instead of backtracking. That guarantees linear-time matching
in the input length, unlike backtracking engines that can go exponential
on pathological patterns.

## Files

- `regex_ast.hpp` — AST node types (`Literal`, `Concat`, `Alternation`, `Star`, `Plus`, `Optional`, `AnyChar`)
- `regex_parser.hpp` — recursive descent parser: pattern string -> AST
  (handles `|` at the lowest precedence, then concatenation, then postfix
  `*`/`+`/`?`, then atoms/groups)
- `nfa.hpp` — Thompson's construction (AST -> NFA with epsilon
  transitions) and the state-set simulation matcher
- `main.cpp` — compiles a handful of patterns and matches them against
  test strings, printing pass/fail

## How to run

```bash
make
./regex_demo
```

## Notes

This matches (`fullmatch`-style, the whole string must match) rather than
searching for a substring — wrap a pattern in `.*` on both ends if you want
substring search. No character classes (`[a-z]`), anchors, or capture
groups — those are the natural next features once literals/alternation/
repetition are solid.
