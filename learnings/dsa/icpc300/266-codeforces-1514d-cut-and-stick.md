# ICPC300 266: Codeforces 1514D - Cut and Stick

**Source:** [Codeforces 1514D - Cut and Stick](https://codeforces.com/problemset/problem/1514/D)  
**Rating:** 2200  
**Pattern:** range majority candidate plus indexed occurrence counts  
**Goal:** For each queried multiset, return its minimum cut-and-stick score.
Equivalently, reorder its values to minimize one plus the number of adjacent
equal pairs.

## 1. First principles

Let the range length be `length` and its maximum frequency be `frequency`.
Values other than the most frequent one can separate at most that many pairs
of its copies. The unavoidable score is

```text
max(1, frequency - (length - frequency))
= max(1, 2 * frequency - length).
```

Only a strict majority can make this exceed one. A Boyer-Moore segment tree
finds the only possible majority candidate; sorted position lists verify its
actual frequency.

## 2. Cases that decide correctness

- A one-element range has answer one.
- If no value is a strict majority, the answer is one.
- A candidate balance is not a frequency and must be verified.
- Query endpoints are inclusive in the public function.
- Values need not be small or consecutive.

## 3. Brute force: enumerate all reorderings

```python
from itertools import permutations


def cut_and_stick_brute(
    values: list[int],
    queries: list[tuple[int, int]],
) -> list[int]:
    if not values or any(type(value) is not int for value in values):
        raise ValueError("values must be integers")
    answers = []
    for left, right in queries:
        if (
            type(left) is not int
            or type(right) is not int
            or not 0 <= left <= right < len(values)
        ):
            raise ValueError("invalid query")
        best = right - left + 1
        for order in permutations(values[left : right + 1]):
            score = 1 + sum(
                order[index] == order[index + 1] for index in range(len(order) - 1)
            )
            best = min(best, score)
            if best == 1:
                break
        answers.append(best)
    return answers
```

**Complexity:** `O(q L! L)` time for maximum queried length `L`.

## 4. Better approach: count every value in each query

A frequency dictionary per range gives the formula directly in `O(L)` time.
It is adequate for short queries but repeats almost all work across overlapping
ranges.

## 5. Expert solution: cancellation tree and binary searches

```python
from bisect import bisect_left, bisect_right


Vote = tuple[int | None, int]


def cut_and_stick_scores(
    values: list[int],
    queries: list[tuple[int, int]],
) -> list[int]:
    if not values or any(type(value) is not int for value in values):
        raise ValueError("values must be integers")

    def merge(first: Vote, second: Vote) -> Vote:
        first_value, first_balance = first
        second_value, second_balance = second
        if first_balance == 0:
            return second
        if second_balance == 0:
            return first
        if first_value == second_value:
            return first_value, first_balance + second_balance
        if first_balance > second_balance:
            return first_value, first_balance - second_balance
        return second_value, second_balance - first_balance

    leaf_count = 1
    while leaf_count < len(values):
        leaf_count *= 2
    tree: list[Vote] = [(None, 0)] * (2 * leaf_count)
    positions: dict[int, list[int]] = {}
    for index, value in enumerate(values):
        tree[leaf_count + index] = (value, 1)
        positions.setdefault(value, []).append(index)
    for index in range(leaf_count - 1, 0, -1):
        tree[index] = merge(tree[2 * index], tree[2 * index + 1])

    answers = []
    for query_left, query_right in queries:
        if (
            type(query_left) is not int
            or type(query_right) is not int
            or not 0 <= query_left <= query_right < len(values)
        ):
            raise ValueError("invalid query")
        left = query_left + leaf_count
        right = query_right + 1 + leaf_count
        left_vote: Vote = (None, 0)
        right_vote: Vote = (None, 0)
        while left < right:
            if left & 1:
                left_vote = merge(left_vote, tree[left])
                left += 1
            if right & 1:
                right -= 1
                right_vote = merge(tree[right], right_vote)
            left //= 2
            right //= 2
        candidate, _ = merge(left_vote, right_vote)
        frequency = 0
        if candidate is not None:
            indices = positions[candidate]
            frequency = bisect_right(indices, query_right) - bisect_left(
                indices, query_left
            )
        length = query_right - query_left + 1
        answers.append(max(1, 2 * frequency - length))
    return answers
```

### Why the expert code is correct

Pairwise cancellation preserves any strict majority, so each range query
returns its only possible candidate. Binary searches recover the true count.
Minority values can separate dominant copies until either all equal
adjacencies disappear or their supply is exhausted, proving the score formula.

**Complexity:** `O((n + q) log n)` time and `O(n)` space.

## 6. What to remember

```text
answer above one -> strict majority exists
segment-tree cancellation -> candidate only
position lists -> exact range frequency
```
