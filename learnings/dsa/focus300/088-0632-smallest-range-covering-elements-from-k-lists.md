# Focus300 088: LeetCode 632 - Smallest Range Covering Elements from K Lists

**Source:** [LeetCode 632](https://leetcode.com/problems/smallest-range-covering-elements-from-k-lists/)  
**Difficulty:** Hard  
**Pattern:** k-way merge with a tracked maximum

## Exact contract

Given nonempty sorted integer lists, return the inclusive range `[left, right]`
that contains at least one number from every list. Prefer the smaller width;
when widths tie, prefer the smaller `left`. The source guarantees at least one
list and at most 3,500 total values.

## First principles

Choose one current value from each list. Those values define a covering range
from their minimum to their maximum. Advancing anything except the minimum
cannot reduce the range's left boundary, so only the list contributing the
minimum can lead to a better range. A min-heap identifies that list while one
variable tracks the current maximum.


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

- Duplicates within and across lists are valid.
- A zero-width range is optimal and cannot be improved.
- Equal widths choose the smaller left endpoint.
- Stop when the popped value's list is exhausted; no later choice covers all
  lists.
- Unsorted or empty component lists violate the contract and fail fast.

## Brute force: choose one value from every list

```python
from itertools import product


def smallest_covering_range_brute(number_lists: list[list[int]]) -> list[int]:
    if type(number_lists) is not list or any(
        type(values) is not list for values in number_lists
    ):
        raise TypeError("number_lists must be a list of integer lists")
    if not number_lists or any(not values for values in number_lists):
        raise ValueError("at least one nonempty list is required")
    if sum(map(len, number_lists)) > 3_500:
        raise ValueError("at most 3500 values are allowed")
    if any(type(value) is not int for values in number_lists for value in values):
        raise TypeError("every value must be an integer")
    if any(
        values[index] > values[index + 1]
        for values in number_lists
        for index in range(len(values) - 1)
    ):
        raise ValueError("each component list must be sorted")

    choice = min(
        product(*number_lists),
        key=lambda values: (max(values) - min(values), min(values)),
    )
    return [min(choice), max(choice)]
```

For list lengths `m1..mk`, this examines `m1 * ... * mk` combinations and
stores `O(k)` values per generated tuple.

## Better approach: flatten and slide a colored window

Attach each value's source-list index, sort all values, and slide a window
until it contains every source color. This is `O(N log N)` time and `O(N)`
space. The heap method avoids materializing and sorting the entire merge.

## Expert solution: advance only the current minimum

```python
from heapq import heapify, heappop, heappush


def smallest_covering_range(number_lists: list[list[int]]) -> list[int]:
    if type(number_lists) is not list or any(
        type(values) is not list for values in number_lists
    ):
        raise TypeError("number_lists must be a list of integer lists")
    if not number_lists or any(not values for values in number_lists):
        raise ValueError("at least one nonempty list is required")
    if sum(map(len, number_lists)) > 3_500:
        raise ValueError("at most 3500 values are allowed")
    if any(type(value) is not int for values in number_lists for value in values):
        raise TypeError("every value must be an integer")
    if any(
        values[index] > values[index + 1]
        for values in number_lists
        for index in range(len(values) - 1)
    ):
        raise ValueError("each component list must be sorted")

    heap = [
        (values[0], list_index, 0) for list_index, values in enumerate(number_lists)
    ]
    heapify(heap)
    current_maximum = max(value for value, _, _ in heap)
    best_left = heap[0][0]
    best_right = current_maximum

    while True:
        current_minimum, list_index, value_index = heappop(heap)
        if (current_maximum - current_minimum, current_minimum) < (
            best_right - best_left,
            best_left,
        ):
            best_left, best_right = current_minimum, current_maximum

        next_index = value_index + 1
        if next_index == len(number_lists[list_index]):
            break
        next_value = number_lists[list_index][next_index]
        current_maximum = max(current_maximum, next_value)
        heappush(heap, (next_value, list_index, next_index))

    return [best_left, best_right]
```

The heap always contains exactly one value from every list. Popping and
advancing its minimum enumerates every potentially improving left boundary,
and exhaustion proves that no complete later range exists.

**Complexity:** `O(N log k)` time and `O(k)` space for `N` total values and
`k` lists.
