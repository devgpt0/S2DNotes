# Focus300 087: LeetCode 630 - Course Schedule III

**Source:** [LeetCode 630](https://leetcode.com/problems/course-schedule-iii/)  
**Difficulty:** Hard  
**Pattern:** deadline order with greedy replacement

## Exact contract

Each course is `(duration, last_day)`. Starting on day zero, courses are taken
one at a time without interruption, and a chosen course must finish no later
than its `last_day`. Return the maximum number of courses that can be completed.
Both fields are positive, and at most 10,000 courses are supplied.

## First principles

Any feasible chosen set can be scheduled in nondecreasing deadline order.
While scanning in that order, accepting a course increases the count. If the
elapsed time becomes infeasible, removing the longest accepted duration keeps
the same count minus one while leaving the smallest possible elapsed time for
all future deadlines.


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

- A course whose duration exceeds its own deadline can never remain selected.
- Equal deadlines may be processed in either order.
- Replacing a long earlier course can make room for several later courses.
- The answer is a count; the source does not require the chosen schedule.
- Durations and deadlines must be strictly positive integers.

## Brute force: inspect every subset

```python
from collections.abc import Sequence


Course = tuple[int, int]


def maximum_courses_brute(courses: Sequence[Course]) -> int:
    if len(courses) > 10_000:
        raise ValueError("at most 10000 courses are allowed")
    if any(
        type(course) is not tuple
        or len(course) != 2
        or type(course[0]) is not int
        or type(course[1]) is not int
        for course in courses
    ):
        raise TypeError("each course must be an (int, int) tuple")
    if any(duration <= 0 or deadline <= 0 for duration, deadline in courses):
        raise ValueError("durations and deadlines must be positive")

    ordered = sorted(courses, key=lambda course: course[1])
    answer = 0
    for mask in range(1 << len(ordered)):
        elapsed = 0
        count = 0
        feasible = True
        for index, (duration, deadline) in enumerate(ordered):
            if mask & (1 << index):
                elapsed += duration
                count += 1
                if elapsed > deadline:
                    feasible = False
                    break
        if feasible:
            answer = max(answer, count)
    return answer
```

Deadline ordering is sufficient to test a chosen subset. Enumeration takes
`O(2^n * n)` time and `O(n)` sorting space.

## Better approach: minimum elapsed time for each count

```python
from collections.abc import Sequence


Course = tuple[int, int]


def maximum_courses_dp(courses: Sequence[Course]) -> int:
    if len(courses) > 10_000:
        raise ValueError("at most 10000 courses are allowed")
    if any(
        type(course) is not tuple
        or len(course) != 2
        or type(course[0]) is not int
        or type(course[1]) is not int
        for course in courses
    ):
        raise TypeError("each course must be an (int, int) tuple")
    if any(duration <= 0 or deadline <= 0 for duration, deadline in courses):
        raise ValueError("durations and deadlines must be positive")

    unreachable = sum(duration for duration, _ in courses) + 1
    minimum_time = [0] + [unreachable] * len(courses)
    answer = 0
    for duration, deadline in sorted(courses, key=lambda course: course[1]):
        for count in range(answer, -1, -1):
            finish = minimum_time[count] + duration
            if finish <= deadline and finish < minimum_time[count + 1]:
                minimum_time[count + 1] = finish
                answer = max(answer, count + 1)
    return answer
```

The DP retains the least elapsed time for each attainable count. It uses
`O(n^2)` time and `O(n)` space.

## Expert solution: replace the longest accepted course

```python
from collections.abc import Sequence
from heapq import heappop, heappush


Course = tuple[int, int]


def maximum_courses(courses: Sequence[Course]) -> int:
    if len(courses) > 10_000:
        raise ValueError("at most 10000 courses are allowed")
    if any(
        type(course) is not tuple
        or len(course) != 2
        or type(course[0]) is not int
        or type(course[1]) is not int
        for course in courses
    ):
        raise TypeError("each course must be an (int, int) tuple")
    if any(duration <= 0 or deadline <= 0 for duration, deadline in courses):
        raise ValueError("durations and deadlines must be positive")

    elapsed = 0
    longest_first: list[int] = []
    for duration, deadline in sorted(courses, key=lambda course: course[1]):
        elapsed += duration
        heappush(longest_first, -duration)
        if elapsed > deadline:
            elapsed += heappop(longest_first)
    return len(longest_first)
```

After each deadline, the heap represents a feasible set of maximum size with
minimum possible elapsed time among the greedy choices. Removing its longest
course is therefore the exchange that best preserves future capacity.

**Complexity:** `O(n log n)` time and `O(n)` space.
