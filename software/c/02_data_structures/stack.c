#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define STACK_CAPACITY 128

typedef struct {
    char items[STACK_CAPACITY];
    int top; /* index of top element, -1 if empty */
} CharStack;

void stack_init(CharStack *s) {
    s->top = -1;
}

bool stack_is_empty(const CharStack *s) {
    return s->top == -1;
}

bool stack_push(CharStack *s, char c) {
    if (s->top >= STACK_CAPACITY - 1) {
        return false;
    }
    s->items[++s->top] = c;
    return true;
}

bool stack_pop(CharStack *s, char *out) {
    if (stack_is_empty(s)) {
        return false;
    }
    *out = s->items[s->top--];
    return true;
}

bool is_balanced(const char *expr) {
    CharStack s;
    stack_init(&s);

    for (size_t i = 0; i < strlen(expr); i++) {
        char c = expr[i];
        if (c == '(' || c == '[' || c == '{') {
            stack_push(&s, c);
        } else if (c == ')' || c == ']' || c == '}') {
            char top;
            if (!stack_pop(&s, &top)) {
                return false;
            }
            if ((c == ')' && top != '(') ||
                (c == ']' && top != '[') ||
                (c == '}' && top != '{')) {
                return false;
            }
        }
    }
    return stack_is_empty(&s);
}

int main(void) {
    const char *tests[] = {"(a[b]{c})", "(a[b)]", "{[()]}", "((("};
    for (size_t i = 0; i < sizeof(tests) / sizeof(tests[0]); i++) {
        printf("\"%s\" balanced? %s\n", tests[i], is_balanced(tests[i]) ? "true" : "false");
    }
    return 0;
}
