# Merging Intervals

## Idea

Sort intervals by start. Any interval that overlaps the last merged interval
extends it; a non-overlapping interval starts a new group.

## Visual model

```text
[1-------5]
    [3---------8]  -> [1-------------8]
                         [10---12]    -> new interval
```

## Classroom board: merge after sorting

```text
sorted: [1,4], [2,6], [8,9]
start merged [1,4]
[2,6] overlaps because 2 <= 4 -> extend to [1,6]
[8,9] starts after 6          -> new group
answer: [1,6], [8,9]
```

## Steps

1. Sort intervals by start, then end.
2. Start the answer with the first interval.
3. If the next start is at most the last end, extend the last end.
4. Otherwise append a new interval.

## First-principles derivation

After sorting by start, any interval that can overlap the current merged
interval appears before every interval starting later.

If the next start is inside the current end, extend the end; otherwise the
current interval is final and can be emitted.

## Pattern recognition

Use it for union of ranges, calendar blocks, covered segments, or any task that
must combine overlapping intervals.

## Implementation: closed intervals

### C++

```cpp
std::vector<std::pair<int, int>> mergeIntervals(std::vector<std::pair<int, int>> intervals) {
    if (intervals.empty()) return {};
    std::sort(intervals.begin(), intervals.end());
    std::vector<std::pair<int, int>> merged{intervals.front()};
    for (int index = 1; index < static_cast<int>(intervals.size()); ++index) {
        auto [start, end] = intervals[index];
        if (start <= merged.back().second) merged.back().second = std::max(merged.back().second, end);
        else merged.push_back({start, end});
    }
    return merged;
}
```

### Python

```python
def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if not intervals:
        return []
    merged = [list(interval) for interval in sorted(intervals)]
    write = 0
    for read in range(1, len(merged)):
        start, end = merged[read]
        if start <= merged[write][1]:
            merged[write][1] = max(merged[write][1], end)
        else:
            write += 1
            merged[write] = [start, end]
    return [(start, end) for start, end in merged[: write + 1]]
```

### Java

```java
static List<int[]> mergeIntervals(int[][] intervals) {
    Arrays.sort(intervals, Comparator.comparingInt(interval -> interval[0]));
    List<int[]> merged = new ArrayList<>();
    for (int[] interval : intervals) {
        if (merged.isEmpty() || interval[0] > merged.get(merged.size() - 1)[1]) {
            merged.add(interval.clone());
        } else {
            int[] last = merged.get(merged.size() - 1);
            last[1] = Math.max(last[1], interval[1]);
        }
    }
    return merged;
}
```

## Why it works

After sorting, no future interval can start before the current one. Therefore
only the last merged interval can overlap the next interval.

## Complexity

Time is `O(n log n)` and output space is `O(n)`.

## Common mistakes

- Forgetting whether endpoints are closed or half-open.
- Replacing the last end instead of taking the maximum.
- Failing on empty input.
