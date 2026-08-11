#include <cassert>
#include <cstdio>
#include <string>

#include "lru_cache.hpp"

int main() {
    LRUCache<int, std::string> cache(3);

    cache.put(1, "one");
    cache.put(2, "two");
    cache.put(3, "three");
    // order (MRU->LRU): 3, 2, 1

    assert(cache.get(1).has_value() && *cache.get(1) == "one");
    // touching 1 makes it MRU: order now 1, 3, 2

    cache.put(4, "four");
    // capacity exceeded -> evict LRU, which is now 2
    assert(!cache.contains(2));
    assert(cache.contains(1));
    assert(cache.contains(3));
    assert(cache.contains(4));

    std::printf("Cache size after 4 puts (capacity 3): %zu\n", cache.size());
    std::printf("Key 2 evicted as expected: %s\n", !cache.contains(2) ? "yes" : "no");
    std::printf("Key 1 survived (was touched before eviction): %s\n", cache.contains(1) ? "yes" : "no");

    cache.put(3, "THREE-updated");
    assert(*cache.get(3) == "THREE-updated");
    std::printf("Update-in-place works: %s\n", (*cache.get(3) == "THREE-updated") ? "yes" : "no");

    std::printf("All assertions passed.\n");
    return 0;
}
