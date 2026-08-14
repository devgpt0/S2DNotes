# 145. SUM and REPLACE — Codeforces 920F

**Source:** [Codeforces 920F - SUM and REPLACE](https://codeforces.com/problemset/problem/920/F)  
**Difficulty:** 2300

## 1. Problem in plain words

Maintain a positive-integer array under two operations: replace every value in `[left, right]` by its number of positive divisors, or print the range sum.

The functions use zero-based inclusive endpoints and operations `(1, left, right)` or `(2, left, right)`.

## 2. First principles

The divisor-count function rapidly shrinks every value, and `d(1)=1`, `d(2)=2`. Once a position reaches `1` or `2`, every future replacement leaves it unchanged.

An expert solution maintains range sums with a Fenwick tree and a successor disjoint-set structure that jumps over permanently stable positions.

## 3. Cases that define correctness

- Values `1` and `2` must never be revisited after stabilization.
- A replacement may stabilize only some positions in its interval.
- Sum queries must reflect every earlier point change.
- Source values are positive and at most `10⁶`.

## 4. Brute force

Visit every updated value and compute its divisor count by trial division.

```python
from math import isqrt


def sum_and_replace_brute_force(
    values: list[int], operations: list[tuple[int, int, int]]
) -> list[int]:
    if not values or any(not 1 <= value <= 10**6 for value in values):
        raise ValueError("source values must be in [1, 10^6]")

    def divisor_count(value: int) -> int:
        result = 0
        for divisor in range(1, isqrt(value) + 1):
            if value % divisor == 0:
                result += 1 if divisor * divisor == value else 2
        return result

    data = values.copy()
    answers: list[int] = []
    for kind, left, right in operations:
        if kind not in (1, 2) or not 0 <= left <= right < len(data):
            raise ValueError("invalid operation")
        if kind == 1:
            for index in range(left, right + 1):
                data[index] = divisor_count(data[index])
        else:
            answers.append(sum(data[left : right + 1]))
    return answers
```

Worst-case time is `O(qn sqrt(A))`, where `A` is the largest value, and space is `O(n)`.

## 5. Better approach: stable-aware blocks

Square-root blocks store sums and maximums. A full block with maximum at most `2` is already stable and can be skipped during replacement; full-block sums answer queries quickly.

```python
from math import isqrt


def sum_and_replace_blocks(
    values: list[int], operations: list[tuple[int, int, int]]
) -> list[int]:
    if not values or any(not 1 <= value <= 10**6 for value in values):
        raise ValueError("source values must be in [1, 10^6]")

    maximum = max(values)
    divisors = [0] * (maximum + 1)
    for divisor in range(1, maximum + 1):
        for multiple in range(divisor, maximum + 1, divisor):
            divisors[multiple] += 1

    size = len(values)
    block_size = isqrt(size) + 1
    block_count = (size + block_size - 1) // block_size
    data = values.copy()
    block_sum = [0] * block_count
    block_max = [0] * block_count

    def rebuild(block: int) -> None:
        left = block * block_size
        right = min(size, left + block_size)
        block_sum[block] = sum(data[left:right])
        block_max[block] = max(data[left:right], default=0)

    for block in range(block_count):
        rebuild(block)

    answers: list[int] = []
    for kind, left, right in operations:
        if kind not in (1, 2) or not 0 <= left <= right < size:
            raise ValueError("invalid operation")
        if kind == 1:
            first_block = left // block_size
            last_block = right // block_size
            for block in range(first_block, last_block + 1):
                if block_max[block] <= 2:
                    continue
                start = max(left, block * block_size)
                end = min(right + 1, (block + 1) * block_size)
                for index in range(start, end):
                    data[index] = divisors[data[index]]
                rebuild(block)
        else:
            answer = 0
            index = left
            while index <= right and index % block_size:
                answer += data[index]
                index += 1
            while index + block_size - 1 <= right:
                answer += block_sum[index // block_size]
                index += block_size
            while index <= right:
                answer += data[index]
                index += 1
            answers.append(answer)
    return answers
```

Queries cost `O(sqrt(n))`; replacements skip stable blocks and use `O(n)` space.

## 6. Expert solution: successor DSU plus Fenwick tree

The successor structure returns the first not-yet-stable index at or after a position. Once a value becomes at most `2`, link its index to its successor. Fenwick point updates keep sums current.

```python
def sum_and_replace(
    values: list[int], operations: list[tuple[int, int, int]]
) -> list[int]:
    if not values or any(not 1 <= value <= 10**6 for value in values):
        raise ValueError("source values must be in [1, 10^6]")

    maximum = max(values)
    smallest_prime = list(range(maximum + 1))
    for prime in range(2, int(maximum**0.5) + 1):
        if smallest_prime[prime] != prime:
            continue
        for multiple in range(prime * prime, maximum + 1, prime):
            if smallest_prime[multiple] == multiple:
                smallest_prime[multiple] = prime

    divisors = [0] * (maximum + 1)
    divisors[1] = 1
    for value in range(2, maximum + 1):
        prime = smallest_prime[value]
        remaining = value
        exponent = 0
        while remaining % prime == 0:
            remaining //= prime
            exponent += 1
        divisors[value] = divisors[remaining] * (exponent + 1)

    size = len(values)
    data = values.copy()
    fenwick = [0, *data]
    for index in range(1, size + 1):
        parent = index + (index & -index)
        if parent <= size:
            fenwick[parent] += fenwick[index]

    def add(position: int, delta: int) -> None:
        index = position + 1
        while index <= size:
            fenwick[index] += delta
            index += index & -index

    def prefix(position: int) -> int:
        result = 0
        index = position + 1
        while index > 0:
            result += fenwick[index]
            index -= index & -index
        return result

    successor = list(range(size + 1))

    def find(position: int) -> int:
        root = position
        while successor[root] != root:
            root = successor[root]
        while successor[position] != position:
            next_position = successor[position]
            successor[position] = root
            position = next_position
        return root

    for index in range(size - 1, -1, -1):
        if data[index] <= 2:
            successor[index] = find(index + 1)

    answers: list[int] = []
    for kind, left, right in operations:
        if kind not in (1, 2) or not 0 <= left <= right < size:
            raise ValueError("invalid operation")
        if kind == 1:
            index = find(left)
            while index <= right:
                updated = divisors[data[index]]
                add(index, updated - data[index])
                data[index] = updated
                if updated <= 2:
                    successor[index] = find(index + 1)
                index = find(index + 1)
        else:
            answers.append(prefix(right) - (prefix(left - 1) if left else 0))
    return answers
```

## 7. Why the expert solution is correct

Fenwick values always equal the current array because each replacement applies the exact point difference. The successor DSU removes only positions where all future replacements are identity, so skipping them cannot change a result. Every non-stable position in the requested interval is visited and updated exactly once for that operation.

Each value changes only a small bounded number of times before reaching `1` or `2`. Total time is `O((n + q + U) log n + A log A)`, where `U` is the number of actual value changes; space is `O(n + A)`.
