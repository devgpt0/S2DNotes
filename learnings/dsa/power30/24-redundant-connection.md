# Problem 24: Redundant Connection (LeetCode #684)

**Difficulty:** Medium  
**Core pattern:** Disjoint Set Union (Union-Find)

## Problem statement

An undirected graph started as a tree, then one extra edge was added. Return the
edge that creates the cycle.

## Example

```text
edges = [[1,2], [1,3], [2,3]]

1 ----- 2
 \     /
   \ /
    3

Edge [2,3] connects nodes that are already connected, so it is redundant.
```

## Observation

Process edges in input order. If two endpoints are already connected, adding
their edge closes a cycle. That edge is redundant.

```text
Before edge 2-3:     After edge 2-3:

1 --- 2             1 --- 2
 \                         / \
  3                       3---+

find(2) == find(3), so union(2, 3) must fail.
```

## Solution 1: DFS Before Adding Every Edge

### Observation

Before adding an edge, run DFS to see whether its endpoints are connected.
Time: `O(n^2)`.

### Algorithm

1. Start with an empty graph.
2. Before adding an edge `(u, v)`, DFS from `u` to search for `v`.
3. If `v` is already reachable, return the edge.
4. Otherwise add the edge and continue.

### C++ code

```cpp
class Solution {
   private:
    bool connected(int node, int target, const vector<vector<int>>& graph,
                   vector<bool>& visited) {
        if (node == target) {
            return true;
        }

        visited[node] = true;
        for (int neighbor : graph[node]) {
            if (!visited[neighbor] &&
                connected(neighbor, target, graph, visited)) {
                return true;
            }
        }
        return false;
    }

   public:
    vector<int> findRedundantConnection(vector<vector<int>>& edges) {
        vector<vector<int>> graph(edges.size() + 1);

        for (const vector<int>& edge : edges) {
            vector<bool> visited(edges.size() + 1, false);
            if (connected(edge[0], edge[1], graph, visited)) {
                return edge;
            }

            graph[edge[0]].push_back(edge[1]);
            graph[edge[1]].push_back(edge[0]);
        }
        return {};
    }
};
```

### Complexity

- Time: `O(n^2)`
- Space: `O(n)`

## How we derive the optimal solution

```text
Run DFS connectivity check before every edge
                 |
                 v
Only component membership is needed, not full paths
                 |
                 v
Represent each component by one root
                 |
                 v
find roots; same root means cycle, different roots get merged
                 |
                 v
Union-Find: O(n alpha(n))
```

## Optimized / CP approach: Union-Find

### Algorithm

1. Initially, each node is its own component.
2. For every edge, find both component roots.
3. If the roots match, return that edge.
4. Otherwise, merge the smaller component into the larger one.
5. Use path compression during `find`.

### Complexity

- Time: `O(n * alpha(n))`, effectively linear
- Space: `O(n)`

## Pattern to remember

```text
Edges arrive one by one + need fast connectivity/cycle checks
        => Union-Find

same root      -> edge creates a cycle
different root -> merge components
```

## C++

```cpp
class Solution {
   public:
    vector<int> findRedundantConnection(vector<vector<int>>& edges) {
        vector<int> parent(edges.size() + 1);
        vector<int> size(edges.size() + 1, 1);
        iota(parent.begin(), parent.end(), 0);

        function<int(int)> find = [&](int node) {
            if (parent[node] != node) {
                parent[node] = find(parent[node]);
            }
            return parent[node];
        };

        for (const vector<int>& edge : edges) {
            int leftRoot = find(edge[0]);
            int rightRoot = find(edge[1]);

            if (leftRoot == rightRoot) {
                return edge;
            }
            if (size[leftRoot] < size[rightRoot]) {
                swap(leftRoot, rightRoot);
            }
            parent[rightRoot] = leftRoot;
            size[leftRoot] += size[rightRoot];
        }
        return {};
    }
};
```

## Python

```python
class Solution:
    def find_redundant_connection(
        self,
        edges: list[list[int]],
    ) -> list[int]:
        parent = list(range(len(edges) + 1))
        size = [1] * (len(edges) + 1)

        def find(node: int) -> int:
            while node != parent[node]:
                parent[node] = parent[parent[node]]
                node = parent[node]
            return node

        for left, right in edges:
            left_root = find(left)
            right_root = find(right)
            if left_root == right_root:
                return [left, right]

            if size[left_root] < size[right_root]:
                left_root, right_root = right_root, left_root
            parent[right_root] = left_root
            size[left_root] += size[right_root]

        return []
```

## Java

```java
class Solution {
    public int[] findRedundantConnection(int[][] edges) {
        int[] parent = new int[edges.length + 1];
        int[] size = new int[edges.length + 1];
        for (int node = 0; node < parent.length; node++) {
            parent[node] = node;
            size[node] = 1;
        }

        for (int[] edge : edges) {
            int leftRoot = find(parent, edge[0]);
            int rightRoot = find(parent, edge[1]);
            if (leftRoot == rightRoot) {
                return edge;
            }

            if (size[leftRoot] < size[rightRoot]) {
                int temporary = leftRoot;
                leftRoot = rightRoot;
                rightRoot = temporary;
            }
            parent[rightRoot] = leftRoot;
            size[leftRoot] += size[rightRoot];
        }
        return new int[0];
    }

    private int find(int[] parent, int node) {
        if (parent[node] != node) {
            parent[node] = find(parent, parent[node]);
        }
        return parent[node];
    }
}
```

## Go

```go
func findRedundantConnection(edges [][]int) []int {
	parent := make([]int, len(edges)+1)
	size := make([]int, len(edges)+1)
	for node := range parent {
		parent[node] = node
		size[node] = 1
	}

	var find func(int) int
	find = func(node int) int {
		if parent[node] != node {
			parent[node] = find(parent[node])
		}
		return parent[node]
	}

	for _, edge := range edges {
		leftRoot := find(edge[0])
		rightRoot := find(edge[1])
		if leftRoot == rightRoot {
			return edge
		}

		if size[leftRoot] < size[rightRoot] {
			leftRoot, rightRoot = rightRoot, leftRoot
		}
		parent[rightRoot] = leftRoot
		size[leftRoot] += size[rightRoot]
	}
	return nil
}
```

## Common mistakes

- Checking roots after union instead of before it.
- Merging original nodes instead of their roots.
- Omitting path compression and union-by-size/rank.
