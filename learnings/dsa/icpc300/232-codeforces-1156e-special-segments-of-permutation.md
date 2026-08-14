# ICPC300 232: Codeforces 1156E - Special Segments of Permutation

**Source:** [Codeforces 1156E - Special Segments of Permutation](https://codeforces.com/problemset/problem/1156/E)  
**Difficulty:** 2200  
**Pattern:** divide by interval maximum and enumerate the smaller side

## Exact contract

Given a permutation of `1..n`, count subarrays of length at least three whose
maximum value equals the sum of their two endpoint values.

## First principles

Let the maximum of interval `[left,right]` be at `middle`. Any special segment
crossing `middle` needs endpoint values summing to that maximum. Enumerate
indices on the smaller side; the needed value has one known position because
the input is a permutation. Then recurse into the two sides.

## Cases that decide correctness

- The maximum cannot be an endpoint because values are positive.
- Each special segment is counted at the recursion node containing its maximum.
- Needed endpoint values outside `1..n` do not exist.
- Enumerating the smaller side bounds how often one index is inspected.
- An interval of fewer than three positions contributes nothing.

## Brute force: inspect every subarray

```python
def special_segments_brute(permutation: list[int]) -> int:
    size = len(permutation)
    if sorted(permutation) != list(range(1, size + 1)):
        raise ValueError("input must be a permutation of 1..n")
    answer = 0
    for left in range(size):
        maximum = permutation[left]
        for right in range(left + 1, size):
            maximum = max(maximum, permutation[right])
            if right - left >= 2 and permutation[left] + permutation[right] == maximum:
                answer += 1
    return answer
```

This is `O(n^2)` time.

## Better approach: range maximum queries

A segment tree finds each recursive interval maximum in `O(log n)`, but
enumerating both sides can still be quadratic. Inspecting only the smaller side
is the key amortized improvement.

## Expert solution: maximum divide-and-conquer

```python
def count_special_segments(permutation: list[int]) -> int:
    size = len(permutation)
    if sorted(permutation) != list(range(1, size + 1)):
        raise ValueError("input must be a permutation of 1..n")
    if size < 3:
        return 0

    position = [0] * (size + 1)
    for index, value in enumerate(permutation):
        position[value] = index

    tree_size = 1
    while tree_size < size:
        tree_size *= 2
    tree = [(-1, -1)] * (2 * tree_size)
    for index, value in enumerate(permutation):
        tree[tree_size + index] = value, index
    for node in range(tree_size - 1, 0, -1):
        tree[node] = max(tree[node * 2], tree[node * 2 + 1])

    def interval_maximum(left: int, right: int) -> tuple[int, int]:
        result = -1, -1
        left += tree_size
        right += tree_size
        while left < right:
            if left & 1:
                result = max(result, tree[left])
                left += 1
            if right & 1:
                right -= 1
                result = max(result, tree[right])
            left //= 2
            right //= 2
        return result

    answer = 0
    intervals = [(0, size)]
    while intervals:
        left, right = intervals.pop()
        if right - left < 3:
            continue
        maximum, middle = interval_maximum(left, right)
        if middle - left < right - middle - 1:
            for first in range(left, middle):
                needed = maximum - permutation[first]
                if 1 <= needed <= size and middle < position[needed] < right:
                    answer += 1
        else:
            for second in range(middle + 1, right):
                needed = maximum - permutation[second]
                if 1 <= needed <= size and left <= position[needed] < middle:
                    answer += 1
        intervals.append((left, middle))
        intervals.append((middle + 1, right))
    return answer
```

Every counted pair lies on opposite sides of its unique maximum. Under
smaller-side enumeration, an index is inspected only logarithmically many times
across the recursive partition.

**Complexity:** `O(n log n)` time and `O(n)` space.
