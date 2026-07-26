# Problem 30: Minimum Cost to Connect All Points (LeetCode #1584)

**Difficulty:** Medium  
**Core pattern:** Minimum spanning tree (Prim's algorithm)

## Problem statement

Connect all points with minimum total cost. The cost between `(x1, y1)` and
`(x2, y2)` is Manhattan distance: `|x1-x2| + |y1-y2|`.

## Example

```text
points = [[0,0], [2,2], [3,10], [5,2], [7,0]]

Connect all five points with four carefully chosen Manhattan-distance edges.
Minimum total cost = 20.
```

## Observation

Every pair of points can form an edge, so this is a dense weighted graph. We
need enough edges to connect all nodes with minimum total cost: exactly a
minimum spanning tree (MST).

```text
current MST ---- cheapest crossing edge ---- unvisited point

Prim repeats this choice until every point belongs to the MST.
```

## Solution 1: Straightforward Kruskal with All Pairwise Edges

### Observation

Trying all sets of `n - 1` edges is exponential.

### Algorithm

1. Generate the Manhattan-distance edge for every pair of points.
2. Sort all edges by cost.
3. Use Union-Find to add an edge only when it joins two components.
4. Stop after selecting `n - 1` edges.

### C++ code

```cpp
class Solution {
   public:
    int minCostConnectPoints(vector<vector<int>>& points) {
        struct Edge {
            int cost;
            int left;
            int right;
        };

        vector<Edge> edges;
        for (int left = 0; left < static_cast<int>(points.size()); ++left) {
            for (int right = left + 1; right < static_cast<int>(points.size());
                 ++right) {
                int cost = abs(points[left][0] - points[right][0]) +
                           abs(points[left][1] - points[right][1]);
                edges.push_back({cost, left, right});
            }
        }
        sort(edges.begin(), edges.end(),
             [](const Edge& first, const Edge& second) {
                 return first.cost < second.cost;
             });

        vector<int> parent(points.size());
        iota(parent.begin(), parent.end(), 0);
        function<int(int)> find = [&](int node) {
            if (parent[node] != node) {
                parent[node] = find(parent[node]);
            }
            return parent[node];
        };

        int totalCost = 0;
        int usedEdges = 0;
        for (const Edge& edge : edges) {
            int leftRoot = find(edge.left);
            int rightRoot = find(edge.right);
            if (leftRoot == rightRoot) {
                continue;
            }

            parent[rightRoot] = leftRoot;
            totalCost += edge.cost;
            if (++usedEdges == static_cast<int>(points.size()) - 1) {
                break;
            }
        }
        return totalCost;
    }
};
```

### Complexity

- Time: `O(n^2 log n)` for sorting all pairwise edges
- Space: `O(n^2)` for the edge list

## How we derive the optimal solution

```text
Kruskal materializes every one of O(n^2) edges
                   |
                   v
The graph is dense, but edge costs can be calculated when needed
                   |
                   v
Grow one MST and store only each point's cheapest connection
                   |
                   v
Select the cheapest unvisited point, then relax distances
                   |
                   v
Dense Prim: O(n^2) time, O(n) space
```

The literal brute force would enumerate spanning trees and take exponential
time. Kruskal is used as the first practical solution because it follows the MST
definition directly and makes the memory improvement to dense Prim easy to see.

## Optimized / CP approach: Dense Prim

### Algorithm

1. Set point `0`'s connection cost to `0`; all others start at infinity.
2. Repeatedly choose the unvisited point with smallest connection cost.
3. Add that cost to the answer and mark the point visited.
4. Relax the Manhattan distance from it to every unvisited point.
5. Stop after adding all points.

### Why no heap?

The graph has `O(n^2)` implicit edges. A simple `O(n)` scan per selected point
gives `O(n^2)` total time and avoids building or storing all edges.

### Complexity

- Time: `O(n^2)`
- Space: `O(n)`

## Pattern to remember

```text
Connect all nodes + minimum total edge cost
        => minimum spanning tree

dense graph  -> array-based Prim is simple
sparse graph -> heap Prim or sorted-edge Kruskal
```

## C++

```cpp
class Solution {
   public:
    int minCostConnectPoints(vector<vector<int>>& points) {
        int count = points.size();
        vector<int> bestDistance(count, INT_MAX);
        vector<bool> inTree(count, false);
        bestDistance[0] = 0;

        int totalCost = 0;
        for (int added = 0; added < count; ++added) {
            int next = -1;
            for (int point = 0; point < count; ++point) {
                if (!inTree[point] &&
                    (next == -1 || bestDistance[point] < bestDistance[next])) {
                    next = point;
                }
            }

            inTree[next] = true;
            totalCost += bestDistance[next];

            for (int point = 0; point < count; ++point) {
                if (!inTree[point]) {
                    int distance = abs(points[next][0] - points[point][0]) +
                                   abs(points[next][1] - points[point][1]);
                    bestDistance[point] = min(bestDistance[point], distance);
                }
            }
        }
        return totalCost;
    }
};
```

## Python

```python
class Solution:
    def min_cost_connect_points(self, points: list[list[int]]) -> int:
        count = len(points)
        best_distance = [float("inf")] * count
        in_tree = [False] * count
        best_distance[0] = 0
        total_cost = 0

        for _ in range(count):
            next_point = min(
                (index for index in range(count) if not in_tree[index]),
                key=best_distance.__getitem__,
            )
            in_tree[next_point] = True
            total_cost += best_distance[next_point]

            x1, y1 = points[next_point]
            for point, (x2, y2) in enumerate(points):
                if not in_tree[point]:
                    distance = abs(x1 - x2) + abs(y1 - y2)
                    best_distance[point] = min(
                        best_distance[point],
                        distance,
                    )

        return int(total_cost)
```

## Java

```java
class Solution {
    public int minCostConnectPoints(int[][] points) {
        int count = points.length;
        int[] bestDistance = new int[count];
        boolean[] inTree = new boolean[count];
        Arrays.fill(bestDistance, Integer.MAX_VALUE);
        bestDistance[0] = 0;

        int totalCost = 0;
        for (int added = 0; added < count; added++) {
            int next = -1;
            for (int point = 0; point < count; point++) {
                if (!inTree[point] && (next == -1 || bestDistance[point] < bestDistance[next])) {
                    next = point;
                }
            }

            inTree[next] = true;
            totalCost += bestDistance[next];

            for (int point = 0; point < count; point++) {
                if (!inTree[point]) {
                    int distance = Math.abs(points[next][0] - points[point][0])
                        + Math.abs(points[next][1] - points[point][1]);
                    bestDistance[point] = Math.min(bestDistance[point], distance);
                }
            }
        }
        return totalCost;
    }
}
```

## Go

```go
func absolute(value int) int {
	if value < 0 {
		return -value
	}
	return value
}

func minCostConnectPoints(points [][]int) int {
	count := len(points)
	bestDistance := make([]int, count)
	inTree := make([]bool, count)
	for point := range bestDistance {
		bestDistance[point] = math.MaxInt
	}
	bestDistance[0] = 0

	totalCost := 0
	for added := 0; added < count; added++ {
		next := -1
		for point := 0; point < count; point++ {
			if !inTree[point] &&
				(next == -1 || bestDistance[point] < bestDistance[next]) {
				next = point
			}
		}

		inTree[next] = true
		totalCost += bestDistance[next]

		for point := 0; point < count; point++ {
			if !inTree[point] {
				distance := absolute(points[next][0] - points[point][0])
				distance += absolute(points[next][1] - points[point][1])
				bestDistance[point] = min(bestDistance[point], distance)
			}
		}
	}
	return totalCost
}
```

## Common mistakes

- Solving a shortest-path problem instead of an MST problem.
- Adding every pairwise edge to memory unnecessarily.
- Updating distances for points already included in the tree.
