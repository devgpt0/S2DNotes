# ICPC300 267: Codeforces 1151E - Number of Components

**Source:** [Codeforces 1151E - Number of Components](https://codeforces.com/problemset/problem/1151/E)  
**Rating:** 2200  
**Pattern:** sum induced-path vertices minus induced-path edges  
**Goal:** For every subarray of a permutation, take the values as vertices of
the path `0-1-...-(n-1)`. Sum the number of connected components in all those
induced subgraphs.

## 1. First principles

Every induced subgraph of a path is a forest, so

```text
components = present vertices - present edges.
```

A value at position `p` occurs in `(p + 1) * (n - p)` subarrays. The edge
between consecutive values at positions `p` and `q` occurs in every subarray
whose left endpoint is at most `min(p, q)` and right endpoint is at least
`max(p, q)`.

## 2. Cases that decide correctness

- A one-value permutation contributes one.
- Consecutive positions and consecutive values are different concepts.
- Each path edge is counted only when both endpoint values occur.
- Zero-based positions make the endpoint-choice products explicit.
- The input must be a genuine permutation.

## 3. Brute force: construct every induced value set

```python
def component_sum_brute(permutation: list[int]) -> int:
    if (
        not permutation
        or any(type(value) is not int for value in permutation)
        or sorted(permutation) != list(range(len(permutation)))
    ):
        raise ValueError("input must be a zero-based permutation")

    answer = 0
    for left in range(len(permutation)):
        present: set[int] = set()
        for right in range(left, len(permutation)):
            present.add(permutation[right])
            answer += sum(value == 0 or value - 1 not in present for value in present)
    return answer
```

**Complexity:** `O(n^3)` time and `O(n)` space.

## 4. Better approach: update components while extending a subarray

For each fixed left endpoint, adding one value changes the component count by
one minus the number of its present path neighbors. This reduces brute force to
`O(n^2)` but still visits every subarray.

## 5. Expert solution: aggregate vertex and edge lifetimes

```python
def component_sum(permutation: list[int]) -> int:
    if (
        not permutation
        or any(type(value) is not int for value in permutation)
        or sorted(permutation) != list(range(len(permutation)))
    ):
        raise ValueError("input must be a zero-based permutation")

    size = len(permutation)
    position = [0] * size
    for index, value in enumerate(permutation):
        position[value] = index

    vertex_total = sum((index + 1) * (size - index) for index in position)
    edge_total = 0
    for value in range(size - 1):
        left_position = min(position[value], position[value + 1])
        right_position = max(position[value], position[value + 1])
        edge_total += (left_position + 1) * (size - right_position)
    return vertex_total - edge_total
```

### Why the expert code is correct

Summing `vertices - edges` over all induced subgraphs can be reordered into one
contribution per value and one subtraction per consecutive-value edge. The two
endpoint products count exactly the subarrays containing each object, so their
difference is the requested component total.

**Complexity:** `O(n log n)` time for permutation validation, `O(n)` after
validation, and `O(n)` space.

## 6. What to remember

```text
induced subgraph of a path -> forest
forest components -> vertices minus edges
sum over subarrays -> count each vertex and edge lifetime
```
