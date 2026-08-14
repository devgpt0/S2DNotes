# Focus300 099: LeetCode 715 - Range Module

**Source:** [LeetCode 715](https://leetcode.com/problems/range-module/)  
**Difficulty:** Hard  
**Pattern:** canonical sorted union of half-open intervals

## Exact contract

Maintain a set of real numbers under at most `10_000` operations with integer
endpoints `1 <= left < right <= 10^9`:

- `add_range(left, right)` tracks every number in `[left, right)`.
- `query_range(left, right)` reports whether every number in that interval is
  tracked.
- `remove_range(left, right)` stops tracking every number in that interval.

## First principles

The tracked set can be represented uniquely as sorted, disjoint, non-touching
half-open intervals. Addition merges every overlapping or touching interval.
Removal preserves up to two pieces of each overlap. A query needs only the last
stored interval whose start is at most the query's left endpoint.

## Cases that decide correctness

- The right endpoint is excluded.
- Touching tracked intervals should merge because their union has no gap.
- Removal can delete, trim, or split an interval.
- A query spanning a real gap is false even when both endpoints are tracked.
- Empty intervals are outside the source contract and fail immediately.

## Brute force: track every integer unit segment

```python
class BruteRangeModule:
    def __init__(self) -> None:
        self._tracked_units: set[int] = set()

    def add_range(self, left: int, right: int) -> None:
        if type(left) is not int or type(right) is not int:
            raise TypeError("range endpoints must be integers")
        if not 1 <= left < right <= 1_000_000_000:
            raise ValueError("range must satisfy 1 <= left < right <= 10^9")
        self._tracked_units.update(range(left, right))

    def query_range(self, left: int, right: int) -> bool:
        if type(left) is not int or type(right) is not int:
            raise TypeError("range endpoints must be integers")
        if not 1 <= left < right <= 1_000_000_000:
            raise ValueError("range must satisfy 1 <= left < right <= 10^9")
        return all(unit in self._tracked_units for unit in range(left, right))

    def remove_range(self, left: int, right: int) -> None:
        if type(left) is not int or type(right) is not int:
            raise TypeError("range endpoints must be integers")
        if not 1 <= left < right <= 1_000_000_000:
            raise ValueError("range must satisfy 1 <= left < right <= 10^9")
        self._tracked_units.difference_update(range(left, right))
```

Integer endpoints make each integer represent the real unit segment
`[integer, integer+1)`, but coordinate magnitude makes this infeasible.

## Better insight: store only boundaries where coverage changes

Maintaining a canonical interval union makes the number of stored items depend
on operations, not coordinate magnitude. Binary search answers queries; linear
merging and splitting keep updates simple and reliable.

## Expert solution: sorted disjoint half-open intervals

```python
class RangeModule:
    def __init__(self) -> None:
        self._ranges: list[tuple[int, int]] = []

    def add_range(self, left: int, right: int) -> None:
        if type(left) is not int or type(right) is not int:
            raise TypeError("range endpoints must be integers")
        if not 1 <= left < right <= 1_000_000_000:
            raise ValueError("range must satisfy 1 <= left < right <= 10^9")

        merged: list[tuple[int, int]] = []
        inserted = False
        for start, stop in self._ranges:
            if stop < left:
                merged.append((start, stop))
            elif right < start:
                if not inserted:
                    merged.append((left, right))
                    inserted = True
                merged.append((start, stop))
            else:
                left = min(left, start)
                right = max(right, stop)
        if not inserted:
            merged.append((left, right))
        self._ranges = merged

    def query_range(self, left: int, right: int) -> bool:
        if type(left) is not int or type(right) is not int:
            raise TypeError("range endpoints must be integers")
        if not 1 <= left < right <= 1_000_000_000:
            raise ValueError("range must satisfy 1 <= left < right <= 10^9")

        low = 0
        high = len(self._ranges)
        while low < high:
            middle = (low + high) // 2
            if self._ranges[middle][0] <= left:
                low = middle + 1
            else:
                high = middle
        candidate = low - 1
        return candidate >= 0 and self._ranges[candidate][1] >= right

    def remove_range(self, left: int, right: int) -> None:
        if type(left) is not int or type(right) is not int:
            raise TypeError("range endpoints must be integers")
        if not 1 <= left < right <= 1_000_000_000:
            raise ValueError("range must satisfy 1 <= left < right <= 10^9")

        remaining: list[tuple[int, int]] = []
        for start, stop in self._ranges:
            if stop <= left or right <= start:
                remaining.append((start, stop))
                continue
            if start < left:
                remaining.append((start, left))
            if right < stop:
                remaining.append((right, stop))
        self._ranges = remaining
```

Every update restores the canonical interval invariant. The binary search then
finds the only interval that could cover a query.

**Complexity:** `O(q)` worst-case time for add/remove, `O(log q)` for query,
and `O(q)` space after `q` operations.
