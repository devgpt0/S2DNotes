# Lowest Common Ancestor with Binary Lifting

## Idea

The lowest common ancestor (LCA) of two tree vertices is their deepest shared
ancestor. Binary lifting stores each vertex's `2^k`-th ancestor.

## Visual model

```text
up[v][0] = parent
up[v][1] = 2 steps up
up[v][2] = 4 steps up
```

## Classroom board: lift before meeting

```text
query vertices at depths 5 and 2
lift deeper vertex by 3 = binary 11 -> jump 2 then 1
depths now equal
lift both with largest jumps that keep ancestors different
their next parent is the LCA
```

## Steps

1. DFS/BFS from the root to store depth and immediate parent.
2. Build larger jumps: `up[v][k] = up[up[v][k-1]][k-1]`.
3. Lift the deeper query vertex to equal depth.
4. Lift both from largest jump down while their ancestors differ.
5. Their parent is the LCA.

## First-principles derivation

The LCA is the deepest vertex that is an ancestor of both queries. First lift
the deeper vertex to equal depth, then lift both upward while their ancestors
differ.

Binary lifting stores jumps of length `1, 2, 4, 8, ...`, turning many
one-parent moves into logarithmically many jumps.

## Classroom board: lift by powers of two

```text
        0
       / \
      1   2
     / \   \
    3   4   5
       /
      6

LCA(6,3):
depth 6 = 3, depth 3 = 2
lift 6 by 1 -> 4
parents differ: parent(4)=1 and parent(3)=1
answer = 1

LCA(6,5):
lift 6 -> 4
lift 4 and 5 until just below common ancestor
answer = 0
```

## Pattern recognition

Use it for many ancestor/path queries on a fixed tree. Path length is
`depth[a] + depth[b] - 2 * depth[lca]`.

## Implementation

### C++

```cpp
class Lca {
   public:
    Lca(const std::vector<std::vector<int>>& tree, int root) : depth_(tree.size()), levels_(1) {
        while ((1LL << levels_) <= static_cast<int>(tree.size())) ++levels_;
        up_.assign(levels_, std::vector<int>(tree.size(), root));
        std::queue<int> queue;
        std::vector<bool> visited(tree.size(), false);
        queue.push(root);
        visited[root] = true;
        while (!queue.empty()) {
            int vertex = queue.front(); queue.pop();
            for (int neighbor : tree[vertex]) if (!visited[neighbor]) {
                visited[neighbor] = true;
                depth_[neighbor] = depth_[vertex] + 1;
                up_[0][neighbor] = vertex;
                queue.push(neighbor);
            }
        }
        for (int level = 1; level < levels_; ++level) {
            for (int vertex = 0; vertex < static_cast<int>(tree.size()); ++vertex) {
                up_[level][vertex] = up_[level - 1][up_[level - 1][vertex]];
            }
        }
    }

    int query(int first, int second) const {
        if (depth_[first] < depth_[second]) std::swap(first, second);
        int difference = depth_[first] - depth_[second];
        for (int level = 0; level < levels_; ++level) if ((difference >> level) & 1) first = up_[level][first];
        if (first == second) return first;
        for (int level = levels_ - 1; level >= 0; --level) {
            if (up_[level][first] != up_[level][second]) {
                first = up_[level][first];
                second = up_[level][second];
            }
        }
        return up_[0][first];
    }

   private:
    std::vector<int> depth_;
    int levels_;
    std::vector<std::vector<int>> up_;
};
```

### Python

```python
from collections import deque


class Lca:
    def __init__(self, tree: list[list[int]], root: int) -> None:
        self.levels = max(1, len(tree).bit_length())
        self.depth = [0] * len(tree)
        self.up = [[root] * len(tree) for _ in range(self.levels)]
        visited = [False] * len(tree)
        visited[root] = True
        queue = deque([root])
        while queue:
            vertex = queue.popleft()
            for neighbor in tree[vertex]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    self.depth[neighbor] = self.depth[vertex] + 1
                    self.up[0][neighbor] = vertex
                    queue.append(neighbor)
        for level in range(1, self.levels):
            for vertex in range(len(tree)):
                self.up[level][vertex] = self.up[level - 1][self.up[level - 1][vertex]]

    def query(self, first: int, second: int) -> int:
        if self.depth[first] < self.depth[second]:
            first, second = second, first
        difference = self.depth[first] - self.depth[second]
        for level in range(self.levels):
            if difference >> level & 1:
                first = self.up[level][first]
        if first == second:
            return first
        for level in range(self.levels - 1, -1, -1):
            if self.up[level][first] != self.up[level][second]:
                first = self.up[level][first]
                second = self.up[level][second]
        return self.up[0][first]
```

### Java

```java
final class Lca {
    private final int[] depth;
    private final int[][] up;

    Lca(List<List<Integer>> tree, int root) {
        int levels = 1;
        while ((1L << levels) <= tree.size()) levels++;
        depth = new int[tree.size()];
        up = new int[levels][tree.size()];
        Arrays.fill(up[0], root);
        boolean[] visited = new boolean[tree.size()];
        Queue<Integer> queue = new ArrayDeque<>();
        visited[root] = true;
        queue.add(root);
        while (!queue.isEmpty()) {
            int vertex = queue.remove();
            for (int neighbor : tree.get(vertex)) if (!visited[neighbor]) {
                visited[neighbor] = true;
                depth[neighbor] = depth[vertex] + 1;
                up[0][neighbor] = vertex;
                queue.add(neighbor);
            }
        }
        for (int level = 1; level < levels; level++) {
            for (int vertex = 0; vertex < tree.size(); vertex++) up[level][vertex] = up[level - 1][up[level - 1][vertex]];
        }
    }

    int query(int first, int second) {
        if (depth[first] < depth[second]) { int value = first; first = second; second = value; }
        int difference = depth[first] - depth[second];
        for (int level = 0; level < up.length; level++) if (((difference >> level) & 1) == 1) first = up[level][first];
        if (first == second) return first;
        for (int level = up.length - 1; level >= 0; level--) {
            if (up[level][first] != up[level][second]) {
                first = up[level][first];
                second = up[level][second];
            }
        }
        return up[0][first];
    }
}
```

## Why it works

Binary decomposition lifts any depth difference. Largest-to-smallest joint
lifts keep both vertices below the LCA until their immediate parents match.

## Complexity

Preprocessing is `O(V log V)` time and space; each query is `O(log V)`.

## Common mistakes

- Lifting both vertices before making depths equal.
- Setting the root's parent to an invalid index.
- Using this preprocessing after tree edges change.
