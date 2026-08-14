# ICPC300 003: CSES - Distinct Values Queries

**Source:** [CSES - Distinct Values Queries](https://cses.fi/problemset/task/1734/)  
**Pattern:** offline queries + Fenwick tree  
**Goal:** For every inclusive range `[left, right]`, count how many different
values it contains.

The implementations use zero-based query indices.

## 1. First principles

For a fixed right endpoint, keep a `1` only at the latest occurrence of each
value in the prefix. Older occurrences hold `0`.

Every value present in `[left, right]` then contributes exactly one active
position to that range. Process queries in increasing `right` order and use a
Fenwick tree to sum those active positions.

```text
values:          3  2  3  1  2
latest markers:  0  0  1  1  1   after reaching right = 4

query [1, 4] -> marker sum = 3 -> values {1, 2, 3}
```

## 2. Cases that decide correctness

| Case | Required behavior |
| --- | --- |
| All values equal | Every non-empty query returns `1`. |
| All values distinct | A query returns its length. |
| Repeated value before `left` | Its latest occurrence inside the range still contributes once. |
| One-element range | Return `1`. |
| Queries arrive unsorted | Preserve their original output order. |

## 3. Brute force: build a set per query

This direct implementation is the best small-input oracle.

```python
def distinct_values_brute(
    values: list[int], queries: list[tuple[int, int]]
) -> list[int]:
    return [len(set(values[left : right + 1])) for left, right in queries]
```

**Why it works:** a set keeps one representative of every different value in
the requested slice.

**Complexity:** `O(total queried length)` time, `O(n)` temporary space; worst
case `O(nq)` time.

## 4. Better: Mo's algorithm

Order ranges so consecutive queries move their boundaries only a little.
Maintain frequencies and the current number of nonzero frequencies.

```python
from math import isqrt


def distinct_values_mo(values: list[int], queries: list[tuple[int, int]]) -> list[int]:
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
    distinct_count = 0
    current_left = 0
    current_right = -1

    def add(index: int) -> None:
        nonlocal distinct_count
        value = values[index]
        old_count = frequencies.get(value, 0)
        frequencies[value] = old_count + 1
        if old_count == 0:
            distinct_count += 1

    def remove(index: int) -> None:
        nonlocal distinct_count
        value = values[index]
        new_count = frequencies[value] - 1
        if new_count == 0:
            del frequencies[value]
            distinct_count -= 1
        else:
            frequencies[value] = new_count

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
        answers[query_index] = distinct_count

    return answers
```

**Complexity:** about `O((n + q) sqrt(n))` boundary moves and `O(n)` frequency
space.

## 5. Expert solution: right-endpoint sweep

When position `i` is read, deactivate the previous occurrence of `values[i]`
and activate `i`. The Fenwick tree always represents latest occurrences in the
processed prefix.

```python
def distinct_values_fenwick(
    values: list[int], queries: list[tuple[int, int]]
) -> list[int]:
    if not values:
        if queries:
            raise ValueError("queries require at least one value")
        return []

    tree = [0] * (len(values) + 1)

    def add(index: int, difference: int) -> None:
        while index < len(tree):
            tree[index] += difference
            index += index & -index

    def prefix_sum(end: int) -> int:
        total = 0
        while end > 0:
            total += tree[end]
            end -= end & -end
        return total

    indexed_queries = sorted(enumerate(queries), key=lambda item: item[1][1])
    answers = [0] * len(queries)
    last_position: dict[int, int] = {}
    current_right = -1

    for query_index, (left, right) in indexed_queries:
        while current_right < right:
            current_right += 1
            value = values[current_right]
            previous = last_position.get(value)
            if previous is not None:
                add(previous + 1, -1)
            add(current_right + 1, 1)
            last_position[value] = current_right

        answers[query_index] = prefix_sum(right + 1) - prefix_sum(left)

    return answers
```

### Why the expert code is correct

- After processing `right`, exactly one marker exists for each value in
  `values[0:right + 1]`, at that value's latest position.
- A value occurs in `[left, right]` exactly when its latest position is at
  least `left`.
- Therefore the marker sum over `[left, right]` equals the distinct count.

**Complexity:** `O((n + q) log n)` time and `O(n)` space.

## 6. What to remember

```text
sort queries by right endpoint
move each value's marker: previous position -> 0, current position -> 1
Fenwick sum(left, right) = number of distinct values
```
