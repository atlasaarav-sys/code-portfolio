"""Stack and Queue built on a plain Python list, plus a practical use case."""


class Stack:
    def __init__(self):
        self._items = []

    def push(self, value):
        self._items.append(value)

    def pop(self):
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        return self._items[-1] if self._items else None

    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)


class Queue:
    def __init__(self):
        self._items = []

    def enqueue(self, value):
        self._items.append(value)

    def dequeue(self):
        if not self._items:
            raise IndexError("dequeue from empty queue")
        return self._items.pop(0)

    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)


def is_balanced(expression: str) -> bool:
    """Check balanced (), [], {} using a stack."""
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = Stack()
    for ch in expression:
        if ch in "([{":
            stack.push(ch)
        elif ch in ")]}":
            if stack.is_empty() or stack.pop() != pairs[ch]:
                return False
    return stack.is_empty()


def main():
    s = Stack()
    for v in [1, 2, 3]:
        s.push(v)
    print("stack pop order:", [s.pop() for _ in range(3)])

    q = Queue()
    for v in [1, 2, 3]:
        q.enqueue(v)
    print("queue dequeue order:", [q.dequeue() for _ in range(3)])

    for expr in ["(a[b]{c})", "(a[b)]", "{[()]}", "((("]:
        print(f"{expr!r} balanced? {is_balanced(expr)}")


if __name__ == "__main__":
    main()
