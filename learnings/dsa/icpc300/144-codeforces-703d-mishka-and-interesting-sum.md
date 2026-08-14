# 144. Mishka and Interesting sum — Codeforces 703D

**Source:** [Codeforces 703D - Mishka and Interesting sum](https://codeforces.com/problemset/problem/703/D)  
**Difficulty:** 2200

## 1. Problem in plain words

For each subarray, XOR the distinct values whose frequency in that subarray is positive and even. Print that “interesting sum.”

The functions use zero-based inclusive endpoints.

## 2. First principles

XOR of every occurrence keeps exactly values with odd frequency. XOR of every distinct present value keeps all values with positive frequency. XOR those two results together: odd-frequency values cancel, leaving exactly positive even-frequency values.

Offline by right endpoint, a Fenwick tree can hold each value only at its latest occurrence. Its range XOR is therefore the distinct-value XOR.

## 3. Cases that define correctness

- A value occurring twice contributes once, not twice.
- A value occurring zero times is absent from both XORs.
- A single occurrence cancels between occurrence XOR and distinct XOR.
- Equal values at old positions must be disabled when a new latest occurrence arrives.

## 4. Brute force

Count every query interval and XOR values with positive even counts.

```python
from collections import Counter


def interesting_sums_brute_force(
    values: list[int], queries: list[tuple[int, int]]
) -> list[int]:
    if any(value < 0 for value in values):
        raise ValueError("values must be nonnegative")

    answers: list[int] = []
    for left, right in queries:
        if not 0 <= left <= right < len(values):
            raise ValueError("invalid query")
        counts = Counter(values[left : right + 1])
        answer = 0
        for value, count in counts.items():
            if count % 2 == 0:
                answer ^= value
        answers.append(answer)
    return answers
```

Worst-case time is `O(nq)` and temporary space is `O(n)`.

## 5. Better approach: Mo's algorithm

Maintain both the XOR of all occurrences and the XOR of distinct present values. Their XOR is the answer.

```python
from math import isqrt


def interesting_sums_mo(values: list[int], queries: list[tuple[int, int]]) -> list[int]:
    if any(value < 0 for value in values):
        raise ValueError("values must be nonnegative")

    size = len(values)
    block_size = isqrt(size) + 1
    ordered: list[tuple[int, int, int]] = []
    for index, (left, right) in enumerate(queries):
        if not 0 <= left <= right < size:
            raise ValueError("invalid query")
        ordered.append((left, right, index))
    ordered.sort(
        key=lambda item: (
            item[0] // block_size,
            item[1] if item[0] // block_size % 2 == 0 else -item[1],
        )
    )

    frequency: dict[int, int] = {}
    occurrence_xor = 0
    distinct_xor = 0

    def change(position: int, delta: int) -> None:
        nonlocal occurrence_xor, distinct_xor
        value = values[position]
        old = frequency.get(value, 0)
        occurrence_xor ^= value
        new = old + delta
        if old == 0 or new == 0:
            distinct_xor ^= value
        if new == 0:
            frequency.pop(value)
        else:
            frequency[value] = new

    answers = [0] * len(queries)
    current_left = 0
    current_right = -1
    for left, right, query_index in ordered:
        while current_left > left:
            current_left -= 1
            change(current_left, 1)
        while current_right < right:
            current_right += 1
            change(current_right, 1)
        while current_left < left:
            change(current_left, -1)
            current_left += 1
        while current_right > right:
            change(current_right, -1)
            current_right -= 1
        answers[query_index] = occurrence_xor ^ distinct_xor
    return answers
```

The standard Mo bound is `O((n + q) sqrt(n))` updates and `O(n + q)` space.

## 6. Expert solution: latest-occurrence XOR Fenwick tree

Sort queries by right endpoint. Toggle a value out at its old latest position and into its new one. A Fenwick range XOR then contains every distinct query value exactly once.

```python
def interesting_sums(values: list[int], queries: list[tuple[int, int]]) -> list[int]:
    if any(value < 0 for value in values):
        raise ValueError("values must be nonnegative")

    size = len(values)
    ordered: list[tuple[int, int, int]] = []
    for index, (left, right) in enumerate(queries):
        if not 0 <= left <= right < size:
            raise ValueError("invalid query")
        ordered.append((right, left, index))
    ordered.sort()

    prefix_xor = [0]
    for value in values:
        prefix_xor.append(prefix_xor[-1] ^ value)

    fenwick = [0] * (size + 1)

    def toggle(position: int, value: int) -> None:
        index = position + 1
        while index <= size:
            fenwick[index] ^= value
            index += index & -index

    def prefix(position: int) -> int:
        result = 0
        index = position + 1
        while index > 0:
            result ^= fenwick[index]
            index -= index & -index
        return result

    answers = [0] * len(queries)
    last_position: dict[int, int] = {}
    query_pointer = 0
    for right, value in enumerate(values):
        previous = last_position.get(value)
        if previous is not None:
            toggle(previous, value)
        toggle(right, value)
        last_position[value] = right

        while query_pointer < len(ordered) and ordered[query_pointer][0] == right:
            _, left, query_index = ordered[query_pointer]
            distinct_xor = prefix(right) ^ (prefix(left - 1) if left else 0)
            occurrence_xor = prefix_xor[right + 1] ^ prefix_xor[left]
            answers[query_index] = distinct_xor ^ occurrence_xor
            query_pointer += 1
    return answers
```

## 7. Why the expert solution is correct

At a processed right endpoint, the Fenwick tree stores each seen value at exactly its latest position. Such a position lies in `[left, right]` exactly when the value occurs in that interval, so the range XOR is the distinct-value XOR. XORing it with the ordinary occurrence XOR cancels precisely odd-frequency values and leaves positive even-frequency values.

Time is `O((n + q) log n)` and space is `O(n + q)`.
