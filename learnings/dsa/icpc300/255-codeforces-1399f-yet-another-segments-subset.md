# ICPC300 255: Codeforces 1399F - Yet Another Segments Subset

**Source:** [Codeforces 1399F - Yet Another Segments Subset](https://codeforces.com/problemset/problem/1399/F)  
**Rating:** 2200  
**Pattern:** coordinate-compressed interval DP for a laminar subset  
**Goal:** Select as many closed segments as possible so every two selected
segments are disjoint or one contains the other. Equal segments are compatible.

## 1. First principles

Compress all endpoints. Let `dp[left][right]` be the best laminar subset using
segments contained in that coordinate interval.

Without a segment spanning the entire interval, top-level selected segments
can be separated at some split. Every copy of the exact segment
`[left, right]` contains all internal choices and can then be added:

```text
dp[left][right] = count_exact[left][right]
                  + max(dp[left][split] + dp[split+1][right])
```

## 2. Cases that decide correctness

- Equal input segments may all be selected.
- Touching closed segments overlap at an endpoint and must be nested to coexist.
- Endpoint compression preserves containment and disjointness order.
- A one-point segment is a valid interval.
- The answer may contain several disjoint top-level components.

## 3. Brute force: test every segment subset

```python
def maximum_laminar_segments_brute(segments: list[tuple[int, int]]) -> int:
    if not segments or any(left > right for left, right in segments):
        raise ValueError("segments must be nonempty and ordered")

    def compatible(first: tuple[int, int], second: tuple[int, int]) -> bool:
        first_left, first_right = first
        second_left, second_right = second
        disjoint = first_right < second_left or second_right < first_left
        nested = (
            first_left <= second_left <= second_right <= first_right
            or second_left <= first_left <= first_right <= second_right
        )
        return disjoint or nested

    answer = 0
    for chosen in range(1 << len(segments)):
        selected = [
            segments[index] for index in range(len(segments)) if chosen >> index & 1
        ]
        if all(
            compatible(selected[first], selected[second])
            for first in range(len(selected))
            for second in range(first + 1, len(selected))
        ):
            answer = max(answer, len(selected))
    return answer
```

**Complexity:** `O(2^n n^2)` time and `O(n)` space.

## 4. Better transition: split disjoint roots, then add containers

A laminar family forms a forest by containment. Inside a coordinate interval,
its top-level children are disjoint and admit a separating split. Copies of the
full interval sit above that entire forest and are compatible with all of it.

## 5. Expert solution: cubic interval DP

```python
def maximum_laminar_segments(segments: list[tuple[int, int]]) -> int:
    if not segments or any(left > right for left, right in segments):
        raise ValueError("segments must be nonempty and ordered")

    coordinates = sorted({coordinate for segment in segments for coordinate in segment})
    index = {coordinate: position for position, coordinate in enumerate(coordinates)}
    size = len(coordinates)
    exact_count = [[0] * size for _ in range(size)]
    for left, right in segments:
        exact_count[index[left]][index[right]] += 1

    dp = [[0] * size for _ in range(size)]
    for length in range(1, size + 1):
        for left in range(size - length + 1):
            right = left + length - 1
            best_inside = 0
            for split in range(left, right):
                best_inside = max(best_inside, dp[left][split] + dp[split + 1][right])
            dp[left][right] = best_inside + exact_count[left][right]
    return dp[0][size - 1]
```

### Why the expert code is correct

Remove all selected copies equal to `[left,right]`; they contain every remaining
selected segment. The maximal remaining segments are mutually disjoint, so some
coordinate split separates them into two independent laminar families covered
by the recurrence. Conversely, combining two split solutions and adding all
exact outer copies preserves laminarity. Induction on interval length proves
optimality.

**Complexity:** `O(C^3 + n)` time and `O(C^2)` space for `C <= 2n` compressed
coordinates.

## 6. What to remember

```text
laminar intervals -> containment forest
top-level siblings -> disjoint split
exact outer interval -> compatible with every internal choice
```
