#pragma once

#include <stdexcept>
#include <vector>

template <typename T>
class Stack {
public:
    void push(const T &value) {
        items_.push_back(value);
    }

    T pop() {
        if (items_.empty()) {
            throw std::out_of_range("pop from empty stack");
        }
        T value = items_.back();
        items_.pop_back();
        return value;
    }

    const T &peek() const {
        if (items_.empty()) {
            throw std::out_of_range("peek on empty stack");
        }
        return items_.back();
    }

    bool empty() const {
        return items_.empty();
    }

    size_t size() const {
        return items_.size();
    }

private:
    std::vector<T> items_;
};
