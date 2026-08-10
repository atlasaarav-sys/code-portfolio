# JSON Parser

**Level:** Advanced | **Concepts:** recursive descent parsing, `std::variant`, recursive value trees

A JSON parser written from scratch (no library) — tokenizer-free recursive
descent directly over the character stream, producing a `JsonValue` tree
backed by `std::variant` (null/bool/number/string/array/object). Includes a
serializer to round-trip back to a JSON string.

## Files

- `json_value.hpp` — `JsonValue` (the variant-based tree) + a `dump()` serializer
- `json_parser.hpp` — recursive descent parser: `parse_value`,
  `parse_object`, `parse_array`, `parse_string`, `parse_number`, with
  string escape handling (`\"`, `\\`, `\n`, `\uXXXX`, etc.)
- `main.cpp` — parses a small nested JSON document, prints the recovered
  structure, and round-trips it back to text

## How to run

```bash
make
./json_demo
```

## Notes

`JsonValue`'s array/object variants hold `std::vector<JsonValue>` and
`std::vector<std::pair<std::string, JsonValue>>` respectively (an
insertion-ordered "object" rather than a `map`, matching how most real
JSON tooling treats key order) — recursive types like this need the
`vector`-of-incomplete-type trick or, as here, `std::variant` member types
that are themselves complete via indirection through `vector`.
