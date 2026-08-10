#include <stdio.h>

void increment(int *value) {
    (*value)++;
}

void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

void print_array_via_pointer(const int *arr, size_t len) {
    for (size_t i = 0; i < len; i++) {
        printf("%d ", *(arr + i)); /* pointer arithmetic == arr[i] */
    }
    printf("\n");
}

int main(void) {
    int x = 5;
    int *px = &x;
    printf("x = %d, *px = %d, address of x = %p\n", x, *px, (void *)px);

    increment(px);
    printf("after increment(px): x = %d\n", x);

    int a = 1, b = 2;
    printf("before swap: a=%d b=%d\n", a, b);
    swap(&a, &b);
    printf("after swap: a=%d b=%d\n", a, b);

    int arr[] = {1, 2, 3, 4, 5};
    size_t len = sizeof(arr) / sizeof(arr[0]);
    print_array_via_pointer(arr, len);

    /* arrays decay to pointers */
    int *p = arr;
    printf("arr[2] via pointer indexing: %d\n", p[2]);

    return 0;
}
