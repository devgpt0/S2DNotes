# ICPC300 090: CSES - Maximum Subarray Sum II

**Source:** [CSES - Maximum Subarray Sum II](https://cses.fi/problemset/task/1644/)  
**Pattern:** prefix sums + monotonic deque  
**Goal:** Find the maximum subarray sum among lengths from `minimum_length` to
`maximum_length`, inclusive.

## 1. First principles

For prefix sums, a subarray ending at prefix index `right` has sum:

```text
prefix[right] - prefix[left]
```

Its valid left indices are
`right-maximum_length .. right-minimum_length`. Maximize the subarray by
subtracting the minimum prefix in that sliding index window. A monotonic deque
maintains that minimum in constant amortized time.

## 2. Cases that decide correctness

- All-negative arrays still require a non-empty allowed subarray.
- Both length boundaries are inclusive.
- Expire a prefix only after it falls left of the valid range.
- Equal prefix sums may discard the older one because it expires sooner.
- `minimum_length = maximum_length` fixes the length exactly.

## 3. Brute force: rescan every subarray

```python
def maximum_subarray_sum_ii_brute(
    values: list[int], minimum_length: int, maximum_length: int
) -> int:
    if not 1 <= minimum_length <= maximum_length <= len(values):
        raise ValueError("invalid subarray length bounds")

    best: int | None = None
    for left in range(len(values)):
        for right in range(
            left + minimum_length,
            min(len(values), left + maximum_length) + 1,
        ):
            candidate = sum(values[left:right])
            best = candidate if best is None else max(best, candidate)
    if best is None:
        raise RuntimeError("valid bounds must produce a subarray")
    return best
```

**Complexity:** `O(n^3)` time and `O(1)` extra space.

## 4. Better: prefix sums with all valid left indices

```python
def maximum_subarray_sum_ii_prefix(
    values: list[int], minimum_length: int, maximum_length: int
) -> int:
    if not 1 <= minimum_length <= maximum_length <= len(values):
        raise ValueError("invalid subarray length bounds")

    prefix = [0]
    for value in values:
        prefix.append(prefix[-1] + value)

    best: int | None = None
    for right in range(minimum_length, len(values) + 1):
        for left in range(max(0, right - maximum_length), right - minimum_length + 1):
            candidate = prefix[right] - prefix[left]
            best = candidate if best is None else max(best, candidate)
    if best is None:
        raise RuntimeError("valid bounds must produce a subarray")
    return best
```

**Complexity:** `O(n^2)` time and `O(n)` space.

## 5. Expert solution: monotonic prefix deque

```python
from collections import deque


def maximum_subarray_sum_ii_monotonic(
    values: list[int], minimum_length: int, maximum_length: int
) -> int:
    if not 1 <= minimum_length <= maximum_length <= len(values):
        raise ValueError("invalid subarray length bounds")

    prefix = [0]
    for value in values:
        prefix.append(prefix[-1] + value)

    candidates: deque[int] = deque()
    best: int | None = None
    for right in range(minimum_length, len(values) + 1):
        added = right - minimum_length
        while candidates and prefix[candidates[-1]] >= prefix[added]:
            candidates.pop()
        candidates.append(added)

        earliest = right - maximum_length
        while candidates[0] < earliest:
            candidates.popleft()

        candidate = prefix[right] - prefix[candidates[0]]
        best = candidate if best is None else max(best, candidate)

    if best is None:
        raise RuntimeError("valid bounds must produce a subarray")
    return best
```

### Why the expert code is correct

At each right endpoint, the deque contains exactly the useful valid left
prefixes in increasing prefix-sum order. Its front is therefore the smallest
prefix that can form an allowed-length subarray ending at `right`.

**Complexity:** `O(n)` time and `O(n)` space; every prefix enters and leaves the
deque at most once.

## 6. What to remember

```text
length bounds -> sliding range of prefix indices
maximum subarray sum -> current prefix - minimum valid earlier prefix
sliding minimum -> monotonic deque
```
