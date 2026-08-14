# 143. XOR and Favorite Number — Codeforces 617E

**Source:** [Codeforces 617E - XOR and Favorite Number](https://codeforces.com/problemset/problem/617/E)  
**Difficulty:** 2200

## 1. Problem in plain words

For each query `[left, right]`, count subarrays completely inside that interval whose XOR equals a fixed favorite number `k`.

The functions use zero-based inclusive endpoints.

## 2. First principles

Let `prefix[i]` be the XOR of the first `i` values. Subarray `[i, j-1]` has XOR `k` exactly when `prefix[i] XOR prefix[j] = k`.

Thus array query `[l, r]` becomes a pair-count query over prefix indices `[l, r+1]`. Mo's algorithm maintains that prefix window. Adding prefix value `x` creates one pair with every existing `x XOR k`.

## 3. Cases that define correctness

- The prefix before `left` must be included.
- When `k = 0`, equal prefix values form valid pairs.
- Pair count can exceed 32 bits.
- Query answers must return to original order after Mo sorting.

## 4. Brute force

Start every subarray inside every query and extend its XOR.

```python
def favorite_xor_counts_brute_force(
    values: list[int], favorite: int, queries: list[tuple[int, int]]
) -> list[int]:
    if any(value < 0 for value in values) or favorite < 0:
        raise ValueError("values and favorite must be nonnegative")

    answers: list[int] = []
    for left, right in queries:
        if not 0 <= left <= right < len(values):
            raise ValueError("invalid query")
        answer = 0
        for start in range(left, right + 1):
            current = 0
            for end in range(start, right + 1):
                current ^= values[end]
                answer += current == favorite
        answers.append(answer)
    return answers
```

Worst-case time is `O(qn²)` and auxiliary space is `O(1)`.

## 5. Better approach: one prefix-frequency scan per query

Scan the query once. Before consuming the next prefix XOR `x`, all earlier matching prefixes have value `x XOR k`.

```python
def favorite_xor_counts_linear(
    values: list[int], favorite: int, queries: list[tuple[int, int]]
) -> list[int]:
    if any(value < 0 for value in values) or favorite < 0:
        raise ValueError("values and favorite must be nonnegative")

    answers: list[int] = []
    for left, right in queries:
        if not 0 <= left <= right < len(values):
            raise ValueError("invalid query")
        frequency = {0: 1}
        current = 0
        answer = 0
        for index in range(left, right + 1):
            current ^= values[index]
            answer += frequency.get(current ^ favorite, 0)
            frequency[current] = frequency.get(current, 0) + 1
        answers.append(answer)
    return answers
```

Time is `O(total queried length)`—`O(nq)` worst case—and space is `O(n)`.

## 6. Expert solution: Mo's algorithm on prefix XOR

Convert each query to a prefix interval. Maintain a frequency map and the number of matching unordered pairs while moving the window.

```python
from math import isqrt


def favorite_xor_counts(
    values: list[int], favorite: int, queries: list[tuple[int, int]]
) -> list[int]:
    if any(value < 0 for value in values) or favorite < 0:
        raise ValueError("values and favorite must be nonnegative")

    prefix = [0]
    for value in values:
        prefix.append(prefix[-1] ^ value)

    block_size = isqrt(len(prefix)) + 1
    ordered: list[tuple[int, int, int]] = []
    for index, (left, right) in enumerate(queries):
        if not 0 <= left <= right < len(values):
            raise ValueError("invalid query")
        prefix_right = right + 1
        ordered.append((left, prefix_right, index))
    ordered.sort(
        key=lambda item: (
            item[0] // block_size,
            item[1] if item[0] // block_size % 2 == 0 else -item[1],
        )
    )

    frequency: dict[int, int] = {}
    pair_count = 0

    def add(position: int) -> None:
        nonlocal pair_count
        value = prefix[position]
        pair_count += frequency.get(value ^ favorite, 0)
        frequency[value] = frequency.get(value, 0) + 1

    def remove(position: int) -> None:
        nonlocal pair_count
        value = prefix[position]
        frequency[value] -= 1
        pair_count -= frequency.get(value ^ favorite, 0)
        if frequency[value] == 0:
            del frequency[value]

    answers = [0] * len(queries)
    current_left = 0
    current_right = -1
    for left, right, query_index in ordered:
        while current_left > left:
            current_left -= 1
            add(current_left)
        while current_right < right:
            current_right += 1
            add(current_right)
        while current_left < left:
            remove(current_left)
            current_left += 1
        while current_right > right:
            remove(current_right)
            current_right -= 1
        answers[query_index] = pair_count
    return answers
```

## 7. Why the expert solution is correct

Every wanted subarray corresponds bijectively to two prefix indices in the converted interval whose XOR is `k`. When adding `x`, all existing `x XOR k` values create exactly the new pairs involving `x`; removal reverses that update. Therefore the maintained count equals the query answer for every Mo window.

The standard Mo bound is `O((n + q) sqrt(n))` dictionary updates and `O(n + q)` space.
