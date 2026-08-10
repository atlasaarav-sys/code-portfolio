#include <iostream>
#include <memory>

#include "linked_list.hpp"
#include "stack.hpp"

template <typename T>
class BST {
public:
    void insert(const T &value) {
        root_ = insert(std::move(root_), value);
    }

    bool search(const T &value) const {
        return search(root_.get(), value);
    }

private:
    struct Node {
        T value;
        std::unique_ptr<Node> left;
        std::unique_ptr<Node> right;
        explicit Node(const T &v) : value(v) {}
    };

    std::unique_ptr<Node> insert(std::unique_ptr<Node> node, const T &value) {
        if (!node) {
            return std::make_unique<Node>(value);
        }
        if (value < node->value) {
            node->left = insert(std::move(node->left), value);
        } else if (value > node->value) {
            node->right = insert(std::move(node->right), value);
        }
        return node;
    }

    bool search(const Node *node, const T &value) const {
        if (!node) {
            return false;
        }
        if (value == node->value) {
            return true;
        }
        return value < node->value ? search(node->left.get(), value)
                                    : search(node->right.get(), value);
    }

    std::unique_ptr<Node> root_;
};

int main() {
    LinkedList<int> list;
    for (int i = 1; i <= 5; i++) {
        list.push_back(i);
    }
    std::cout << "list: " << list.to_string() << "\n";
    list.remove(3);
    std::cout << "after remove(3): " << list.to_string() << "\n";

    Stack<std::string> stack;
    stack.push("a");
    stack.push("b");
    stack.push("c");
    std::cout << "stack pop order: ";
    while (!stack.empty()) {
        std::cout << stack.pop() << " ";
    }
    std::cout << "\n";

    try {
        Stack<int> empty_stack;
        empty_stack.pop();
    } catch (const std::out_of_range &e) {
        std::cout << "caught expected exception: " << e.what() << "\n";
    }

    BST<int> bst;
    for (int v : {8, 3, 10, 1, 6, 14}) {
        bst.insert(v);
    }
    std::cout << "bst.search(6) = " << std::boolalpha << bst.search(6) << "\n";
    std::cout << "bst.search(99) = " << std::boolalpha << bst.search(99) << "\n";

    return 0;
}
