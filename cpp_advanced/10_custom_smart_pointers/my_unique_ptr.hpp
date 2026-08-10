#pragma once

#include <utility>

template <typename T>
class MyUniquePtr {
public:
    MyUniquePtr() = default;
    explicit MyUniquePtr(T *ptr) : ptr_(ptr) {}

    ~MyUniquePtr() { delete ptr_; }

    MyUniquePtr(const MyUniquePtr &) = delete;
    MyUniquePtr &operator=(const MyUniquePtr &) = delete;

    MyUniquePtr(MyUniquePtr &&other) noexcept : ptr_(other.ptr_) {
        other.ptr_ = nullptr;
    }

    MyUniquePtr &operator=(MyUniquePtr &&other) noexcept {
        if (this != &other) {
            delete ptr_;
            ptr_ = other.ptr_;
            other.ptr_ = nullptr;
        }
        return *this;
    }

    T &operator*() const { return *ptr_; }
    T *operator->() const { return ptr_; }
    T *get() const { return ptr_; }
    explicit operator bool() const { return ptr_ != nullptr; }

    T *release() {
        T *old = ptr_;
        ptr_ = nullptr;
        return old;
    }

    void reset(T *new_ptr = nullptr) {
        delete ptr_;
        ptr_ = new_ptr;
    }

private:
    T *ptr_ = nullptr;
};

template <typename T, typename... Args>
MyUniquePtr<T> make_my_unique(Args &&...args) {
    return MyUniquePtr<T>(new T(std::forward<Args>(args)...));
}
