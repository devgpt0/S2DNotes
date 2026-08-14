# 141. Tree Requests — Codeforces 570D

**Source:** [Codeforces 570D - Tree Requests](https://codeforces.com/problemset/problem/570/D)  
**Difficulty:** 2200

## 1. Problem in plain words

A rooted tree has one lowercase letter on every vertex. Query `(v, h)` takes vertices inside `v`'s subtree whose absolute depth is `h`. Answer `Yes` if their letters can be rearranged into a palindrome, otherwise `No`.

The functions use zero-based vertices, while depths match the source: the root has depth `1`.

## 2. First principles

A multiset can form a palindrome exactly when at most one letter has odd frequency. Represent frequency parity by a 26-bit XOR mask; the condition is `mask == 0` or `mask` has one set bit.

A preorder Euler tour makes a subtree an interval. For each depth, store vertices in Euler order and prefix XOR masks. Two binary searches isolate one subtree at one depth.

## 3. Cases that define correctness

- No vertex at the requested depth gives `Yes`.
- One letter always gives `Yes`.
- Counts matter only modulo two.
- Query depth is absolute, not relative to `v`.

## 4. Brute force

Traverse the requested subtree and toggle letters only at the requested depth.

```python
def tree_request_answers_brute_force(
    parents: list[int], letters: str, queries: list[tuple[int, int]]
) -> list[str]:
    size = len(parents)
    if size == 0 or len(letters) != size or parents[0] != -1:
        raise ValueError("invalid rooted tree")

    children = [[] for _ in range(size)]
    depth = [1] * size
    for vertex in range(1, size):
        parent = parents[vertex]
        if not 0 <= parent < vertex:
            raise ValueError("parents must precede their children")
        children[parent].append(vertex)
        depth[vertex] = depth[parent] + 1

    answers: list[str] = []
    for root, requested_depth in queries:
        if not 0 <= root < size or requested_depth <= 0:
            raise ValueError("invalid query")
        mask = 0
        stack = [root]
        while stack:
            vertex = stack.pop()
            if depth[vertex] == requested_depth:
                mask ^= 1 << (ord(letters[vertex]) - ord("a"))
            if depth[vertex] < requested_depth:
                stack.extend(children[vertex])
        answers.append("Yes" if mask & (mask - 1) == 0 else "No")
    return answers
```

Worst-case time is `O(nq)` and space is `O(n)`.

## 5. Better approach: Euler interval scan

Flatten the tree once. A query scans only `v`'s Euler interval and checks the stored depth of each position.

```python
def tree_request_answers_euler_scan(
    parents: list[int], letters: str, queries: list[tuple[int, int]]
) -> list[str]:
    size = len(parents)
    if size == 0 or len(letters) != size or parents[0] != -1:
        raise ValueError("invalid rooted tree")

    children = [[] for _ in range(size)]
    depth = [1] * size
    for vertex in range(1, size):
        parent = parents[vertex]
        if not 0 <= parent < vertex:
            raise ValueError("parents must precede their children")
        children[parent].append(vertex)
        depth[vertex] = depth[parent] + 1

    start = [0] * size
    end = [0] * size
    tour: list[int] = []
    stack = [(0, False)]
    while stack:
        vertex, leaving = stack.pop()
        if leaving:
            end[vertex] = len(tour) - 1
            continue
        start[vertex] = len(tour)
        tour.append(vertex)
        stack.append((vertex, True))
        for child in reversed(children[vertex]):
            stack.append((child, False))

    answers: list[str] = []
    for root, requested_depth in queries:
        if not 0 <= root < size or requested_depth <= 0:
            raise ValueError("invalid query")
        mask = 0
        for position in range(start[root], end[root] + 1):
            vertex = tour[position]
            if depth[vertex] == requested_depth:
                mask ^= 1 << (ord(letters[vertex]) - ord("a"))
        answers.append("Yes" if mask & (mask - 1) == 0 else "No")
    return answers
```

Preprocessing is `O(n)`; a query costs `O(subtree size)` and space is `O(n)`.

## 6. Expert solution: depth-indexed prefix XOR

Group Euler positions by depth. Alongside each group, store a prefix XOR of its letters. Binary searches find the positions lying inside the subtree interval.

```python
from bisect import bisect_left, bisect_right


def tree_request_answers(
    parents: list[int], letters: str, queries: list[tuple[int, int]]
) -> list[str]:
    size = len(parents)
    if size == 0 or len(letters) != size or parents[0] != -1:
        raise ValueError("invalid rooted tree")
    if any(not "a" <= letter <= "z" for letter in letters):
        raise ValueError("letters must be lowercase")

    children = [[] for _ in range(size)]
    depth = [1] * size
    for vertex in range(1, size):
        parent = parents[vertex]
        if not 0 <= parent < vertex:
            raise ValueError("parents must precede their children")
        children[parent].append(vertex)
        depth[vertex] = depth[parent] + 1

    start = [0] * size
    end = [0] * size
    tour: list[int] = []
    stack = [(0, False)]
    while stack:
        vertex, leaving = stack.pop()
        if leaving:
            end[vertex] = len(tour) - 1
            continue
        start[vertex] = len(tour)
        tour.append(vertex)
        stack.append((vertex, True))
        for child in reversed(children[vertex]):
            stack.append((child, False))

    maximum_depth = max(depth)
    positions = [[] for _ in range(maximum_depth + 1)]
    prefixes = [[0] for _ in range(maximum_depth + 1)]
    for position, vertex in enumerate(tour):
        level = depth[vertex]
        positions[level].append(position)
        prefixes[level].append(
            prefixes[level][-1] ^ (1 << (ord(letters[vertex]) - ord("a")))
        )

    answers: list[str] = []
    for root, requested_depth in queries:
        if not 0 <= root < size or requested_depth <= 0:
            raise ValueError("invalid query")
        if requested_depth > maximum_depth:
            answers.append("Yes")
            continue
        left = bisect_left(positions[requested_depth], start[root])
        right = bisect_right(positions[requested_depth], end[root])
        mask = prefixes[requested_depth][right] ^ prefixes[requested_depth][left]
        answers.append("Yes" if mask & (mask - 1) == 0 else "No")
    return answers
```

## 7. Why the expert solution is correct

Euler positions between `start[v]` and `end[v]` are exactly `v`'s subtree. Binary search intersects that interval with exactly one depth group. Prefix XOR toggles each selected letter once, producing its odd-frequency mask. A palindrome rearrangement exists exactly when that mask has at most one bit.

Time is `O(n + q log n)` and space is `O(n)`.
