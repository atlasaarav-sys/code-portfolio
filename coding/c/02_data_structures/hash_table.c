#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BUCKET_COUNT 16

typedef struct Entry {
    char *key;
    unsigned long value;
    struct Entry *next;
} Entry;

typedef struct {
    Entry *buckets[BUCKET_COUNT];
} HashTable;

unsigned long hash_string(const char *str) {
    /* djb2 */
    unsigned long hash = 5381;
    int c;
    while ((c = *str++)) {
        hash = ((hash << 5) + hash) + (unsigned long)c;
    }
    return hash;
}

void table_init(HashTable *table) {
    memset(table->buckets, 0, sizeof(table->buckets));
}

char *str_dup(const char *s) {
    size_t len = strlen(s) + 1;
    char *copy = malloc(len);
    if (!copy) {
        fprintf(stderr, "malloc failed\n");
        exit(1);
    }
    memcpy(copy, s, len);
    return copy;
}

void table_set(HashTable *table, const char *key, unsigned long value) {
    unsigned long index = hash_string(key) % BUCKET_COUNT;
    Entry *entry = table->buckets[index];

    while (entry) {
        if (strcmp(entry->key, key) == 0) {
            entry->value = value;
            return;
        }
        entry = entry->next;
    }

    Entry *new_entry = malloc(sizeof(Entry));
    if (!new_entry) {
        fprintf(stderr, "malloc failed\n");
        exit(1);
    }
    new_entry->key = str_dup(key);
    new_entry->value = value;
    new_entry->next = table->buckets[index];
    table->buckets[index] = new_entry;
}

int table_get(const HashTable *table, const char *key, unsigned long *out) {
    unsigned long index = hash_string(key) % BUCKET_COUNT;
    Entry *entry = table->buckets[index];

    while (entry) {
        if (strcmp(entry->key, key) == 0) {
            *out = entry->value;
            return 1;
        }
        entry = entry->next;
    }
    return 0;
}

void table_free(HashTable *table) {
    for (int i = 0; i < BUCKET_COUNT; i++) {
        Entry *entry = table->buckets[i];
        while (entry) {
            Entry *next = entry->next;
            free(entry->key);
            free(entry);
            entry = next;
        }
        table->buckets[i] = NULL;
    }
}

int main(void) {
    HashTable table;
    table_init(&table);

    table_set(&table, "apples", 10);
    table_set(&table, "bananas", 5);
    table_set(&table, "cherries", 100);
    table_set(&table, "apples", 12); /* overwrite */

    const char *keys[] = {"apples", "bananas", "cherries", "durian"};
    for (size_t i = 0; i < sizeof(keys) / sizeof(keys[0]); i++) {
        unsigned long value;
        if (table_get(&table, keys[i], &value)) {
            printf("%s -> %lu\n", keys[i], value);
        } else {
            printf("%s -> (not found)\n", keys[i]);
        }
    }

    table_free(&table);
    return 0;
}
