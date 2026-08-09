#pragma once

#include <memory>
#include <sstream>
#include <string>

template <typename T>
class LinkedList {
public:
    void push_back(const T &value) {
        auto node = std::make_unique<Node>(value);
        if (!head_) {
            head_ = std::move(node);
            return;
        }
        Node *current = head_.get();
        while (current->next) {
            current = current->next.get();
        }
        current->next = std::move(node);
    }

    bool remove(const T &value) {
        if (!head_) {
            return false;
        }
        if (head_->data == value) {
            head_ = std::move(head_->next);
            return true;
        }
        Node *prev = head_.get();
        while (prev->next) {
            if (prev->next->data == value) {
                prev->next = std::move(prev->next->next);
                return true;
            }
            prev = prev->next.get();
        }
        return false;
    }

    std::string to_string() const {
        std::ostringstream oss;
        Node *current = head_.get();
        while (current) {
            oss << current->data;
            if (current->next) {
                oss << " -> ";
            }
            current = current->next.get();
        }
        return oss.str();
    }

private:
    struct Node {
        T data;
        std::unique_ptr<Node> next;
        explicit Node(const T &value) : data(value), next(nullptr) {}
    };

    std::unique_ptr<Node> head_;
};
