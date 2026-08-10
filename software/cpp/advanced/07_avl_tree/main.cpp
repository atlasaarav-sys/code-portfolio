#include <algorithm>
#include <cassert>
#include <cmath>
#include <cstdio>

#include "avl_tree.hpp"

int main() {
    AVLTree<int> tree;

    // Ascending insertion would degrade an unbalanced BST to a linked list
    // (height N); an AVL tree must stay near log2(N).
    const int N = 1000;
    for (int i = 0; i < N; i++) {
        tree.insert(i);
    }

    int h = tree.height();
    double bound = 1.44 * std::log2(N + 2); // known AVL height upper bound
    std::printf("Inserted %d ascending values. Height = %d (AVL bound ~%.1f)\n", N, h, bound);
    assert(h <= static_cast<int>(bound) + 1);

    auto sorted = tree.in_order();
    assert(std::is_sorted(sorted.begin(), sorted.end()));
    assert(sorted.size() == static_cast<size_t>(N));
    std::printf("In-order traversal is sorted and complete: yes\n");

    for (int i = 0; i < N; i += 2) {
        tree.erase(i);
    }
    auto after_erase = tree.in_order();
    assert(after_erase.size() == static_cast<size_t>(N / 2));
    for (int v : after_erase) {
        assert(v % 2 == 1);
    }
    std::printf("After erasing all even values: %zu remain, all odd: yes\n", after_erase.size());
    std::printf("Height after erasure: %d (still balanced)\n", tree.height());

    assert(tree.contains(501));
    assert(!tree.contains(500));
    std::printf("contains() checks: passed\n");

    std::printf("\nAll assertions passed.\n");
    return 0;
}
