#include <cassert>
#include <cstdio>

#include "my_shared_ptr.hpp"
#include "my_unique_ptr.hpp"

struct Tracked {
    static int alive;
    int value;
    explicit Tracked(int v) : value(v) { alive++; }
    ~Tracked() { alive--; }
};
int Tracked::alive = 0;

void test_unique_ptr() {
    {
        MyUniquePtr<Tracked> a = make_my_unique<Tracked>(42);
        assert(Tracked::alive == 1);
        assert(a->value == 42);

        MyUniquePtr<Tracked> b = std::move(a);
        assert(!a); // moved-from is empty
        assert(b->value == 42);
        assert(Tracked::alive == 1); // still just one object, ownership transferred
    }
    assert(Tracked::alive == 0); // destroyed when b went out of scope
    std::printf("MyUniquePtr: move semantics + RAII destruction: PASS\n");
}

void test_shared_ptr() {
    MySharedPtr<Tracked> a = make_my_shared<Tracked>(7);
    assert(Tracked::alive == 1);
    assert(a.use_count() == 1);

    {
        MySharedPtr<Tracked> b = a; // copy: shares ownership
        assert(a.use_count() == 2);
        assert(b.use_count() == 2);
        assert(Tracked::alive == 1); // still one underlying object
    }
    // b destroyed, refcount back to 1
    assert(a.use_count() == 1);
    assert(Tracked::alive == 1);

    MySharedPtr<Tracked> c;
    c = a; // copy-assignment
    assert(a.use_count() == 2);

    c = MySharedPtr<Tracked>(); // release c's share
    assert(a.use_count() == 1);

    std::printf("MySharedPtr: reference counting + shared destruction timing: PASS\n");
}

int main() {
    test_unique_ptr();
    test_shared_ptr();
    std::printf("\nAll assertions passed.\n");
    return 0;
}
