#pragma once

#include <atomic>
#include <utility>

template <typename T>
class MySharedPtr {
public:
    MySharedPtr() = default;

    explicit MySharedPtr(T *ptr) : ptr_(ptr) {
        if (ptr_) control_ = new ControlBlock{1};
    }

    ~MySharedPtr() { release(); }

    MySharedPtr(const MySharedPtr &other) : ptr_(other.ptr_), control_(other.control_) {
        if (control_) control_->ref_count.fetch_add(1, std::memory_order_relaxed);
    }

    MySharedPtr &operator=(const MySharedPtr &other) {
        if (this != &other) {
            release();
            ptr_ = other.ptr_;
            control_ = other.control_;
            if (control_) control_->ref_count.fetch_add(1, std::memory_order_relaxed);
        }
        return *this;
    }

    MySharedPtr(MySharedPtr &&other) noexcept : ptr_(other.ptr_), control_(other.control_) {
        other.ptr_ = nullptr;
        other.control_ = nullptr;
    }

    MySharedPtr &operator=(MySharedPtr &&other) noexcept {
        if (this != &other) {
            release();
            ptr_ = other.ptr_;
            control_ = other.control_;
            other.ptr_ = nullptr;
            other.control_ = nullptr;
        }
        return *this;
    }

    T &operator*() const { return *ptr_; }
    T *operator->() const { return ptr_; }
    T *get() const { return ptr_; }
    explicit operator bool() const { return ptr_ != nullptr; }

    long use_count() const { return control_ ? control_->ref_count.load(std::memory_order_relaxed) : 0; }

private:
    struct ControlBlock {
        std::atomic<int> ref_count;
    };

    void release() {
        if (control_ && control_->ref_count.fetch_sub(1, std::memory_order_acq_rel) == 1) {
            delete ptr_;
            delete control_;
        }
        ptr_ = nullptr;
        control_ = nullptr;
    }

    T *ptr_ = nullptr;
    ControlBlock *control_ = nullptr;
};

template <typename T, typename... Args>
MySharedPtr<T> make_my_shared(Args &&...args) {
    return MySharedPtr<T>(new T(std::forward<Args>(args)...));
}
