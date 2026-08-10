CC = gcc
CFLAGS = -Wall -Wextra -std=c11
TARGETS = basics pointers structs

all: $(TARGETS)

basics: basics.c
	$(CC) $(CFLAGS) -o $@ $<

pointers: pointers.c
	$(CC) $(CFLAGS) -o $@ $<

structs: structs.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(TARGETS) *.o
