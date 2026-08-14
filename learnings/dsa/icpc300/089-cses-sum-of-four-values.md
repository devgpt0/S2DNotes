# ICPC300 089: CSES - Sum of Four Values

**Source:** [CSES - Sum of Four Values](https://cses.fi/problemset/task/1642/)  
**Pattern:** incremental pair-sum lookup  
**Goal:** Return four distinct zero-based indices whose values sum to the
target, or `None` if no such indices exist.

## 1. First principles

Rewrite the equation as two pair sums:

```text
values[a] + values[b] = target - values[c] - values[d]
```

Before querying pair `(c,d)`, store only pairs ending before `c`. Any match then
has four distinct indices by construction, without expensive overlap checks.

## 2. Cases that decide correctness

- Equal values at different indices are allowed.
- One index may never be reused.
- Negative values and targets are valid.
- Any valid quadruple is acceptable.
- Fewer than four values returns `None`.

## 3. Brute force: enumerate quadruples

```python
from itertools import combinations


def sum_of_four_values_brute(
    values: list[int], target: int
) -> tuple[int, int, int, int] | None:
    for indices in combinations(range(len(values)), 4):
        if sum(values[index] for index in indices) == target:
            return indices
    return None
```

**Complexity:** `O(n^4)` time and `O(1)` auxiliary space.

## 4. Better: fix two indices and solve a two-sum suffix

```python
def sum_of_four_values_cubic(
    values: list[int], target: int
) -> tuple[int, int, int, int] | None:
    for first in range(len(values)):
        for second in range(first + 1, len(values)):
            seen: dict[int, int] = {}
            for fourth in range(second + 1, len(values)):
                needed = target - values[first] - values[second] - values[fourth]
                third = seen.get(needed)
                if third is not None:
                    return first, second, third, fourth
                seen[values[fourth]] = fourth
    return None
```

**Complexity:** `O(n^3)` time and `O(n)` space.

## 5. Expert solution: incremental pair sums

Query pairs starting at `third` against earlier disjoint pairs, then insert all
pairs ending at `third` for future iterations.

```python
def sum_of_four_values_pairs(
    values: list[int], target: int
) -> tuple[int, int, int, int] | None:
    pair_by_sum: dict[int, tuple[int, int]] = {}

    for third in range(len(values)):
        for fourth in range(third + 1, len(values)):
            needed = target - values[third] - values[fourth]
            earlier_pair = pair_by_sum.get(needed)
            if earlier_pair is not None:
                return earlier_pair[0], earlier_pair[1], third, fourth

        for first in range(third):
            pair_by_sum[values[first] + values[third]] = first, third
    return None
```

### Why the expert code is correct

When `(third, fourth)` is queried, every stored pair ends before `third`, so a
sum match is valid and disjoint. Every ordered quadruple `a<b<c<d` is considered
when the loop reaches `c`, proving completeness.

**Complexity:** `O(n^2)` expected time and `O(n^2)` space.

## 6. What to remember

```text
four-sum -> pair sum + complementary pair sum
store only pairs completely before the queried pair
index ordering guarantees distinctness
```
