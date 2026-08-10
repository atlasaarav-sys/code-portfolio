"""Classic sorting algorithms, each returning a new sorted list."""

import heapq


def quicksort(items: list) -> list:
    """Average O(n log n) time, O(log n) space (recursion stack).
    Worst case O(n^2) on already-sorted input with this pivot choice
    (last element) -- a real implementation would randomize the pivot.
    """
    if len(items) <= 1:
        return list(items)

    pivot = items[-1]
    less = [x for x in items[:-1] if x <= pivot]
    greater = [x for x in items[:-1] if x > pivot]
    return quicksort(less) + [pivot] + quicksort(greater)


def mergesort(items: list) -> list:
    """O(n log n) time, O(n) space -- stable sort."""
    if len(items) <= 1:
        return list(items)

    mid = len(items) // 2
    left = mergesort(items[:mid])
    right = mergesort(items[mid:])
    return _merge(left, right)


def _merge(left: list, right: list) -> list:
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def heapsort(items: list) -> list:
    """O(n log n) time, O(n) space (this implementation builds a new heap
    rather than sorting in place)."""
    heap = list(items)
    heapq.heapify(heap)
    return [heapq.heappop(heap) for _ in range(len(heap))]
