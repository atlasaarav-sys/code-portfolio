"""Binary search and duplicate-aware variants. All require sorted input."""


def binary_search(items: list, target) -> int:
    """O(log n) time. Returns an index of target, or -1 if not found.
    If there are duplicates, which index is returned is unspecified --
    use find_first/find_last for that."""
    lo, hi = 0, len(items) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if items[mid] == target:
            return mid
        elif items[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def find_first(items: list, target) -> int:
    """O(log n) time. Returns the index of the first occurrence of target,
    or -1 if not found."""
    lo, hi = 0, len(items) - 1
    result = -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if items[mid] == target:
            result = mid
            hi = mid - 1  # keep searching left for an earlier occurrence
        elif items[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return result


def find_last(items: list, target) -> int:
    """O(log n) time. Returns the index of the last occurrence of target,
    or -1 if not found."""
    lo, hi = 0, len(items) - 1
    result = -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if items[mid] == target:
            result = mid
            lo = mid + 1  # keep searching right for a later occurrence
        elif items[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return result
