# ICPC300 004: Codeforces 86D - Powerful Array

**Source:** [Codeforces 86D - Powerful Array](https://codeforces.com/problemset/problem/86/D)  
**Pattern:** Mo's algorithm  
**Goal:** For each inclusive range, compute
`sum(value * frequency(value)^2)`.

The implementations use zero-based query indices.

## 1. First principles

Recomputing every frequency for every query wastes overlapping work. Mo's
algorithm reorders static range queries so one boundary moves at a time.

If value `x` currently appears `c` times, adding one occurrence changes only
its contribution:

```text
x(c + 1)^2 - xc^2 = x(2c + 1)
```

Removing one occurrence changes it by `x(1 - 2c)`. Both updates are `O(1)`.

## 2. Cases that decide correctness

| Case | Required behavior |
| --- | --- |
| One element `x` | Power is `x`. |
| All values equal | For length `k`, power is `x * k^2`. |
| Boundary moves left | Add/remove the same way as a right-boundary move. |
| Queries arrive unsorted | Store each answer at its original index. |
| Large answer | Use integer arithmetic wide enough for the source limit. |

## 3. Brute force: follow the formula directly

For each distinct value in a query, scan the range again to count it. This is
slow but makes a transparent small-input oracle.

```python
def powerful_array_brute(
    values: list[int], queries: list[tuple[int, int]]
) -> list[int]:
    answers: list[int] = []

    for left, right in queries:
        processed: set[int] = set()
        power = 0
        for index in range(left, right + 1):
            value = values[index]
            if value in processed:
                continue

            frequency = 0
            for candidate_index in range(left, right + 1):
                if values[candidate_index] == value:
                    frequency += 1

            power += value * frequency * frequency
            processed.add(value)
        answers.append(power)

    return answers
```

**Complexity:** `O(qn^2)` worst-case time and `O(n)` temporary space.

## 4. Better: count each query in one pass

Build one frequency table per query, then evaluate the formula once per
distinct value.

```python
from collections import Counter


def powerful_array_counting(
    values: list[int], queries: list[tuple[int, int]]
) -> list[int]:
    answers: list[int] = []

    for left, right in queries:
        frequencies = Counter(values[left : right + 1])
        answers.append(
            sum(
                value * frequency * frequency
                for value, frequency in frequencies.items()
            )
        )

    return answers
```

**Complexity:** `O(total queried length)` time and `O(n)` temporary space;
worst case `O(nq)` time.

## 5. Expert solution: Mo's algorithm

Split left endpoints into blocks and sort by block. Reverse the right-endpoint
order in alternating blocks to avoid repeatedly sweeping back across the
array.

```python
from math import isqrt


def powerful_array_mo(values: list[int], queries: list[tuple[int, int]]) -> list[int]:
    if not values:
        if queries:
            raise ValueError("queries require at least one value")
        return []

    block_size = max(1, isqrt(len(values)))

    def query_key(query_index: int) -> tuple[int, int]:
        left, right = queries[query_index]
        block = left // block_size
        ordered_right = right if block % 2 == 0 else -right
        return block, ordered_right

    order = sorted(range(len(queries)), key=query_key)
    answers = [0] * len(queries)
    frequencies: dict[int, int] = {}
    current_power = 0
    current_left = 0
    current_right = -1

    def add(index: int) -> None:
        nonlocal current_power
        value = values[index]
        frequency = frequencies.get(value, 0)
        current_power += value * (2 * frequency + 1)
        frequencies[value] = frequency + 1

    def remove(index: int) -> None:
        nonlocal current_power
        value = values[index]
        frequency = frequencies[value]
        current_power += value * (1 - 2 * frequency)
        if frequency == 1:
            del frequencies[value]
        else:
            frequencies[value] = frequency - 1

    for query_index in order:
        left, right = queries[query_index]
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
        answers[query_index] = current_power

    return answers
```

### Why the expert code is correct

- The maintained frequency table describes exactly the current inclusive
  window.
- `add` and `remove` replace one value's old contribution with its new one,
  leaving every other contribution unchanged.
- Boundary moves transform the current window into each requested range, so
  the stored power is that query's exact formula value.

**Complexity:** `O((n + q) sqrt(n) + q log q)` time and `O(n + q)` space.

## 6. What to remember

```text
static offline ranges + cheap add/remove -> consider Mo's algorithm
add x at old count c    -> answer += x(2c + 1)
remove x at old count c -> answer += x(1 - 2c)
```
