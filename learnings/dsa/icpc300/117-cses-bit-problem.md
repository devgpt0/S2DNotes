# ICPC300 117: CSES - Bit Problem

**Source:** [CSES - Bit Problem](https://cses.fi/problemset/task/1654/)  
**Pattern:** sum over subsets dynamic programming  
**Goal:** For every input value `x`, report in source order the number of input
values `y` satisfying `(x | y) == x`, `(x & y) == x`, and `(x & y) != 0`.

## 1. First principles

The first condition says that `y` is a submask of `x`. The second says that
`y` is a supermask of `x`. For the third condition, count its complement:
`x & y == 0` exactly when `y` is a submask of the complement of `x` inside
the chosen bit universe.

SOS DP computes all submask and supermask frequency sums at once.

## 2. Cases that decide correctness

- Repeated values are separate list entries and keep their multiplicity.
- Zero is a submask of every value but intersects no value nontrivially.
- A value is both its own submask and supermask.
- The complement is restricted to the bits needed by the maximum input.
- Input values must be nonnegative.

## 3. Brute force: test every ordered pair

```python
def bit_problem_brute(values: list[int]) -> list[tuple[int, int, int]]:
    if any(value < 0 for value in values):
        raise ValueError("values must be nonnegative")

    answers: list[tuple[int, int, int]] = []
    for value in values:
        submasks = sum(1 for other in values if value | other == value)
        supermasks = sum(1 for other in values if value & other == value)
        intersecting = sum(1 for other in values if value & other != 0)
        answers.append((submasks, supermasks, intersecting))
    return answers
```

**Complexity:** `O(n^2)` time and `O(n)` output space.

## 4. Better: enumerate each queried mask family

```python
def bit_problem_enumerate(values: list[int]) -> list[tuple[int, int, int]]:
    if any(value < 0 for value in values):
        raise ValueError("values must be nonnegative")
    bit_count = max(1, max(values, default=0).bit_length())
    full_mask = (1 << bit_count) - 1
    frequency = [0] * (full_mask + 1)
    for value in values:
        frequency[value] += 1

    def count_submasks(mask: int) -> int:
        total = 0
        submask = mask
        while True:
            total += frequency[submask]
            if submask == 0:
                return total
            submask = (submask - 1) & mask

    answers: list[tuple[int, int, int]] = []
    for value in values:
        submasks = count_submasks(value)
        missing = full_mask ^ value
        supermasks = 0
        addition = missing
        while True:
            supermasks += frequency[value | addition]
            if addition == 0:
                break
            addition = (addition - 1) & missing
        disjoint = count_submasks(missing)
        answers.append((submasks, supermasks, len(values) - disjoint))
    return answers
```

**Complexity:** `O(n * 2^b)` time in the worst case and `O(2^b)` space,
where `b` is the bit width.

## 5. Expert solution: submask and supermask SOS transforms

```python
def bit_problem_sos(values: list[int]) -> list[tuple[int, int, int]]:
    if any(value < 0 for value in values):
        raise ValueError("values must be nonnegative")
    bit_count = max(1, max(values, default=0).bit_length())
    universe_size = 1 << bit_count
    full_mask = universe_size - 1

    frequency = [0] * universe_size
    for value in values:
        frequency[value] += 1
    submask_count = frequency.copy()
    supermask_count = frequency.copy()

    for index in range(bit_count):
        bit = 1 << index
        for mask in range(universe_size):
            if mask & bit:
                submask_count[mask] += submask_count[mask ^ bit]
            else:
                supermask_count[mask] += supermask_count[mask | bit]

    return [
        (
            submask_count[value],
            supermask_count[value],
            len(values) - submask_count[full_mask ^ value],
        )
        for value in values
    ]
```

### Why the expert code is correct

After processing a bit, each SOS table has combined both choices for that bit.
After all bits, one table sums every submask and the other every supermask.
The submasks of `full_mask ^ x` are exactly the masks disjoint from `x`, so
subtracting their multiplicity gives the third answer.

**Complexity:** `O(n + b * 2^b)` time and `O(2^b)` space.

## 6. What to remember

```text
x | y == x -> y is a submask of x
x & y == x -> y is a supermask of x
x & y != 0 -> total minus submasks of complement(x)
```
