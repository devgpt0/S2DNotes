# ICPC300 299: Codeforces 1746D - Paths on the Tree

**Source:** [Codeforces 1746D - Paths on the Tree](https://codeforces.com/problemset/problem/1746/D)  
**Rating:** 2200  
**Pattern:** balanced token distribution with marginal child gains  
**Goal:** Send `token_count` paths from the root through a valued tree. At each
vertex, child path counts must differ by at most one. Maximize the sum of
`value[vertex] * paths_visiting_vertex`.

## 1. First principles

If `tokens` reach a vertex with `degree` children, each child gets either
`quotient = tokens // degree` or `quotient + 1`; exactly
`remainder = tokens % degree` children get the extra token.

Compute every child's score at both counts. The base uses all quotient scores,
then the `remainder` largest marginal gains choose which children receive one
extra.

## 2. Cases that decide correctness

- A leaf keeps all arriving paths and has no distribution choice.
- Zero arriving tokens contribute zero throughout that subtree.
- Exactly the remainder number of children receive an extra token.
- A vertex can be evaluated for at most two token counts inherited from its
  parent.
- Iterative dependency evaluation avoids recursion-depth failure.

## 3. Brute force: enumerate all balanced child choices

```python
from functools import lru_cache
from itertools import combinations


def maximum_tree_path_score_brute(
    values: list[int],
    edges: list[tuple[int, int]],
    token_count: int,
) -> int:
    if (
        not values
        or any(type(value) is not int or value < 0 for value in values)
        or type(token_count) is not int
        or token_count < 0
        or len(edges) != len(values) - 1
    ):
        raise ValueError("invalid values, token count, or tree size")
    graph = [[] for _ in values]
    for first, second in edges:
        if (
            type(first) is not int
            or type(second) is not int
            or not 0 <= first < len(values)
            or not 0 <= second < len(values)
            or first == second
        ):
            raise ValueError("invalid edge")
        graph[first].append(second)
        graph[second].append(first)
    parent = [-2] * len(values)
    parent[0] = -1
    order = [0]
    for vertex in order:
        for neighbor in graph[vertex]:
            if neighbor == parent[vertex]:
                continue
            if parent[neighbor] != -2:
                raise ValueError("edges must describe a tree")
            parent[neighbor] = vertex
            order.append(neighbor)
    if len(order) != len(values):
        raise ValueError("tree must be connected")
    children = [[] for _ in values]
    for vertex in range(1, len(values)):
        children[parent[vertex]].append(vertex)

    @lru_cache(maxsize=None)
    def solve(vertex: int, tokens: int) -> int:
        score = tokens * values[vertex]
        if not children[vertex]:
            return score
        quotient, remainder = divmod(tokens, len(children[vertex]))
        best = -1
        for extra_children in combinations(children[vertex], remainder):
            extra = set(extra_children)
            candidate = score + sum(
                solve(child, quotient + (child in extra)) for child in children[vertex]
            )
            best = max(best, candidate)
        return best

    return solve(0, token_count)
```

**Complexity:** exponential in high vertex degrees.

## 4. Better approach: recompute both child scores recursively

Taking the largest marginal gains removes subset enumeration. Plain recursion
is concise, but a path-shaped source tree can exceed Python's call-stack limit.

## 5. Expert solution: iterative two-state tree DP

```python
def maximum_tree_path_score(
    values: list[int],
    edges: list[tuple[int, int]],
    token_count: int,
) -> int:
    if (
        not values
        or any(type(value) is not int or value < 0 for value in values)
        or type(token_count) is not int
        or token_count < 0
        or len(edges) != len(values) - 1
    ):
        raise ValueError("invalid values, token count, or tree size")
    graph = [[] for _ in values]
    for first, second in edges:
        if (
            type(first) is not int
            or type(second) is not int
            or not 0 <= first < len(values)
            or not 0 <= second < len(values)
            or first == second
        ):
            raise ValueError("invalid edge")
        graph[first].append(second)
        graph[second].append(first)
    parent = [-2] * len(values)
    parent[0] = -1
    order = [0]
    for vertex in order:
        for neighbor in graph[vertex]:
            if neighbor == parent[vertex]:
                continue
            if parent[neighbor] != -2:
                raise ValueError("edges must describe a tree")
            parent[neighbor] = vertex
            order.append(neighbor)
    if len(order) != len(values):
        raise ValueError("tree must be connected")
    children = [[] for _ in values]
    for vertex in range(1, len(values)):
        children[parent[vertex]].append(vertex)

    memo: dict[tuple[int, int], int] = {}
    stack = [(0, token_count, False)]
    while stack:
        vertex, tokens, expanded = stack.pop()
        state = (vertex, tokens)
        if state in memo:
            continue
        if not children[vertex]:
            memo[state] = tokens * values[vertex]
            continue
        quotient, remainder = divmod(tokens, len(children[vertex]))
        if not expanded:
            stack.append((vertex, tokens, True))
            for child in children[vertex]:
                if remainder:
                    stack.append((child, quotient + 1, False))
                stack.append((child, quotient, False))
            continue

        score = tokens * values[vertex]
        gains = []
        for child in children[vertex]:
            base_score = memo[(child, quotient)]
            score += base_score
            if remainder:
                gains.append(memo[(child, quotient + 1)] - base_score)
        score += sum(sorted(gains, reverse=True)[:remainder])
        memo[state] = score
    return memo[(0, token_count)]
```

### Why the expert code is correct

Balanced distribution fixes every child count except which `remainder`
children receive one extra. Child subproblems are independent, so choosing the
largest marginal score increases is optimal. The iterative stack evaluates
exactly those dependencies before combining them.

**Complexity:** `O(n log n)` time for sorting child gains and `O(n)` memoized
states and tree storage.

## 6. What to remember

```text
balanced distribution -> quotient or quotient plus one
base child scores -> all quotient allocations
extra tokens -> choose largest marginal subtree gains
```
