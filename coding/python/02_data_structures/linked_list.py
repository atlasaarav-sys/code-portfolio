"""Singly linked list implemented from scratch."""


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, value):
        node = Node(value)
        if not self.head:
            self.head = node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = node

    def prepend(self, value):
        node = Node(value)
        node.next = self.head
        self.head = node

    def delete(self, value):
        if not self.head:
            return False
        if self.head.value == value:
            self.head = self.head.next
            return True
        current = self.head
        while current.next:
            if current.next.value == value:
                current.next = current.next.next
                return True
            current = current.next
        return False

    def find(self, value):
        current = self.head
        while current:
            if current.value == value:
                return True
            current = current.next
        return False

    def reverse(self):
        prev = None
        current = self.head
        while current:
            nxt = current.next
            current.next = prev
            prev = current
            current = nxt
        self.head = prev

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.value)
            current = current.next
        return result

    def __repr__(self):
        return " -> ".join(str(v) for v in self.to_list())


def main():
    ll = LinkedList()
    for v in [1, 2, 3, 4, 5]:
        ll.append(v)
    print("list:", ll)

    ll.prepend(0)
    print("after prepend(0):", ll)

    ll.delete(3)
    print("after delete(3):", ll)

    print("find(4):", ll.find(4))
    print("find(99):", ll.find(99))

    ll.reverse()
    print("reversed:", ll)


if __name__ == "__main__":
    main()
