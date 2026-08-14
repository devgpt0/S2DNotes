# Focus300 055: LeetCode 352 - Data Stream as Disjoint Intervals

**Source:** [LeetCode 352 - Data Stream as Disjoint Intervals](https://leetcode.com/problems/data-stream-as-disjoint-intervals/)  
**Difficulty:** Hard  
**Pattern:** ordered interval insertion and neighbor merging  

## Exact contract

Maintain a stream of integers in `[0, 10_000]`. `add_num(value)` inserts a
value, including duplicates. `get_intervals()` returns sorted, disjoint,
maximal inclusive intervals covering every inserted value.

## First principles

Only the intervals immediately before and after an inserted value can change.
The value is either already covered, extends one neighbor, bridges both
neighbors, or creates a new singleton interval.

## Cases that decide correctness

- Duplicate insertion changes nothing.
- A value one above the left interval extends it.
- A value one below the right interval extends it.
- Bridging `[a, value-1]` and `[value+1, b]` creates `[a, b]`.
- Returned intervals must not expose mutable internal storage.

## Brute force: store values and rebuild every query

```python
class SummaryRangesBrute:
    def __init__(self) -> None:
        self._values: set[int] = set()

    def add_num(self, value: int) -> None:
        if type(value) is not int or not 0 <= value <= 10_000:
            raise ValueError("value must be an integer in [0, 10000]")
        self._values.add(value)

    def get_intervals(self) -> list[tuple[int, int]]:
        intervals: list[tuple[int, int]] = []
        for value in sorted(self._values):
            if not intervals or value > intervals[-1][1] + 1:
                intervals.append((value, value))
            else:
                intervals[-1] = (intervals[-1][0], value)
        return intervals
```

**Complexity:** `O(1)` expected insertion and `O(v log v)` per query.

## Better approach: bounded-universe bitmap

A boolean array gives `O(1)` insertion and `O(10_000)` query time. It exploits
this source's bound but is not output-sensitive.

## Expert solution: maintain maximal intervals incrementally

```python
from bisect import bisect_left


class SummaryRanges:
    def __init__(self) -> None:
        self._intervals: list[tuple[int, int]] = []

    def add_num(self, value: int) -> None:
        if type(value) is not int or not 0 <= value <= 10_000:
            raise ValueError("value must be an integer in [0, 10000]")
        index = bisect_left(self._intervals, (value, -1))
        if index > 0 and self._intervals[index - 1][1] >= value:
            return
        if index < len(self._intervals) and self._intervals[index][0] == value:
            return

        joins_left = index > 0 and self._intervals[index - 1][1] + 1 == value
        joins_right = (
            index < len(self._intervals) and self._intervals[index][0] - 1 == value
        )
        if joins_left and joins_right:
            left_start = self._intervals[index - 1][0]
            right_end = self._intervals[index][1]
            self._intervals[index - 1] = (left_start, right_end)
            self._intervals.pop(index)
        elif joins_left:
            left_start, _ = self._intervals[index - 1]
            self._intervals[index - 1] = (left_start, value)
        elif joins_right:
            _, right_end = self._intervals[index]
            self._intervals[index] = (value, right_end)
        else:
            self._intervals.insert(index, (value, value))

    def get_intervals(self) -> list[tuple[int, int]]:
        return self._intervals.copy()
```

Binary search identifies the only possible neighbors. The four exhaustive
cases preserve sorted, disjoint, maximal intervals after every insertion.

**Complexity:** `O(log q)` search plus `O(q)` list shifting per insertion and
`O(q)` query time for `q` current intervals. A tree map removes the shift cost.

