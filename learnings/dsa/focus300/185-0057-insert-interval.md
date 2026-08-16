# Focus300 185: LeetCode 57 - Insert Interval

**Source:** [LeetCode 57](https://leetcode.com/problems/insert-interval/)  
**Difficulty:** Medium  
**Pattern:** three-phase interval scan

## Exact contract

Insert one closed interval into intervals already sorted by start and mutually
non-overlapping. Merge all overlap and return sorted non-overlapping intervals.
Input intervals may be empty.

## First principles

Existing intervals fall into three ordered groups: strictly before the new
interval, overlapping it, and strictly after it. Copy the first group, expand
the inserted interval across the second, then append the third.


## Classroom board: see the repeated work once

```text
brute force tries every choice.
the optimized solution keeps only the state that must survive to the
next step.
```



## Step-by-step transformation

1. Read the input and identify the smallest state that still determines the answer.
2. Process one element, node, or row at a time while preserving that state.
3. Discard work that can no longer change the result.
4. Convert the surviving state into the output the problem requests.

The examples and code below show this transformation on the specific problem instance.


## Diagram: input to output

```text

        input
            |
            v
        core invariant
            |
            v
        process one step at a time
            |
            v
        output
```

The note shows the main idea, the repeated work, and the small state that turns the input into the output.

## Cases that decide correctness

- An empty input returns only the new interval.
- The new interval may belong before all or after all existing intervals.
- Endpoint equality is overlap for closed intervals.
- One insertion may bridge several existing intervals.
- Caller-owned inputs are not modified.

## Brute force: append, sort, and run a general merge

```python
def insert_interval_brute(
    intervals: list[list[int]], new_interval: list[int]
) -> list[list[int]]:
    if type(intervals) is not list or any(
        type(interval) is not list
        or len(interval) != 2
        or any(type(value) is not int for value in interval)
        for interval in intervals
    ):
        raise TypeError("intervals must be a list of integer pairs")
    if (
        type(new_interval) is not list
        or len(new_interval) != 2
        or any(type(value) is not int for value in new_interval)
    ):
        raise TypeError("new_interval must be an integer pair")
    if any(start > end for start, end in intervals + [new_interval]):
        raise ValueError("interval starts must not exceed ends")
    if any(
        intervals[index][1] >= intervals[index + 1][0]
        for index in range(len(intervals) - 1)
    ):
        raise ValueError("existing intervals must be sorted and non-overlapping")

    answer: list[list[int]] = []
    for start, end in sorted(
        [interval.copy() for interval in intervals] + [new_interval.copy()]
    ):
        if not answer or start > answer[-1][1]:
            answer.append([start, end])
        else:
            answer[-1][1] = max(answer[-1][1], end)
    return answer
```

Sorting makes this `O(n log n)` time and `O(n)` output space.

## Better approach: binary-search the unaffected prefix

The sorted starts and ends can locate the overlap range in `O(log n)`, but
building the output still costs `O(n)`. A linear three-phase scan is simpler
and does no extra searches.

## Expert solution: copy, coalesce, copy

```python
def insert_interval(
    intervals: list[list[int]], new_interval: list[int]
) -> list[list[int]]:
    if type(intervals) is not list or any(
        type(interval) is not list
        or len(interval) != 2
        or any(type(value) is not int for value in interval)
        for interval in intervals
    ):
        raise TypeError("intervals must be a list of integer pairs")
    if (
        type(new_interval) is not list
        or len(new_interval) != 2
        or any(type(value) is not int for value in new_interval)
    ):
        raise TypeError("new_interval must be an integer pair")
    if any(start > end for start, end in intervals + [new_interval]):
        raise ValueError("interval starts must not exceed ends")
    if any(
        intervals[index][1] >= intervals[index + 1][0]
        for index in range(len(intervals) - 1)
    ):
        raise ValueError("existing intervals must be sorted and non-overlapping")

    start, end = new_interval
    answer: list[list[int]] = []
    index = 0
    while index < len(intervals) and intervals[index][1] < start:
        answer.append(intervals[index].copy())
        index += 1
    while index < len(intervals) and intervals[index][0] <= end:
        start = min(start, intervals[index][0])
        end = max(end, intervals[index][1])
        index += 1
    answer.append([start, end])
    answer.extend(interval.copy() for interval in intervals[index:])
    return answer
```

Sorted non-overlap guarantees the three phases are contiguous. The overlap
phase produces one maximal union interval.

**Complexity:** `O(n)` time and `O(n)` output space.
