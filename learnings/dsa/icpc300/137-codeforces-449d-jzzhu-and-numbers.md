# 137. Jzzhu and Numbers — Codeforces 449D

**Source:** [Codeforces 449D - Jzzhu and Numbers](https://codeforces.com/problemset/problem/449/D)  
**Difficulty:** 2200

## 1. Problem in plain words

Count the nonempty subsequences whose bitwise AND is zero. Equal values at different positions are different choices. Every source value is in `[0, 2²⁰)`. Print the count modulo `1_000_000_007`.

## 2. First principles

For a bit mask `mask`, let `superset_count[mask]` be the number of array values containing every bit of `mask`. Any nonempty subsequence chosen only from those values has an AND containing `mask`, so there are `2^superset_count[mask] - 1` such subsequences.

Inclusion-exclusion over the 20 bits leaves exactly subsequences whose AND contains none of them, which means AND zero. A superset zeta transform computes every `superset_count` together.

## 3. Cases that define correctness

- A zero element alone is a valid subsequence.
- Duplicate values represent independent positions.
- The empty subsequence must be excluded from every power-of-two count.
- Values use exactly the low 20 bits in the source domain.

## 4. Brute force

Enumerate every nonempty set of positions and compute its AND.

```python
MODULO = 1_000_000_007
BIT_COUNT = 20


def count_zero_and_subsequences_brute_force(values: list[int]) -> int:
    limit = 1 << BIT_COUNT
    if any(not 0 <= value < limit for value in values):
        raise ValueError("values must fit in 20 bits")

    answer = 0
    for chosen in range(1, 1 << len(values)):
        result = limit - 1
        for index, value in enumerate(values):
            if chosen >> index & 1:
                result &= value
        if result == 0:
            answer += 1
    return answer % MODULO
```

Time is `O(n 2ⁿ)` and space is `O(1)`.

## 5. Better approach: sparse AND-state DP

Maintain the number of subsequences producing each AND encountered so far. For a new value, either start a subsequence with it or append it to every existing state.

```python
MODULO = 1_000_000_007
BIT_COUNT = 20


def count_zero_and_subsequences_sparse(values: list[int]) -> int:
    limit = 1 << BIT_COUNT
    if any(not 0 <= value < limit for value in values):
        raise ValueError("values must fit in 20 bits")

    counts: dict[int, int] = {}
    for value in values:
        additions = {value: 1}
        for current_and, amount in counts.items():
            next_and = current_and & value
            additions[next_and] = (additions.get(next_and, 0) + amount) % MODULO
        for result, amount in additions.items():
            counts[result] = (counts.get(result, 0) + amount) % MODULO
    return counts.get(0, 0)
```

If `s` distinct AND states occur, time is `O(ns)` and space is `O(s)`. The worst case is still exponential in the bit width.

## 6. Expert solution: superset zeta transform

Start with value frequencies. For each bit, add the count of masks with that bit to the corresponding mask without it. Then apply inclusion-exclusion by mask parity.

```python
MODULO = 1_000_000_007
BIT_COUNT = 20


def count_zero_and_subsequences(values: list[int]) -> int:
    limit = 1 << BIT_COUNT
    if any(not 0 <= value < limit for value in values):
        raise ValueError("values must fit in 20 bits")

    superset_count = [0] * limit
    for value in values:
        superset_count[value] += 1

    for bit in range(BIT_COUNT):
        step = 1 << bit
        for block in range(0, limit, step * 2):
            for mask in range(block, block + step):
                superset_count[mask] += superset_count[mask + step]

    powers_of_two = [1] * (len(values) + 1)
    for exponent in range(1, len(powers_of_two)):
        powers_of_two[exponent] = powers_of_two[exponent - 1] * 2 % MODULO

    answer = 0
    for mask, count in enumerate(superset_count):
        subsequences = powers_of_two[count] - 1
        if mask.bit_count() % 2:
            answer -= subsequences
        else:
            answer += subsequences
    return answer % MODULO
```

## 7. Why the expert solution is correct

After the zeta transform, `superset_count[mask]` counts exactly the positions whose values contain `mask`. Its nonempty subsets are precisely the subsequences whose AND contains `mask`. Inclusion-exclusion adds masks with even bit count and subtracts masks with odd bit count, retaining exactly subsequences whose AND contains no bit: AND zero.

Time is `O(20 · 2²⁰ + n)` and space is `O(2²⁰ + n)`.
