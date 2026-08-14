# Focus300 075: LeetCode 493 - Reverse Pairs

**Source:** [LeetCode 493](https://leetcode.com/problems/reverse-pairs/)  
**Difficulty:** Hard  
**Pattern:** cross-half counting during merge sort

## Exact contract

Given a nonempty integer array, return the number of pairs `(i, j)` with
`i < j` and `numbers[i] > 2 * numbers[j]`. The inequality is strict and must be
evaluated without 32-bit overflow assumptions.

## First principles

After sorting the left and right halves, a right pointer only moves forward as
left values increase. For each left value, every right value before that pointer
forms a reverse pair. Count cross pairs before merging the halves.

## Cases that decide correctness

- Equality `left == 2 * right` does not count.
- Negative values can form reverse pairs.
- Equal values at different indices remain separate elements.
- Pair order is the original index order, not sorted order.
- Python integers avoid multiplication overflow.

## Brute force: test every ordered index pair

```python
def reverse_pairs_brute(numbers: list[int]) -> int:
    if not numbers:
        raise ValueError("numbers must be nonempty")
    return sum(
        numbers[first] > 2 * numbers[second]
        for first in range(len(numbers))
        for second in range(first + 1, len(numbers))
    )
```

This takes `O(n^2)` time and `O(1)` auxiliary space.

## Better approach: compressed Fenwick frequencies

```python
from bisect import bisect_left, bisect_right


def reverse_pairs_fenwick(numbers: list[int]) -> int:
    if not numbers:
        raise ValueError("numbers must be nonempty")

    coordinates = sorted(set(numbers))
    tree = [0] * (len(coordinates) + 1)

    def add(index: int) -> None:
        index += 1
        while index < len(tree):
            tree[index] += 1
            index += index & -index

    def prefix(length: int) -> int:
        answer = 0
        while length:
            answer += tree[length]
            length -= length & -length
        return answer

    answer = 0
    for index, number in enumerate(numbers):
        not_greater = prefix(bisect_right(coordinates, 2 * number))
        answer += index - not_greater
        add(bisect_left(coordinates, number))
    return answer
```

The tree stores earlier values; subtracting those at most `2 * number` leaves
exactly the required greater values.

## Expert solution: merge-sort cross counting

```python
def reverse_pairs(numbers: list[int]) -> int:
    if not numbers:
        raise ValueError("numbers must be nonempty")

    values = numbers.copy()

    def sort_count(left: int, right: int) -> int:
        if right - left <= 1:
            return 0
        middle = (left + right) // 2
        answer = sort_count(left, middle) + sort_count(middle, right)
        second = middle
        for first in range(left, middle):
            while second < right and values[first] > 2 * values[second]:
                second += 1
            answer += second - middle

        merged: list[int] = []
        first = left
        second = middle
        while first < middle and second < right:
            if values[first] <= values[second]:
                merged.append(values[first])
                first += 1
            else:
                merged.append(values[second])
                second += 1
        merged.extend(values[first:middle])
        merged.extend(values[second:right])
        values[left:right] = merged
        return answer

    return sort_count(0, len(values))
```

Recursive calls count pairs inside each half. Monotonic scanning counts each
cross-half pair once under the strict inequality, after which merging restores
the sorted invariant required by parent calls.

**Complexity:** `O(n log n)` time and `O(n)` merge space.
