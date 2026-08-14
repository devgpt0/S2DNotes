# Focus300 103: LeetCode 732 - My Calendar III

**Source:** [LeetCode 732](https://leetcode.com/problems/my-calendar-iii/)  
**Difficulty:** Hard  
**Pattern:** online range addition and global maximum

## Exact contract

Implement `book(start_time, end_time)` for half-open events
`[start_time, end_time)`, where `0 <= start_time < end_time <= 10^9`. After
every booking, return the largest number of events that overlap at any instant.

## First principles

An event changes the active count by `+1` at its start and `-1` at its end.
Sweeping those changes gives the maximum, but repeating a full sweep after each
online update is expensive. A dynamic segment tree range-adds only the covered
branches of the huge coordinate domain and keeps the global maximum at its root.

## Cases that decide correctness

- Events are half-open, so `[10, 20)` and `[20, 30)` do not overlap.
- Duplicate and nested events are valid and increase the maximum separately.
- The answer is required after every call, not only after all bookings.
- The coordinate range is too large for an array indexed by time.
- Each booking must satisfy the source bounds exactly.

## Brute force: sort every endpoint after each booking

```python
class MyCalendarThreeBrute:
    def __init__(self) -> None:
        self._bookings: list[tuple[int, int]] = []

    def book(self, start_time: int, end_time: int) -> int:
        if not 0 <= start_time < end_time <= 1_000_000_000:
            raise ValueError("booking must satisfy 0 <= start < end <= 1e9")
        self._bookings.append((start_time, end_time))
        events = [
            event for start, end in self._bookings for event in ((start, 1), (end, -1))
        ]
        active = 0
        maximum = 0
        for _, change in sorted(events):
            active += change
            maximum = max(maximum, active)
        return maximum
```

Sorting `-1` before `+1` at an equal coordinate preserves half-open semantics.
After `q` calls, this approach has taken `O(q^2 log q)` total time.

## Better solution: persistent difference map

```python
class MyCalendarThreeSweep:
    def __init__(self) -> None:
        self._changes: dict[int, int] = {}

    def book(self, start_time: int, end_time: int) -> int:
        if not 0 <= start_time < end_time <= 1_000_000_000:
            raise ValueError("booking must satisfy 0 <= start < end <= 1e9")
        self._changes[start_time] = self._changes.get(start_time, 0) + 1
        self._changes[end_time] = self._changes.get(end_time, 0) - 1

        active = 0
        maximum = 0
        for time in sorted(self._changes):
            active += self._changes[time]
            maximum = max(maximum, active)
        return maximum
```

The map stores each boundary once, but a query still sorts and scans all known
boundaries: `O(q log q)` time per booking and `O(q)` space.

## Expert solution: dynamic lazy segment tree

```python
class MyCalendarThree:
    def __init__(self) -> None:
        self._maximum: dict[int, int] = {}
        self._lazy: dict[int, int] = {}

    def _add(
        self,
        query_left: int,
        query_right: int,
        node: int,
        left: int,
        right: int,
    ) -> None:
        if query_left <= left and right <= query_right:
            self._maximum[node] = self._maximum.get(node, 0) + 1
            self._lazy[node] = self._lazy.get(node, 0) + 1
            return

        middle = (left + right) // 2
        if query_left <= middle:
            self._add(query_left, query_right, node * 2, left, middle)
        if query_right > middle:
            self._add(query_left, query_right, node * 2 + 1, middle + 1, right)
        self._maximum[node] = self._lazy.get(node, 0) + max(
            self._maximum.get(node * 2, 0),
            self._maximum.get(node * 2 + 1, 0),
        )

    def book(self, start_time: int, end_time: int) -> int:
        if not 0 <= start_time < end_time <= 1_000_000_000:
            raise ValueError("booking must satisfy 0 <= start < end <= 1e9")
        self._add(start_time, end_time - 1, 1, 0, 1_000_000_000 - 1)
        return self._maximum[1]
```

Each node maximum equals its own lazy coverage plus the larger child maximum.
Updating through `end_time - 1` converts the half-open booking to the tree's
inclusive integer range.

**Complexity:** `O(log 10^9)` time per booking and
`O(q log 10^9)` created nodes after `q` calls.
