#include <stdio.h>

int add(int a, int b) {
    return a + b;
}

int main(void) {
    /* Variables & format specifiers */
    int age = 21;
    float pi = 3.14159f;
    char grade = 'A';
    printf("age=%d pi=%.2f grade=%c\n", age, pi, grade);

    /* Control flow */
    for (int i = 1; i <= 5; i++) {
        if (i % 2 == 0) {
            printf("%d is even\n", i);
        } else {
            printf("%d is odd\n", i);
        }
    }

    int count = 0;
    while (count < 3) {
        printf("while loop iteration %d\n", count);
        count++;
    }

    int day = 3;
    switch (day) {
        case 1:
            printf("Monday\n");
            break;
        case 3:
            printf("Wednesday\n");
            break;
        default:
            printf("Some other day\n");
    }

    /* Functions */
    printf("add(2, 3) = %d\n", add(2, 3));

    /* Arrays */
    int numbers[5] = {10, 20, 30, 40, 50};
    int sum = 0;
    for (size_t i = 0; i < sizeof(numbers) / sizeof(numbers[0]); i++) {
        sum += numbers[i];
    }
    printf("array sum = %d\n", sum);

    return 0;
}
