# Sweep Line

## Idea

A sweep line turns intervals or geometric events into ordered start/stop
changes. Process events from left to right while maintaining the active state.

## Visual model

```text
interval [start, end):  +1 at start, -1 at end
sorted events -> running active count
```

## Classroom board: maximum rooms in use

```text
intervals [1,4), [2,5), [4,6)
events: (1,+1),(2,+1),(4,-1),(4,+1),(5,-1),(6,-1)
active:    1      2      1      2      1      0
maximum = 2
```

At coordinate 4, end comes before start because intervals are half-open.

## Steps

1. Convert each interval into events.
2. Sort events by coordinate and tie rule.
3. Apply all changes in order.
4. Read the desired maximum, area, or active set from the running state.

## First-principles derivation

Many interval states change only at endpoints. Replace continuous movement
with sorted events: add an interval at its start and remove it at its end.

Between consecutive event coordinates nothing changes, so the active-state
invariant describes that whole region.

## Pattern recognition

Use a sweep line for overlap counts, room allocation, union length, offline
queries, or geometry where only event coordinates change the answer.

## Implementation: maximum overlap of half-open intervals

### C++

```cpp
int maximumOverlap(const std::vector<std::pair<int, int>>& intervals) {
    std::vector<std::pair<int, int>> events;
    for (auto [start, end] : intervals) {
        events.push_back({start, 1});
        events.push_back({end, -1});
    }
    std::sort(events.begin(), events.end());
    int active = 0;
    int answer = 0;
    for (auto [coordinate, change] : events) {
        active += change;
        answer = std::max(answer, active);
    }
    return answer;
}
```

### Python

```python
def maximum_overlap(intervals: list[tuple[int, int]]) -> int:
    events: list[tuple[int, int]] = []
    for start, end in intervals:
        events.append((start, 1))
        events.append((end, -1))
    active = answer = 0
    for _, change in sorted(events):
        active += change
        answer = max(answer, active)
    return answer
```

### Java

```java
static int maximumOverlap(int[][] intervals) {
    int[][] events = new int[2 * intervals.length][2];
    for (int index = 0; index < intervals.length; index++) {
        events[2 * index] = new int[] {intervals[index][0], 1};
        events[2 * index + 1] = new int[] {intervals[index][1], -1};
    }
    Arrays.sort(events, Comparator.<int[]>comparingInt(event -> event[0]).thenComparingInt(event -> event[1]));
    int active = 0;
    int answer = 0;
    for (int[] event : events) {
        active += event[1];
        answer = Math.max(answer, active);
    }
    return answer;
}
```

## Why it works

The active count is constant between consecutive event coordinates. Processing
all boundaries in order visits every point where that count can change.

## Complexity

Time is `O(n log n)` and space is `O(n)`.

## Common mistakes

- Using the wrong tie order. For `[start, end)`, end `-1` must be processed
  before start `+1` at the same coordinate.
- Updating the answer before applying the event.
- Treating discrete and continuous interval endpoints identically.
