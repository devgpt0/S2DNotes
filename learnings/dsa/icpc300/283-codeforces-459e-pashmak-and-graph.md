# ICPC300 283: Codeforces 459E - Pashmak and Graph

**Source:** [Codeforces 459E - Pashmak and Graph](https://codeforces.com/problemset/problem/459/E)  
**Rating:** 2200  
**Pattern:** grouped edge-weight dynamic programming  
**Goal:** Find the maximum number of edges in a directed path whose edge
weights are strictly increasing. Vertices in the code are zero-based.

## 1. First principles

For an edge `(u,v,w)`, a valid path ending there extends the best path ending
at `u` with last weight below `w`. Sorting edges exposes all smaller weights
first. Edges of one equal-weight group must read the old DP together and write
only after every proposal is computed.

## 2. Cases that decide correctness

- Equal consecutive weights are forbidden.
- Several equal-weight edges may share endpoints.
- A single edge forms a path of length one.
- Directed cycles do not cause trouble because weights must increase.
- Parallel edges are valid input.

## 3. Brute force: scan all lighter predecessor edges

```python
def longest_increasing_edge_path_brute(
    vertex_count: int, edges: list[tuple[int, int, int]]
) -> int:
    if vertex_count <= 0 or any(
        not 0 <= start < vertex_count or not 0 <= end < vertex_count
        for start, end, _ in edges
    ):
        raise ValueError("invalid graph")

    ordered = sorted(edges, key=lambda edge: edge[2])
    lengths = [1] * len(ordered)
    for current, (start, _end, weight) in enumerate(ordered):
        lengths[current] = 1 + max(
            (
                lengths[previous]
                for previous in range(current)
                if ordered[previous][1] == start and ordered[previous][2] < weight
            ),
            default=0,
        )
    return max(lengths, default=0)
```

**Complexity:** `O(m^2)` time and `O(m)` space.

## 4. Better transition: compress histories by final vertex

After all weights below `w` are processed, only the best length ending at each
vertex matters. Every edge of weight `w` proposes `best[start] + 1` for its end.
Batching proposals prevents one weight-`w` edge from extending another.

## 5. Expert solution: sort, propose, then commit

```python
def longest_increasing_edge_path(
    vertex_count: int, edges: list[tuple[int, int, int]]
) -> int:
    if vertex_count <= 0 or any(
        not 0 <= start < vertex_count or not 0 <= end < vertex_count
        for start, end, _ in edges
    ):
        raise ValueError("invalid graph")

    ordered = sorted(edges, key=lambda edge: edge[2])
    best = [0] * vertex_count
    index = 0
    while index < len(ordered):
        group_end = index
        while group_end < len(ordered) and ordered[group_end][2] == ordered[index][2]:
            group_end += 1

        proposals: dict[int, int] = {}
        for start, end, _weight in ordered[index:group_end]:
            proposals[end] = max(proposals.get(end, 0), best[start] + 1)
        for end, length in proposals.items():
            best[end] = max(best[end], length)
        index = group_end
    return max(best, default=0)
```

### Why the expert code is correct

Before a group is committed, `best[v]` contains exactly the longest valid path
ending at `v` using smaller weights. Every path whose last weight is the
current group's weight is therefore represented by one proposal, and no
proposal can illegally consume another equal-weight edge. Induction over
weight groups proves all and only strictly increasing paths are considered.

**Complexity:** `O(m log m)` time and `O(n + m)` space.

## 6. What to remember

```text
strict edge order -> sort by weight
equal weights -> read old state together
path history -> keep only best length per ending vertex
```
