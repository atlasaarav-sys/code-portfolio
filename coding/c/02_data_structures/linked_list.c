#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int value;
    struct Node *next;
} Node;

typedef struct {
    Node *head;
} LinkedList;

Node *node_create(int value) {
    Node *node = malloc(sizeof(Node));
    if (!node) {
        fprintf(stderr, "malloc failed\n");
        exit(1);
    }
    node->value = value;
    node->next = NULL;
    return node;
}

void list_append(LinkedList *list, int value) {
    Node *node = node_create(value);
    if (!list->head) {
        list->head = node;
        return;
    }
    Node *current = list->head;
    while (current->next) {
        current = current->next;
    }
    current->next = node;
}

int list_delete(LinkedList *list, int value) {
    Node *current = list->head;
    Node *prev = NULL;

    while (current) {
        if (current->value == value) {
            if (prev) {
                prev->next = current->next;
            } else {
                list->head = current->next;
            }
            free(current);
            return 1;
        }
        prev = current;
        current = current->next;
    }
    return 0;
}

void list_print(const LinkedList *list) {
    Node *current = list->head;
    while (current) {
        printf("%d", current->value);
        if (current->next) {
            printf(" -> ");
        }
        current = current->next;
    }
    printf("\n");
}

void list_free(LinkedList *list) {
    Node *current = list->head;
    while (current) {
        Node *next = current->next;
        free(current);
        current = next;
    }
    list->head = NULL;
}

int main(void) {
    LinkedList list = {NULL};

    for (int i = 1; i <= 5; i++) {
        list_append(&list, i);
    }
    printf("list: ");
    list_print(&list);

    list_delete(&list, 3);
    printf("after delete(3): ");
    list_print(&list);

    list_free(&list);
    printf("list freed\n");

    return 0;
}
