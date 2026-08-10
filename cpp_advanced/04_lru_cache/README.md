# LRU Cache

**Level:** Advanced | **Concepts:** templates, hash map + intrusive doubly-linked list, O(1) get/put

A generic least-recently-used cache with O(1) `get`/`put`: a
`std::unordered_map<Key, ListIterator>` for lookup, and a
`std::list<std::pair<Key, Value>>` ordered from most- to least-recently
used, so eviction is just popping the back and touching a key is just a
splice to the front (no reallocation, no shifting).

## Files

- `lru_cache.hpp` — `LRUCache<Key, Value>` template
- `main.cpp` — demo + a small correctness test: fills a capacity-3 cache,
  confirms the right key gets evicted, confirms `get()` promotes recency

## How to run

```bash
make
./lru_demo
```

## Notes

`std::list::splice` is the trick that makes "touch this key" a pointer
fixup instead of a search-then-move — it moves a node between (or within)
lists in O(1) without invalidating any other iterators, which is exactly
why the map can safely cache iterators into the list long-term.
