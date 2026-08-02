# Rerooting Dynamic Programming

## Idea

Rerooting computes an answer for every possible tree root without rerunning a
full DFS from each root.

## Visual model

For sum of distances, move root from parent `v` to child `c`:

```text
nodes inside c subtree: distance decreases by 1  -> -size[c]
all other nodes:        distance increases by 1  -> +(n - size[c])
answer[c] = answer[v] + n - 2 * size[c]
```

## Classroom board: move root across one edge

```text
n=5, child subtree size=2
move root parent -> child
2 subtree nodes become 1 step nearer: -2
3 other nodes become 1 step farther: +3
new answer = old answer +1 = old + n - 2*subtreeSize
```

## Steps

1. First DFS: compute subtree sizes and the answer for root `0` from depths.
2. Second DFS: move the root across each edge using the transition above.
3. Store the answer for every vertex.

## First-principles derivation

A subtree DP answers one chosen root. Rerooting derives a neighboring root's
answer by removing the neighbor's contribution from one side and adding the
rest of the tree.

Each directed edge carries the answer contributed from the side it points
away from.

## Classroom board: sum of distances from every root

```text
tree: 0 - 1 - 2 - 3

root 0 distances: 0+1+2+3 = 6
move root 0 -> 1:
subtree at 1 has 3 vertices, each becomes 1 closer
other side has 1 vertex, it becomes 1 farther
answer[1] = 6 - 3 + 1 = 4

move root 1 -> 2:
subtree at 2 has 2 vertices
answer[2] = 4 - 2 + 2 = 4

move root 2 -> 3:
answer[3] = 4 - 1 + 3 = 6
```

## Pattern recognition

Use rerooting when a tree asks for the same root-dependent result for every
vertex and neighboring-root answers differ by a small update.

## Implementation: sum of distances from every vertex

### C++

```cpp
std::vector<long long> sumOfDistances(const std::vector<std::vector<int>>& tree) {
    const int size = tree.size();
    std::vector<int> subtree(size, 1);
    std::vector<long long> answer(size, 0);
    std::function<void(int, int, int)> first = [&](int vertex, int parent, int depth) {
        answer[0] += depth;
        for (int child : tree[vertex]) if (child != parent) {
            first(child, vertex, depth + 1);
            subtree[vertex] += subtree[child];
        }
    };
    std::function<void(int, int)> second = [&](int vertex, int parent) {
        for (int child : tree[vertex]) if (child != parent) {
            answer[child] = answer[vertex] + size - 2LL * subtree[child];
            second(child, vertex);
        }
    };
    first(0, -1, 0);
    second(0, -1);
    return answer;
}
```

### Python

```python
def sum_of_distances(tree: list[list[int]]) -> list[int]:
    size = len(tree)
    subtree = [1] * size
    answer = [0] * size

    def first(vertex: int, parent: int, depth: int) -> None:
        answer[0] += depth
        for child in tree[vertex]:
            if child != parent:
                first(child, vertex, depth + 1)
                subtree[vertex] += subtree[child]

    def second(vertex: int, parent: int) -> None:
        for child in tree[vertex]:
            if child != parent:
                answer[child] = answer[vertex] + size - 2 * subtree[child]
                second(child, vertex)

    first(0, -1, 0)
    second(0, -1)
    return answer
```

### Java

```java
static long[] sumOfDistances(List<List<Integer>> tree) {
    int[] subtree = new int[tree.size()];
    Arrays.fill(subtree, 1);
    long[] answer = new long[tree.size()];
    distanceFirst(tree, 0, -1, 0, subtree, answer);
    distanceSecond(tree, 0, -1, subtree, answer);
    return answer;
}

static void distanceFirst(List<List<Integer>> tree, int vertex, int parent, int depth, int[] subtree, long[] answer) {
    answer[0] += depth;
    for (int child : tree.get(vertex)) if (child != parent) {
        distanceFirst(tree, child, vertex, depth + 1, subtree, answer);
        subtree[vertex] += subtree[child];
    }
}

static void distanceSecond(List<List<Integer>> tree, int vertex, int parent, int[] subtree, long[] answer) {
    for (int child : tree.get(vertex)) if (child != parent) {
        answer[child] = answer[vertex] + tree.size() - 2L * subtree[child];
        distanceSecond(tree, child, vertex, subtree, answer);
    }
}
```

## Why it works

The first pass gives one correct root answer. The second transition accounts
for every vertex exactly once based on which side of the moved edge it lies.

## Complexity

Time and space are `O(V)`.

## Common mistakes

- Using subtree size from the wrong original root.
- Forgetting 64-bit answers.
- Recomputing subtrees during the second pass.
