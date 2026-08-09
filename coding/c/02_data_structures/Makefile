CC = gcc
CFLAGS = -Wall -Wextra -std=c11
TARGETS = linked_list stack hash_table

all: $(TARGETS)

linked_list: linked_list.c
	$(CC) $(CFLAGS) -o $@ $<

stack: stack.c
	$(CC) $(CFLAGS) -o $@ $<

hash_table: hash_table.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(TARGETS) *.o
