# ICPC300 251: Codeforces 340E - Iahub and Permutations

**Source:** [Codeforces 340E - Iahub and Permutations](https://codeforces.com/problemset/problem/340/E)  
**Rating:** 2200  
**Pattern:** inclusion-exclusion over dangerous missing fixed points  
**Goal:** Complete a partial permutation so the final permutation has no fixed
point. The code uses zero-based values and `-1` for an unknown position.

## 1. First principles

Known values determine the missing values. Among unknown positions, only a
position whose own index is also missing can accidentally become a fixed point;
call these positions dangerous.

If there are `missing` slots and `dangerous` forbidden matches, inclusion-
exclusion gives

```text
sum over chosen:
    (-1)^chosen * C(dangerous, chosen) * (missing - chosen)!
```

## 2. Cases that decide correctness

- Known values must be distinct and in range.
- A known fixed point makes every completion invalid.
- An unknown position is dangerous only if its own value is still missing.
- Missing values may freely fill non-dangerous positions.
- The fully known valid permutation has exactly one completion.

## 3. Brute force: permute all missing values

```python
from itertools import permutations


MODULO = 1_000_000_007


def derangement_completion_count_brute(partial: list[int]) -> int:
    if not partial:
        raise ValueError("partial permutation must be nonempty")
    known = [value for value in partial if value != -1]
    if any(not 0 <= value < len(partial) for value in known) or len(set(known)) != len(
        known
    ):
        raise ValueError("known values must be distinct and in range")

    unknown_positions = [index for index, value in enumerate(partial) if value == -1]
    missing_values = sorted(set(range(len(partial))) - set(known))
    answer = 0
    for order in permutations(missing_values):
        completed = partial.copy()
        for index, value in zip(unknown_positions, order):
            completed[index] = value
        answer += all(index != value for index, value in enumerate(completed))
    return answer % MODULO
```

**Complexity:** `O(m! * n)` time and `O(n)` space for `m` missing values.

## 4. Better transition: isolate only possible new fixed points

The partial permutation already fixes the missing value set. Fixed-point
restrictions concern only intersections between that set and unknown position
indices, so inclusion-exclusion needs one parameter rather than a subset DP.

## 5. Expert solution: factorial inclusion-exclusion

```python
MODULO = 1_000_000_007


def derangement_completion_count(partial: list[int]) -> int:
    if not partial:
        raise ValueError("partial permutation must be nonempty")
    known = [value for value in partial if value != -1]
    if any(not 0 <= value < len(partial) for value in known) or len(set(known)) != len(
        known
    ):
        raise ValueError("known values must be distinct and in range")
    if any(value == index for index, value in enumerate(partial) if value != -1):
        return 0

    missing_values = set(range(len(partial))) - set(known)
    missing_count = partial.count(-1)
    dangerous = sum(
        value == -1 and index in missing_values for index, value in enumerate(partial)
    )

    factorial = [1] * (missing_count + 1)
    for value in range(1, missing_count + 1):
        factorial[value] = factorial[value - 1] * value % MODULO

    answer = 0
    combination = 1
    for chosen in range(dangerous + 1):
        term = combination * factorial[missing_count - chosen] % MODULO
        answer += term if chosen % 2 == 0 else -term
        if chosen < dangerous:
            combination = (
                combination * (dangerous - chosen) * pow(chosen + 1, MODULO - 2, MODULO)
            ) % MODULO
    return answer % MODULO
```

### Why the expert code is correct

Every completion is a bijection between missing values and unknown positions.
Forcing any chosen dangerous positions to be fixed leaves
`(missing-chosen)!` bijections. Inclusion-exclusion alternately removes and
restores completions containing forbidden fixed matches, leaving exactly the
derangements compatible with the known entries.

**Complexity:** `O(n + d log MODULO)` time and `O(n)` space for `d` dangerous
positions.

## 6. What to remember

```text
partial permutation -> missing positions and missing values
possible fixed point -> index belongs to both sets
avoid all dangerous matches -> inclusion-exclusion
```
