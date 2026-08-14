# Focus300 147: LeetCode 903 - Valid Permutations for DI Sequence

**Source:** [LeetCode 903](https://leetcode.com/problems/valid-permutations-for-di-sequence/)  
**Difficulty:** Hard  
**Pattern:** rank DP with prefix and suffix sums

## Exact contract

For a string of `I` and `D` with length `n`, count permutations of
`0, 1, ..., n` whose adjacent values increase at every `I` and decrease at every
`D`. Return the result modulo `1_000_000_007`.

## First principles

Only the rank of the current last value matters. When appending a new value with
rank `r`, an `I` accepts previous last ranks below `r`; a `D` accepts ranks at or
above `r`. Therefore each new DP row is a prefix-sum or suffix-sum transform of
the previous row.

## Cases that decide correctness

- A length-`n` pattern permutes `n + 1` values.
- The first one-value prefix has one arrangement.
- Rank is relative within the values used so far, not the original numeric value.
- `I` uses previous ranks strictly below the new rank.
- `D` uses previous ranks at least the new rank after insertion.

## Brute force: test every permutation

```python
from itertools import permutations


def num_perms_di_sequence_brute(pattern: str) -> int:
    if not pattern or any(character not in "ID" for character in pattern):
        raise ValueError("pattern must be a non-empty string of I and D")

    answer = 0
    for candidate in permutations(range(len(pattern) + 1)):
        if all(
            (relation == "I" and candidate[index] < candidate[index + 1])
            or (relation == "D" and candidate[index] > candidate[index + 1])
            for index, relation in enumerate(pattern)
        ):
            answer += 1
    return answer % 1_000_000_007
```

This takes `O(n * (n + 1)!)` time.

## Better solution: sum every compatible previous rank

```python
def num_perms_di_sequence_better(pattern: str) -> int:
    if not pattern or any(character not in "ID" for character in pattern):
        raise ValueError("pattern must be a non-empty string of I and D")

    modulus = 1_000_000_007
    counts = [1]
    for relation in pattern:
        width = len(counts) + 1
        if relation == "I":
            counts = [sum(counts[:rank]) % modulus for rank in range(width)]
        else:
            counts = [sum(counts[rank:]) % modulus for rank in range(width)]
    return sum(counts) % modulus
```

Explicit range sums make this `O(n^3)` time and `O(n)` space.

## Expert solution: running prefix or suffix sums

```python
def num_perms_di_sequence(pattern: str) -> int:
    if not pattern or any(character not in "ID" for character in pattern):
        raise ValueError("pattern must be a non-empty string of I and D")

    modulus = 1_000_000_007
    counts = [1]
    for relation in pattern:
        width = len(counts) + 1
        next_counts = [0] * width
        running = 0
        if relation == "I":
            for rank in range(width):
                next_counts[rank] = running
                if rank < len(counts):
                    running = (running + counts[rank]) % modulus
        else:
            for rank in range(width - 1, -1, -1):
                if rank < len(counts):
                    running = (running + counts[rank]) % modulus
                next_counts[rank] = running
        counts = next_counts
    return sum(counts) % modulus
```

The running sum contains exactly the compatible rank range before each state is
written, reproducing the recurrence in constant time per state.

**Complexity:** `O(n^2)` time and `O(n)` space.
