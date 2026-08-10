#pragma once

#include <algorithm>
#include <memory>
#include <vector>

template <typename T>
class AVLTree {
public:
    void insert(const T &value) {
        root_ = insert(std::move(root_), value);
    }

    void erase(const T &value) {
        root_ = erase(std::move(root_), value);
    }

    bool contains(const T &value) const {
        Node *node = root_.get();
        while (node) {
            if (value == node->value) return true;
            node = (value < node->value) ? node->left.get() : node->right.get();
        }
        return false;
    }

    int height() const { return height(root_.get()); }

    std::vector<T> in_order() const {
        std::vector<T> result;
        in_order(root_.get(), result);
        return result;
    }

private:
    struct Node {
        T value;
        int height = 1;
        std::unique_ptr<Node> left;
        std::unique_ptr<Node> right;
        explicit Node(const T &v) : value(v) {}
    };

    std::unique_ptr<Node> root_;

    static int height(const Node *n) { return n ? n->height : 0; }

    static int balance_factor(const Node *n) {
        return n ? height(n->right.get()) - height(n->left.get()) : 0;
    }

    static void update_height(Node *n) {
        n->height = 1 + std::max(height(n->left.get()), height(n->right.get()));
    }

    static std::unique_ptr<Node> rotate_left(std::unique_ptr<Node> n) {
        std::unique_ptr<Node> new_root = std::move(n->right);
        n->right = std::move(new_root->left);
        update_height(n.get());
        new_root->left = std::move(n);
        update_height(new_root.get());
        return new_root;
    }

    static std::unique_ptr<Node> rotate_right(std::unique_ptr<Node> n) {
        std::unique_ptr<Node> new_root = std::move(n->left);
        n->left = std::move(new_root->right);
        update_height(n.get());
        new_root->right = std::move(n);
        update_height(new_root.get());
        return new_root;
    }

    static std::unique_ptr<Node> rebalance(std::unique_ptr<Node> n) {
        update_height(n.get());
        int bf = balance_factor(n.get());

        if (bf > 1) { // right-heavy
            if (balance_factor(n->right.get()) < 0) {
                n->right = rotate_right(std::move(n->right)); // right-left case
            }
            return rotate_left(std::move(n)); // right-right case
        }
        if (bf < -1) { // left-heavy
            if (balance_factor(n->left.get()) > 0) {
                n->left = rotate_left(std::move(n->left)); // left-right case
            }
            return rotate_right(std::move(n)); // left-left case
        }
        return n;
    }

    static std::unique_ptr<Node> insert(std::unique_ptr<Node> n, const T &value) {
        if (!n) return std::make_unique<Node>(value);
        if (value < n->value) {
            n->left = insert(std::move(n->left), value);
        } else if (value > n->value) {
            n->right = insert(std::move(n->right), value);
        } else {
            return n; // duplicate, no-op
        }
        return rebalance(std::move(n));
    }

    static std::unique_ptr<Node> min_node_extract(std::unique_ptr<Node> &n, T &out_value) {
        if (!n->left) {
            out_value = n->value;
            return std::move(n->right);
        }
        n->left = min_node_extract(n->left, out_value);
        return rebalance(std::move(n));
    }

    static std::unique_ptr<Node> erase(std::unique_ptr<Node> n, const T &value) {
        if (!n) return nullptr;

        if (value < n->value) {
            n->left = erase(std::move(n->left), value);
        } else if (value > n->value) {
            n->right = erase(std::move(n->right), value);
        } else {
            if (!n->left) return std::move(n->right);
            if (!n->right) return std::move(n->left);
            T successor_value;
            n->right = min_node_extract(n->right, successor_value);
            n->value = successor_value;
        }
        return rebalance(std::move(n));
    }

    static void in_order(const Node *n, std::vector<T> &out) {
        if (!n) return;
        in_order(n->left.get(), out);
        out.push_back(n->value);
        in_order(n->right.get(), out);
    }
};
