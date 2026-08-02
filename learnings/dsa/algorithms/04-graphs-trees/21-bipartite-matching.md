# Bipartite Matching (Hopcroft-Karp)

## Idea

A bipartite graph splits vertices into left and right groups, with edges only
between groups. A matching chooses edges that share no endpoint.

Hopcroft-Karp finds many shortest augmenting paths in one phase.

## Visual model

```text
unmatched left -> unmatched edge -> matched edge -> ... -> unmatched right
flip every edge on this path -> matching grows by one
```

## Classroom board: an augmenting path fixes a greedy choice

```text
left L1 connects R1,R2; left L2 connects only R1
greedy L1-R1 blocks L2
augmenting path L2-R1-L1-R2 flips edges
new matching: L2-R1 and L1-R2
```

## Steps

1. Store edges from left vertices to right vertices.
2. BFS layers all shortest augmenting paths from unmatched left vertices.
3. DFS follows those layers and augments disjoint paths.
4. Repeat until BFS finds no path to an unmatched right vertex.

## First-principles derivation

A matching assigns each right vertex to at most one left vertex. When a desired
right vertex is occupied, search for an alternating path that moves its current
owner elsewhere.

Flipping an augmenting path increases the matching size by exactly one while
keeping every vertex matched at most once.

## Classroom board: move one assignment

```text
left choices:
A -> {1,2}
B -> {1}
C -> {2,3}

current: A-1, C-2
try B:
B wants 1, occupied by A
A can move to 2, but 2 is occupied by C
C can move to 3, which is free

flip path:
B-1, A-2, C-3
matching grows from 2 to 3
```

## Pattern recognition

Use it for one-to-one assignment, pairing two kinds of objects, minimum path
cover reductions, or grid matching when the graph is bipartite.

## Implementation

### C++

```cpp
int hopcroftKarp(const std::vector<std::vector<int>>& graph, int rightSize) {
    std::vector<int> leftMatch(graph.size(), -1), rightMatch(rightSize, -1), distance(graph.size());
    int shortest;
    auto bfs = [&]() {
        std::queue<int> queue;
        std::fill(distance.begin(), distance.end(), -1);
        for (int left = 0; left < static_cast<int>(graph.size()); ++left) if (leftMatch[left] == -1) {
            distance[left] = 0;
            queue.push(left);
        }
        shortest = std::numeric_limits<int>::max();
        while (!queue.empty()) {
            int left = queue.front(); queue.pop();
            if (distance[left] >= shortest) continue;
            for (int right : graph[left]) {
                int nextLeft = rightMatch[right];
                if (nextLeft == -1) shortest = distance[left] + 1;
                else if (distance[nextLeft] == -1) {
                    distance[nextLeft] = distance[left] + 1;
                    queue.push(nextLeft);
                }
            }
        }
        return shortest != std::numeric_limits<int>::max();
    };
    std::function<bool(int)> dfs = [&](int left) {
        for (int right : graph[left]) {
            int nextLeft = rightMatch[right];
            if (nextLeft == -1 && distance[left] + 1 != shortest) continue;
            if (nextLeft != -1 && (distance[nextLeft] != distance[left] + 1 || !dfs(nextLeft))) continue;
            leftMatch[left] = right;
            rightMatch[right] = left;
            return true;
        }
        distance[left] = -1;
        return false;
    };
    int matching = 0;
    while (bfs()) for (int left = 0; left < static_cast<int>(graph.size()); ++left) {
        if (leftMatch[left] == -1 && dfs(left)) ++matching;
    }
    return matching;
}
```

### Python

```python
from collections import deque


def hopcroft_karp(graph: list[list[int]], right_size: int) -> int:
    left_match = [-1] * len(graph)
    right_match = [-1] * right_size
    distance = [-1] * len(graph)
    shortest = 0

    def bfs() -> bool:
        nonlocal shortest
        queue: deque[int] = deque()
        for left in range(len(graph)):
            distance[left] = 0 if left_match[left] == -1 else -1
            if left_match[left] == -1:
                queue.append(left)
        shortest = len(graph) + 1
        while queue:
            left = queue.popleft()
            if distance[left] >= shortest:
                continue
            for right in graph[left]:
                next_left = right_match[right]
                if next_left == -1:
                    shortest = distance[left] + 1
                elif distance[next_left] == -1:
                    distance[next_left] = distance[left] + 1
                    queue.append(next_left)
        return shortest <= len(graph)

    def dfs(left: int) -> bool:
        for right in graph[left]:
            next_left = right_match[right]
            if next_left == -1 and distance[left] + 1 != shortest:
                continue
            if next_left != -1 and (
                distance[next_left] != distance[left] + 1 or not dfs(next_left)
            ):
                continue
            left_match[left] = right
            right_match[right] = left
            return True
        distance[left] = -1
        return False

    matching = 0
    while bfs():
        for left in range(len(graph)):
            if left_match[left] == -1 and dfs(left):
                matching += 1
    return matching
```

### Java

```java
static int hopcroftKarp(List<List<Integer>> graph, int rightSize) {
    int[] leftMatch = new int[graph.size()];
    int[] rightMatch = new int[rightSize];
    int[] distance = new int[graph.size()];
    Arrays.fill(leftMatch, -1);
    Arrays.fill(rightMatch, -1);
    int matching = 0;
    int shortest;
    while ((shortest = matchingBfs(graph, leftMatch, rightMatch, distance)) != -1) {
        for (int left = 0; left < graph.size(); left++) {
            if (leftMatch[left] == -1
                && matchingDfs(graph, left, leftMatch, rightMatch, distance, shortest)) matching++;
        }
    }
    return matching;
}

static int matchingBfs(List<List<Integer>> graph, int[] leftMatch, int[] rightMatch, int[] distance) {
    Queue<Integer> queue = new ArrayDeque<>();
    Arrays.fill(distance, -1);
    for (int left = 0; left < graph.size(); left++) if (leftMatch[left] == -1) {
        distance[left] = 0;
        queue.add(left);
    }
    int shortest = Integer.MAX_VALUE;
    while (!queue.isEmpty()) {
        int left = queue.remove();
        if (distance[left] >= shortest) continue;
        for (int right : graph.get(left)) {
            int nextLeft = rightMatch[right];
            if (nextLeft == -1) shortest = distance[left] + 1;
            else if (distance[nextLeft] == -1) {
                distance[nextLeft] = distance[left] + 1;
                queue.add(nextLeft);
            }
        }
    }
    return shortest == Integer.MAX_VALUE ? -1 : shortest;
}

static boolean matchingDfs(
    List<List<Integer>> graph,
    int left,
    int[] leftMatch,
    int[] rightMatch,
    int[] distance,
    int shortest) {
    for (int right : graph.get(left)) {
        int nextLeft = rightMatch[right];
        if (nextLeft == -1 && distance[left] + 1 != shortest) continue;
        if (nextLeft != -1 && (distance[nextLeft] != distance[left] + 1
            || !matchingDfs(graph, nextLeft, leftMatch, rightMatch, distance, shortest))) continue;
        leftMatch[left] = right;
        rightMatch[right] = left;
        return true;
    }
    distance[left] = -1;
    return false;
}
```

## Why it works

Flipping an augmenting path increases matching size by one. A matching with no
augmenting path is maximum; BFS/DFS finds a maximal set of shortest such paths
per phase.

## Complexity

Time is `O(E sqrt(V))`; space is `O(V + E)`.

## Common mistakes

- Mixing left and right index spaces.
- Adding edges in both directions to the left adjacency lists.
- Greedily assigning once without searching augmenting paths.
