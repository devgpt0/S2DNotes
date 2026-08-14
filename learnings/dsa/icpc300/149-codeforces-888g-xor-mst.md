# 149. Xor-MST — Codeforces 888G

**Source:** [Codeforces 888G - Xor-MST](https://codeforces.com/problemset/problem/888/G)  
**Difficulty:** 2300

## 1. Problem in plain words

Each array value is a vertex. The complete graph edge between values `a` and `b` costs `a XOR b`. Find the minimum spanning tree's total weight.

Equal values remain separate vertices and can be joined with zero-cost edges.

## 2. First principles

At the highest considered bit, split values into bit-`0` and bit-`1` groups. Any edge inside one group is cheaper than every cross edge at that bit. Therefore an MST contains optimal trees inside both groups and, when both exist, one cheapest cross edge.

A binary trie finds the minimum lower-bit XOR between the two groups.

## 3. Cases that define correctness

- Zero or one vertex needs no edge.
- Duplicate values connect for cost zero.
- If all values share the current bit, simply continue to the next bit.
- A bridge between different current-bit groups always pays that bit once.

## 4. Brute force

Build all complete-graph edges and run Kruskal's algorithm.

```python
def xor_mst_weight_brute_force(values: list[int]) -> int:
    if not values or any(value < 0 for value in values):
        raise ValueError("values must be nonnegative")

    edges: list[tuple[int, int, int]] = []
    for first in range(len(values)):
        for second in range(first + 1, len(values)):
            edges.append((values[first] ^ values[second], first, second))
    edges.sort()

    parent = list(range(len(values)))

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    answer = 0
    used = 0
    for weight, first, second in edges:
        first_root = find(first)
        second_root = find(second)
        if first_root == second_root:
            continue
        parent[first_root] = second_root
        answer += weight
        used += 1
        if used == len(values) - 1:
            break
    return answer
```

Time is `O(n² log n)` and space is `O(n²)`.

## 5. Better approach: implicit Prim

Avoid storing edges. Prim repeatedly chooses the unvisited vertex with smallest known XOR connection and relaxes all remaining vertices.

```python
def xor_mst_weight_prim(values: list[int]) -> int:
    if not values or any(value < 0 for value in values):
        raise ValueError("values must be nonnegative")

    size = len(values)
    infinity = 1 << (max(values, default=0).bit_length() + 1)
    best = [infinity] * size
    best[0] = 0
    used = [False] * size
    answer = 0

    for _ in range(size):
        vertex = min(
            (index for index in range(size) if not used[index]),
            key=best.__getitem__,
        )
        used[vertex] = True
        answer += best[vertex]
        for neighbor in range(size):
            if not used[neighbor]:
                best[neighbor] = min(best[neighbor], values[vertex] ^ values[neighbor])
    return answer
```

Time is `O(n²)` and space is `O(n)`.

## 6. Expert solution: bit divide-and-conquer with tries

Sort values. Recursively solve both current-bit groups. To connect two nonempty groups, insert the smaller one into a trie of lower bits and query every value in the other for the cheapest XOR.

```python
def xor_mst_weight(values: list[int]) -> int:
    if not values or any(value < 0 for value in values):
        raise ValueError("values must be nonnegative")

    ordered = sorted(values)

    def minimum_lower_xor(
        first_left: int,
        first_right: int,
        second_left: int,
        second_right: int,
        bit: int,
    ) -> int:
        if first_right - first_left > second_right - second_left:
            first_left, second_left = second_left, first_left
            first_right, second_right = second_right, first_right

        zero_child = [-1]
        one_child = [-1]
        for index in range(first_left, first_right):
            node = 0
            for current_bit in range(bit, -1, -1):
                digit = ordered[index] >> current_bit & 1
                children = one_child if digit else zero_child
                next_node = children[node]
                if next_node == -1:
                    next_node = len(zero_child)
                    children[node] = next_node
                    zero_child.append(-1)
                    one_child.append(-1)
                node = next_node

        answer = 1 << (bit + 1) if bit >= 0 else 0
        for index in range(second_left, second_right):
            node = 0
            current_xor = 0
            for current_bit in range(bit, -1, -1):
                digit = ordered[index] >> current_bit & 1
                preferred = one_child[node] if digit else zero_child[node]
                if preferred != -1:
                    node = preferred
                else:
                    node = zero_child[node] if digit else one_child[node]
                    current_xor |= 1 << current_bit
            answer = min(answer, current_xor)
        return answer

    def solve(left: int, right: int, bit: int) -> int:
        if right - left <= 1 or bit < 0:
            return 0
        middle = left
        while middle < right and ordered[middle] >> bit & 1 == 0:
            middle += 1
        if middle == left or middle == right:
            return solve(left, right, bit - 1)
        lower = solve(left, middle, bit - 1) + solve(middle, right, bit - 1)
        bridge = (1 << bit) + minimum_lower_xor(left, middle, middle, right, bit - 1)
        return lower + bridge

    return solve(0, len(ordered), max(ordered).bit_length() - 1)
```

## 7. Why the expert solution is correct

Within a current-bit group, every edge omits that bit; every cross edge includes it. Kruskal therefore finishes the two internal minimum spanning forests before using a cross edge, and exactly one cheapest cross edge joins them. Recursing computes the two optimal internal costs, while the trie minimizes all lower bridge bits.

Time is `O(n log² A)` and temporary space is `O(n log A)` for maximum value `A`.
