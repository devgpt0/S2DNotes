# ICPC300 043: CSES - Meet in the Middle

**Source:** [CSES - Meet in the Middle](https://cses.fi/problemset/task/1628/)  
**Pattern:** split subset enumeration  
**Goal:** Count the subsets whose element sum is exactly `x`. Equal values at
different indices are different selectable elements.

## 1. Problem in plain words

For values `[2, 2, 3]` and target `5`, there are two valid subsets: choose the
first `2` with `3`, or choose the second `2` with `3`.

With up to forty elements, `2^n` is too large, while `2^(n/2)` is manageable.

## 2. First principles

Split the array into left and right halves. Every full subset is uniquely a
pair `(left_subset, right_subset)`. It reaches target `x` exactly when:

`left_sum + right_sum = x`.

Enumerate all subset sums of both halves. For each left sum `s`, add the number
of right subsets whose sum is `x - s`.

## 3. Cases that decide correctness

| Case | Required behavior |
| --- | --- |
| Empty subset and target `0` | Count it once. |
| Duplicate values | Preserve multiplicity by subset indices. |
| No matching sum | Return `0`. |
| All elements chosen | Included like every other subset. |
| Negative values in the reusable function | Complement counting still works. |

## 4. Brute force: enumerate all masks

```python
def count_target_subsets_brute_force(values: list[int], target: int) -> int:
    answer = 0
    for mask in range(1 << len(values)):
        total = 0
        for index, value in enumerate(values):
            if mask & (1 << index):
                total += value
        if total == target:
            answer += 1
    return answer
```

**Complexity:** `O(n 2^n)` time and `O(1)` auxiliary memory.

## 5. Better when many sums coincide: incremental frequency DP

Store how many subsets produce each sum. Processing a value duplicates every
existing choice into "exclude" and "include" states. This can be fast with
many repeated sums, but may still create `2^n` distinct keys.

```python
from collections import Counter


def count_target_subsets_frequency_dp(values: list[int], target: int) -> int:
    frequencies = Counter({0: 1})
    for value in values:
        next_frequencies = frequencies.copy()
        for current_sum, count in frequencies.items():
            next_frequencies[current_sum + value] += count
        frequencies = next_frequencies
    return frequencies[target]
```

**Complexity:** `O(nS)` expected time and `O(S)` memory, where `S` is the
number of distinct subset sums retained. Worst-case `S = 2^n`.

## 6. Expert solution: enumerate two half-size sum lists

The iterative generator starts with the empty-subset sum `0`; each value adds
one shifted copy of all sums built so far. A frequency table on the right half
handles duplicate sums without losing subset multiplicity.

```python
from collections import Counter


def count_target_subsets(values: list[int], target: int) -> int:
    middle = len(values) // 2

    def subset_sums(part: list[int]) -> list[int]:
        sums = [0]
        for value in part:
            sums.extend(current_sum + value for current_sum in sums.copy())
        return sums

    left_sums = subset_sums(values[:middle])
    right_frequencies = Counter(subset_sums(values[middle:]))
    return sum(right_frequencies[target - left_sum] for left_sum in left_sums)
```

### Why the expert code is correct

- The generator creates every subset sum of a half exactly once per subset.
- Splitting by indices makes every full subset correspond to exactly one pair
  of generated half subsets.
- Complement lookup counts exactly the right-half subsets that complete each
  left-half subset to the target.
- Frequency values retain distinct choices that happen to have equal sums.

**Complexity:** `O(2^(n/2))` expected time and `O(2^(n/2))` memory.

## 7. What to remember

When `n` is near forty and the operation separates across two halves, replace
one `2^n` enumeration with two `2^(n/2)` enumerations and match complements.
