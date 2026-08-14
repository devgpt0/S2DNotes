# ICPC300 116: CSES - Increasing Subsequence II

**Source:** [CSES - Increasing Subsequence II](https://cses.fi/problemset/task/1748/)  
**Pattern:** Fenwick tree over compressed values  
**Goal:** Count the non-empty strictly increasing subsequences of an integer
array, modulo `1_000_000_007`.

## 1. First principles

Let `ways[i]` count increasing subsequences whose last chosen index is `i`.
The one-element subsequence always exists, and an earlier subsequence may be
extended exactly when its last value is smaller:

```text
ways[i] = 1 + sum(ways[j] for j < i and values[j] < values[i])
```

Only the sum by last value is needed. Coordinate compression preserves `<`,
and a Fenwick tree returns the sum over all smaller ranks.

## 2. Cases that decide correctness

- Equal values never extend one another because the subsequence is strict.
- Equal values at different indices still form distinct one-element choices.
- Negative and large values are handled by compression.
- The empty array has zero non-empty subsequences.
- Every addition is reduced modulo `1_000_000_007`.

## 3. Brute force: enumerate index subsets

```python
MODULO = 1_000_000_007


def increasing_subsequences_brute(values: list[int]) -> int:
    count = 0
    for mask in range(1, 1 << len(values)):
        chosen = [values[index] for index in range(len(values)) if mask & (1 << index)]
        if all(chosen[index - 1] < chosen[index] for index in range(1, len(chosen))):
            count += 1
    return count % MODULO
```

**Complexity:** `O(2^n * n)` time and `O(n)` space.

## 4. Better: quadratic dynamic programming

```python
MODULO = 1_000_000_007


def increasing_subsequences_quadratic(values: list[int]) -> int:
    ways = [1] * len(values)
    for end, value in enumerate(values):
        for previous in range(end):
            if values[previous] < value:
                ways[end] = (ways[end] + ways[previous]) % MODULO
    return sum(ways) % MODULO
```

**Complexity:** `O(n^2)` time and `O(n)` space.

## 5. Expert solution: compressed Fenwick tree

```python
MODULO = 1_000_000_007


def increasing_subsequences_fenwick(values: list[int]) -> int:
    ranks = {value: index + 1 for index, value in enumerate(sorted(set(values)))}
    tree = [0] * (len(ranks) + 1)

    def prefix_sum(index: int) -> int:
        total = 0
        while index > 0:
            total += tree[index]
            index -= index & -index
        return total % MODULO

    def add(index: int, amount: int) -> None:
        while index < len(tree):
            tree[index] = (tree[index] + amount) % MODULO
            index += index & -index

    answer = 0
    for value in values:
        rank = ranks[value]
        ways = (1 + prefix_sum(rank - 1)) % MODULO
        add(rank, ways)
        answer = (answer + ways) % MODULO
    return answer
```

### Why the expert code is correct

Before processing an index, the Fenwick tree contains exactly the counts for
subsequences ending at earlier indices. Querying `rank - 1` selects precisely
the smaller ending values, so the recurrence is evaluated once for every end
index. Summing those disjoint last-index classes counts every non-empty
increasing subsequence once.

**Complexity:** `O(n log n)` time and `O(n)` space.

## 6. What to remember

```text
count subsequences by final index
strict inequality -> query ranks strictly below the current rank
online prefix sums -> Fenwick tree
```
