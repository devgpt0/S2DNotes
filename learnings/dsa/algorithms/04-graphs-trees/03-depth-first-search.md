# Depth-First Search (DFS)

## Idea

DFS follows one path as far as possible, then backtracks. It is the base for
components, cycles, topological order, bridges, and many tree algorithms.

## Visual model

```text
start -> child -> grandchild -> dead end -> backtrack -> next child
```

## Classroom board: follow one path fully

```text
edges: A-B, A-C, B-D

stack [A]
take A -> push B,C
take C -> no unseen neighbor; backtrack
take B -> push D
take D -> finish
```

The exact visit order can change with neighbor order; the reached component
does not.

## Steps

1. Mark a start vertex visited and put it on a stack.
2. Pop a vertex and inspect its neighbors.
3. Mark and push each unseen neighbor.
4. Repeat from every unseen vertex if all components are needed.

## First-principles derivation

To completely explore one branch before another, remember suspended branches
in last-in, first-out order. Recursion uses the call stack; iterative DFS uses
an explicit stack.

The visited set guarantees every vertex is processed at most once.

## Pattern recognition

Use DFS for complete exploration, connected components, recursive structure,
entry/exit times, or algorithms that need backtracking.

## Implementation: count components

### C++

```cpp
int countComponents(const std::vector<std::vector<int>>& graph) {
    std::vector<bool> visited(graph.size(), false);
    int components = 0;
    for (int start = 0; start < static_cast<int>(graph.size()); ++start) {
        if (visited[start]) continue;
        ++components;
        std::vector<int> stack{start};
        visited[start] = true;
        while (!stack.empty()) {
            const int vertex = stack.back();
            stack.pop_back();
            for (int neighbor : graph[vertex]) {
                if (!visited[neighbor]) {
                    visited[neighbor] = true;
                    stack.push_back(neighbor);
                }
            }
        }
    }
    return components;
}
```

### Python

```python
def count_components(graph: list[list[int]]) -> int:
    visited = [False] * len(graph)
    components = 0
    for start in range(len(graph)):
        if visited[start]:
            continue
        components += 1
        visited[start] = True
        stack = [start]
        while stack:
            vertex = stack.pop()
            for neighbor in graph[vertex]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    stack.append(neighbor)
    return components
```

### Java

```java
static int countComponents(List<List<Integer>> graph) {
    boolean[] visited = new boolean[graph.size()];
    int components = 0;
    for (int start = 0; start < graph.size(); start++) {
        if (visited[start]) continue;
        components++;
        Deque<Integer> stack = new ArrayDeque<>();
        stack.addLast(start);
        visited[start] = true;
        while (!stack.isEmpty()) {
            int vertex = stack.removeLast();
            for (int neighbor : graph.get(vertex)) {
                if (!visited[neighbor]) {
                    visited[neighbor] = true;
                    stack.addLast(neighbor);
                }
            }
        }
    }
    return components;
}
```

## Why it works

One traversal visits exactly the vertices reachable from its start. Starting
again only at unseen vertices counts each component once.

## Complexity

Time is `O(V + E)` and space is `O(V)`.

## Common mistakes

- Starting only at vertex `0` when the graph may be disconnected.
- Marking too late and pushing duplicates.
- Using recursive DFS on a path deep enough to overflow the call stack.
