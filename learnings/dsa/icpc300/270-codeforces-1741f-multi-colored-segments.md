# ICPC300 270: Codeforces 1741F - Multi-Colored Segments

**Source:** [Codeforces 1741F - Multi-Colored Segments](https://codeforces.com/problemset/problem/1741/F)  
**Rating:** 2200  
**Pattern:** two endpoint sweeps excluding one color  
**Goal:** For every closed segment, find its minimum distance to a segment of a
different color. Intersecting segments have distance zero.

## 1. First principles

For a candidate whose left endpoint is no larger than the current segment's,
only the largest right endpoint matters. For a candidate whose left endpoint
is no smaller, only the smallest left endpoint matters.

Sweep once from left to right while keeping the two best right endpoints from
distinct colors, then right to left while keeping the two best negated left
endpoints. Two colors are sufficient because a query excludes only its own
color.

## 2. Cases that decide correctness

- Closed segments touching at one endpoint have distance zero.
- A segment nested inside another must update both segments' answers.
- Segments with the same left endpoint and different colors all intersect.
- The best global endpoint may have the forbidden color, requiring second best.
- The source guarantees at least two distinct colors.

## 3. Brute force: compare every differently colored pair

```python
Segment = tuple[int, int, int]


def colored_segment_distances_brute(segments: list[Segment]) -> list[int]:
    if not segments:
        raise ValueError("segments must be nonempty")
    for left, right, color in segments:
        if (
            type(left) is not int
            or type(right) is not int
            or type(color) is not int
            or left > right
        ):
            raise ValueError("invalid colored segment")
    if len({color for _, _, color in segments}) < 2:
        raise ValueError("at least two colors are required")

    answers = []
    for index, (left, right, color) in enumerate(segments):
        best = 10**100
        for other_index, (other_left, other_right, other_color) in enumerate(segments):
            if index == other_index or color == other_color:
                continue
            best = min(
                best,
                max(0, max(left, other_left) - min(right, other_right)),
            )
        answers.append(best)
    return answers
```

**Complexity:** `O(n^2)` time and `O(n)` output space.

## 4. Better approach: ordered sets per color

One ordered endpoint set per color can answer predecessor and successor
queries, but checking every other color is still too slow. Globally retaining
the best two distinct colors removes that factor.

## 5. Expert solution: best-two-color endpoint sweeps

```python
Segment = tuple[int, int, int]
Best = tuple[int, int | None]


def colored_segment_distances(segments: list[Segment]) -> list[int]:
    if not segments:
        raise ValueError("segments must be nonempty")
    for left, right, color in segments:
        if (
            type(left) is not int
            or type(right) is not int
            or type(color) is not int
            or left > right
        ):
            raise ValueError("invalid colored segment")
    if len({color for _, _, color in segments}) < 2:
        raise ValueError("at least two colors are required")

    negative_infinity = -(10**100)

    def add_endpoint(
        first: Best,
        second: Best,
        endpoint: int,
        color: int,
    ) -> tuple[Best, Best]:
        if first[1] == color:
            return (max(first[0], endpoint), color), second
        if second[1] == color:
            second = (max(second[0], endpoint), color)
            if second[0] > first[0]:
                return second, first
            return first, second
        candidate = (endpoint, color)
        if endpoint > first[0]:
            return candidate, first
        if endpoint > second[0]:
            return first, candidate
        return first, second

    answers = [10**100] * len(segments)
    order = sorted(range(len(segments)), key=lambda index: segments[index][0])
    first: Best = (negative_infinity, None)
    second: Best = (negative_infinity, None)
    group_start = 0
    while group_start < len(order):
        group_end = group_start
        left = segments[order[group_start]][0]
        while group_end < len(order) and segments[order[group_end]][0] == left:
            group_end += 1
        group = order[group_start:group_end]
        group_colors = {segments[index][2] for index in group}
        for index in group:
            _, _, color = segments[index]
            endpoint = first[0] if first[1] != color else second[0]
            if endpoint != negative_infinity:
                answers[index] = min(answers[index], max(0, left - endpoint))
            if len(group_colors) > 1:
                answers[index] = 0
        for index in group:
            _, right, color = segments[index]
            first, second = add_endpoint(first, second, right, color)
        group_start = group_end

    order.reverse()
    first = (negative_infinity, None)
    second = (negative_infinity, None)
    group_start = 0
    while group_start < len(order):
        group_end = group_start
        left = segments[order[group_start]][0]
        while group_end < len(order) and segments[order[group_end]][0] == left:
            group_end += 1
        group = order[group_start:group_end]
        group_colors = {segments[index][2] for index in group}
        for index in group:
            _, right, color = segments[index]
            negated_left = first[0] if first[1] != color else second[0]
            if negated_left != negative_infinity:
                answers[index] = min(answers[index], max(0, -negated_left - right))
            if len(group_colors) > 1:
                answers[index] = 0
        for index in group:
            _, _, color = segments[index]
            first, second = add_endpoint(first, second, -left, color)
        group_start = group_end

    return answers
```

### Why the expert code is correct

Every other segment starts either no later or no earlier than the current one.
The forward sweep gives the best distance in the first class from maximum right
endpoints; the reverse sweep gives the second class from minimum left
endpoints. Keeping two distinct colors answers an exclude-one-color query
without losing either optimum.

**Complexity:** `O(n log n)` time and `O(n)` space.

## 6. What to remember

```text
candidate begins earlier -> maximize its right endpoint
candidate begins later -> minimize its left endpoint
exclude one color -> retain the best two colors
```
