#pragma once

#include <list>
#include <optional>
#include <unordered_map>

template <typename Key, typename Value>
class LRUCache {
public:
    explicit LRUCache(size_t capacity) : capacity_(capacity) {}

    // Returns the value if present, and marks it most-recently-used.
    std::optional<Value> get(const Key &key) {
        auto it = index_.find(key);
        if (it == index_.end()) {
            return std::nullopt;
        }
        // Move the touched node to the front (most-recently-used end).
        order_.splice(order_.begin(), order_, it->second);
        return it->second->second;
    }

    void put(const Key &key, Value value) {
        auto it = index_.find(key);
        if (it != index_.end()) {
            it->second->second = std::move(value);
            order_.splice(order_.begin(), order_, it->second);
            return;
        }

        if (index_.size() >= capacity_) {
            evict_lru();
        }

        order_.emplace_front(key, std::move(value));
        index_[key] = order_.begin();
    }

    bool contains(const Key &key) const {
        return index_.find(key) != index_.end();
    }

    size_t size() const { return index_.size(); }

private:
    void evict_lru() {
        if (order_.empty()) return;
        const Key &lru_key = order_.back().first;
        index_.erase(lru_key);
        order_.pop_back();
    }

    size_t capacity_;
    std::list<std::pair<Key, Value>> order_; // front = most recently used
    std::unordered_map<Key, typename std::list<std::pair<Key, Value>>::iterator> index_;
};
