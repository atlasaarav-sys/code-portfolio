# Expression Evaluator (Shunting-Yard)

**Level:** Advanced | **Concepts:** operator precedence parsing, RPN, tokenizing

An arithmetic expression evaluator: tokenizes an infix expression, converts
it to Reverse Polish Notation using Dijkstra's shunting-yard algorithm
(handles `+ - * / ^`, unary minus, parentheses, and correct operator
precedence/associativity — `^` is right-associative, the rest left), then
evaluates the RPN with a simple stack machine. Also supports named
variables via a substitution map.

## Files

- `tokenizer.hpp` — splits an expression string into numbers, operators,
  parens, and identifiers
- `shunting_yard.hpp` — infix token stream -> RPN token stream
- `evaluator.hpp` — evaluates an RPN token stream given a variable map
- `main.cpp` — evaluates a set of expressions (including precedence,
  associativity, and variable substitution cases) and checks each against
  the expected result

## How to run

```bash
make
./expr_demo
```

## Notes

Unary minus is handled by having the tokenizer/shunting-yard distinguish
"minus that follows an operator, `(`, or nothing before it" (unary) from
"minus that follows a number, identifier, or `)`" (binary) — that
distinction is the one easy-to-get-wrong part of this whole pipeline.
