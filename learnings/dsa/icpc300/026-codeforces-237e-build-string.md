# ICPC300 026: Codeforces 237E - Build String

**Source:** [Codeforces 237E - Build String](https://codeforces.com/problemset/problem/237/E)  
**Pattern:** minimum-cost flow through character inventory

## Exact contract

Input gives a target lowercase string `t` (`1 <= |t| <= 1000`), then
`n` source strings (`1 <= n <= 100`). Source line `i` contains a lowercase
string `s[i]` and a limit `a[i]`. A character occurrence in `s[i]` may be used
at most once, at most `a[i]` total characters may be taken from that source,
and every taken character costs `i` using one-based source numbering.

Construct `t`'s multiset of characters at minimum cost. Their order is
irrelevant because selected characters can be rearranged. Output the minimum
cost, or `-1` if the required character counts cannot be supplied.

## First principles

There are two simultaneous capacities for a source string: its total limit
and the number of occurrences of each letter. A flow network expresses both:

- source to string `i`: capacity `a[i]`, cost `i`;
- string `i` to letter `c`: capacity equal to `count(c in s[i])`, cost zero;
- letter `c` to sink: capacity `count(c in t)`, cost zero.

A unit source-sink flow chooses one physical character occurrence and pays its
source number. Sending `|t|` units is exactly a valid construction.

## Cases that decide correctness

- Repeated letters require separate occurrences in source strings.
- A source may contain enough of each individual letter but still violate its
  total limit `a[i]`; both capacity layers are necessary.
- Target order does not matter, only its 26 frequencies.
- If maximum flow is below `|t|`, output `-1` rather than the cost of a partial
  construction.
- Residual reverse edges let a later augmentation replace an earlier source
  choice.

## Brute force: assign every target occurrence

```python
from collections import Counter


def build_string_brute(
    target: str,
    sources: list[tuple[str, int]],
) -> int:
    remaining_letters = [Counter(text) for text, _ in sources]
    remaining_total = [limit for _, limit in sources]
    wanted = sorted(target)
    best = 10**30

    def assign(position: int, cost: int) -> None:
        nonlocal best
        if cost >= best:
            return
        if position == len(wanted):
            best = cost
            return

        character = wanted[position]
        for source_index in range(len(sources)):
            if remaining_total[source_index] == 0:
                continue
            if remaining_letters[source_index][character] == 0:
                continue
            remaining_total[source_index] -= 1
            remaining_letters[source_index][character] -= 1
            assign(position + 1, cost + source_index + 1)
            remaining_letters[source_index][character] += 1
            remaining_total[source_index] += 1

    assign(0, 0)
    return -1 if best == 10**30 else best
```

The state records both kinds of remaining capacity, so this is correct but
exponential in `|t|`.

## Better: SPFA-based minimum-cost flow

```python
from collections import Counter, deque


def build_string_spfa(target: str, sources: list[tuple[str, int]]) -> int:
    source_node = 0
    first_string_node = 1
    first_letter_node = first_string_node + len(sources)
    sink = first_letter_node + 26
    graph: list[list[list[int]]] = [[] for _ in range(sink + 1)]

    def add_edge(start: int, end: int, capacity: int, cost: int) -> None:
        forward = [end, len(graph[end]), capacity, cost]
        backward = [start, len(graph[start]), 0, -cost]
        graph[start].append(forward)
        graph[end].append(backward)

    for source_index, (text, limit) in enumerate(sources):
        string_node = first_string_node + source_index
        add_edge(source_node, string_node, limit, source_index + 1)
        for character, count in Counter(text).items():
            add_edge(
                string_node, first_letter_node + ord(character) - ord("a"), count, 0
            )
    for character, count in Counter(target).items():
        add_edge(first_letter_node + ord(character) - ord("a"), sink, count, 0)

    flow = 0
    total_cost = 0
    infinity = 10**30
    while flow < len(target):
        distance = [infinity] * len(graph)
        parent_node = [-1] * len(graph)
        parent_edge = [-1] * len(graph)
        in_queue = [False] * len(graph)
        distance[source_node] = 0
        queue = deque([source_node])
        in_queue[source_node] = True

        while queue:
            node = queue.popleft()
            in_queue[node] = False
            for edge_index, edge in enumerate(graph[node]):
                neighbor, _, capacity, cost = edge
                candidate = distance[node] + cost
                if capacity and candidate < distance[neighbor]:
                    distance[neighbor] = candidate
                    parent_node[neighbor] = node
                    parent_edge[neighbor] = edge_index
                    if not in_queue[neighbor]:
                        in_queue[neighbor] = True
                        queue.append(neighbor)

        if distance[sink] == infinity:
            return -1

        added = len(target) - flow
        node = sink
        while node != source_node:
            previous = parent_node[node]
            added = min(added, graph[previous][parent_edge[node]][2])
            node = previous

        node = sink
        while node != source_node:
            previous = parent_node[node]
            edge = graph[previous][parent_edge[node]]
            edge[2] -= added
            graph[node][edge[1]][2] += added
            node = previous
        flow += added
        total_cost += added * distance[sink]

    return total_cost
```

SPFA handles negative residual edges directly. It is much smaller than the
brute force, but has `O(VE)` worst-case work per augmentation.

## Expert solution: potentials and Dijkstra

```python
from collections import Counter
from heapq import heappop, heappush
import sys


class CostEdge:
    __slots__ = ("to", "reverse", "capacity", "cost")

    def __init__(self, to: int, reverse: int, capacity: int, cost: int) -> None:
        self.to = to
        self.reverse = reverse
        self.capacity = capacity
        self.cost = cost


class MinCostFlow:
    def __init__(self, vertex_count: int) -> None:
        self.graph: list[list[CostEdge]] = [[] for _ in range(vertex_count)]

    def add_edge(self, start: int, end: int, capacity: int, cost: int) -> None:
        forward = CostEdge(end, len(self.graph[end]), capacity, cost)
        backward = CostEdge(start, len(self.graph[start]), 0, -cost)
        self.graph[start].append(forward)
        self.graph[end].append(backward)

    def send(self, source: int, sink: int, required: int) -> int | None:
        vertex_count = len(self.graph)
        potential = [0] * vertex_count
        flow = 0
        total_cost = 0
        infinity = 10**30

        while flow < required:
            distance = [infinity] * vertex_count
            parent_node = [-1] * vertex_count
            parent_edge = [-1] * vertex_count
            distance[source] = 0
            heap = [(0, source)]

            while heap:
                current_distance, node = heappop(heap)
                if current_distance != distance[node]:
                    continue
                for edge_index, edge in enumerate(self.graph[node]):
                    if edge.capacity == 0:
                        continue
                    reduced_cost = edge.cost + potential[node] - potential[edge.to]
                    candidate = current_distance + reduced_cost
                    if candidate < distance[edge.to]:
                        distance[edge.to] = candidate
                        parent_node[edge.to] = node
                        parent_edge[edge.to] = edge_index
                        heappush(heap, (candidate, edge.to))

            if distance[sink] == infinity:
                return None

            for vertex in range(vertex_count):
                if distance[vertex] < infinity:
                    potential[vertex] += distance[vertex]

            added = required - flow
            path_cost = 0
            node = sink
            while node != source:
                previous = parent_node[node]
                edge = self.graph[previous][parent_edge[node]]
                added = min(added, edge.capacity)
                path_cost += edge.cost
                node = previous

            node = sink
            while node != source:
                previous = parent_node[node]
                edge = self.graph[previous][parent_edge[node]]
                edge.capacity -= added
                self.graph[node][edge.reverse].capacity += added
                node = previous

            flow += added
            total_cost += added * path_cost

        return total_cost


def solve() -> None:
    input_stream = sys.stdin.buffer
    target = input_stream.readline().strip().decode()
    source_count = int(input_stream.readline())
    sources: list[tuple[str, int]] = []
    for _ in range(source_count):
        text, limit = input_stream.readline().split()
        sources.append((text.decode(), int(limit)))

    source_node = 0
    first_string_node = 1
    first_letter_node = first_string_node + source_count
    sink = first_letter_node + 26
    network = MinCostFlow(sink + 1)

    for source_index, (text, limit) in enumerate(sources):
        string_node = first_string_node + source_index
        network.add_edge(source_node, string_node, limit, source_index + 1)
        for character, count in Counter(text).items():
            letter_node = first_letter_node + ord(character) - ord("a")
            network.add_edge(string_node, letter_node, count, 0)

    for character, count in Counter(target).items():
        letter_node = first_letter_node + ord(character) - ord("a")
        network.add_edge(letter_node, sink, count, 0)

    answer = network.send(source_node, sink, len(target))
    print(-1 if answer is None else answer)


if __name__ == "__main__":
    solve()
```

Each integral flow unit is one selected occurrence. All original costs are
nonnegative, so zero initial potentials are valid; subsequent potential
updates keep every reachable reduced residual cost nonnegative for Dijkstra.

**Complexity:** `O(A E log V)` time and `O(V + E)` space, where `A` is the
number of augmentations and this network has `n + 28` vertices and at most
`26n + n + 26` forward edges.

