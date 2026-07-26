# Problem 23: Critical Connections in a Network (LeetCode #1192)

**Difficulty:** Hard  
**Core pattern:** Tarjan bridge-finding DFS

## Problem statement

Return every edge whose removal disconnects an undirected connected network.
Such an edge is called a **bridge**.

## Example

```text
connections = [[0,1], [1,2], [2,0], [1,3]]

0 ----- 1 ----- 3
 \     /
   \ /
    2

Removing 1-3 disconnects node 3, so answer = [[1,3]].
```

## Observation

During DFS, assign each node a discovery time. `low[node]` is the earliest
discovery time reachable from that node's DFS subtree using tree edges and at
most one back edge.

```text
parent u ---- child v

low[v] <= discovery[u]  -> v's subtree can reach u or an ancestor
low[v] >  discovery[u]  -> no route back; (u, v) is a bridge
```

## Diagram

```text
0 ----- 1
 \     /
   \ /
    2 ----- 3

0-1, 1-2, 2-0 are protected by a cycle.
2-3 is the only bridge.
```

## Solution 1: Remove Every Edge and Check Connectivity

### Observation

For each edge, remove it and test connectivity with DFS/BFS. Time:
`O(E * (V + E))`.

### Algorithm

1. Give each edge an ID.
2. Ignore one edge at a time.
3. DFS/BFS from node `0` without that edge.
4. If fewer than `n` nodes are reached, the ignored edge is a bridge.

### C++ code

```cpp
class Solution {
   public:
    vector<vector<int>> criticalConnections(int n,
                                            vector<vector<int>>& connections) {
        vector<vector<pair<int, int>>> graph(n);
        for (int id = 0; id < static_cast<int>(connections.size()); ++id) {
            int left = connections[id][0];
            int right = connections[id][1];
            graph[left].push_back({right, id});
            graph[right].push_back({left, id});
        }

        vector<vector<int>> bridges;
        for (int removed = 0; removed < static_cast<int>(connections.size());
             ++removed) {
            vector<bool> visited(n, false);
            stack<int> pending;
            pending.push(0);
            visited[0] = true;
            int reached = 0;

            while (!pending.empty()) {
                int node = pending.top();
                pending.pop();
                ++reached;

                for (auto [neighbor, edgeId] : graph[node]) {
                    if (edgeId != removed && !visited[neighbor]) {
                        visited[neighbor] = true;
                        pending.push(neighbor);
                    }
                }
            }

            if (reached != n) {
                bridges.push_back(connections[removed]);
            }
        }
        return bridges;
    }
};
```

### Complexity

- Time: `O(E * (V + E))`
- Space: `O(V + E)`

## How we derive the optimal solution

```text
Remove each edge and rerun traversal
              |
              v
Most connectivity work is repeated
              |
              v
One DFS tree can record whether a child subtree reaches an ancestor
              |
              v
Track discovery time and earliest reachable time (low-link)
              |
              v
low[child] > discovery[parent] means bridge
O(V+E) time
```

## Optimized / CP approach: Discovery and low-link times

### Algorithm

1. Build an undirected adjacency list.
2. DFS from each unvisited node and assign its discovery time.
3. After visiting child `v`, update `low[u] = min(low[u], low[v])`.
4. For an already visited non-parent neighbor, update with its discovery time.
5. Record `(u, v)` when `low[v] > discovery[u]`.

### Complexity

- Time: `O(V + E)`
- Space: `O(V + E)`

## Pattern to remember

```text
"Which edges are single points of failure?"
        => bridges
        => DFS discovery time + low-link value
```

## C++

```cpp
class Solution {
   public:
    vector<vector<int>> criticalConnections(int nodeCount,
                                            vector<vector<int>>& connections) {
        vector<vector<int>> graph(nodeCount);
        for (const auto& edge : connections) {
            graph[edge[0]].push_back(edge[1]);
            graph[edge[1]].push_back(edge[0]);
        }

        vector<int> discovery(nodeCount, 0);
        vector<int> low(nodeCount, 0);
        vector<vector<int>> bridges;
        int time = 0;

        function<void(int, int)> dfs = [&](int node, int parent) {
            discovery[node] = low[node] = ++time;

            for (int neighbor : graph[node]) {
                if (neighbor == parent) {
                    continue;
                }
                if (discovery[neighbor] == 0) {
                    dfs(neighbor, node);
                    low[node] = min(low[node], low[neighbor]);
                    if (low[neighbor] > discovery[node]) {
                        bridges.push_back({node, neighbor});
                    }
                } else {
                    low[node] = min(low[node], discovery[neighbor]);
                }
            }
        };

        for (int node = 0; node < nodeCount; ++node) {
            if (discovery[node] == 0) {
                dfs(node, -1);
            }
        }
        return bridges;
    }
};
```

## Python

```python
class Solution:
    def critical_connections(
        self,
        node_count: int,
        connections: list[list[int]],
    ) -> list[list[int]]:
        graph = [[] for _ in range(node_count)]
        for left, right in connections:
            graph[left].append(right)
            graph[right].append(left)

        discovery = [0] * node_count
        low = [0] * node_count
        bridges: list[list[int]] = []
        time = 0

        def dfs(node: int, parent: int) -> None:
            nonlocal time
            time += 1
            discovery[node] = low[node] = time

            for neighbor in graph[node]:
                if neighbor == parent:
                    continue
                if discovery[neighbor] == 0:
                    dfs(neighbor, node)
                    low[node] = min(low[node], low[neighbor])
                    if low[neighbor] > discovery[node]:
                        bridges.append([node, neighbor])
                else:
                    low[node] = min(low[node], discovery[neighbor])

        for node in range(node_count):
            if discovery[node] == 0:
                dfs(node, -1)
        return bridges
```

## Java

```java
class Solution {
    private int time;

    public List<List<Integer>> criticalConnections(int nodeCount, List<List<Integer>> connections) {
        List<List<Integer>> graph = new ArrayList<>();
        for (int node = 0; node < nodeCount; node++) {
            graph.add(new ArrayList<>());
        }
        for (List<Integer> edge : connections) {
            int left = edge.get(0);
            int right = edge.get(1);
            graph.get(left).add(right);
            graph.get(right).add(left);
        }

        int[] discovery = new int[nodeCount];
        int[] low = new int[nodeCount];
        List<List<Integer>> bridges = new ArrayList<>();

        for (int node = 0; node < nodeCount; node++) {
            if (discovery[node] == 0) {
                dfs(node, -1, graph, discovery, low, bridges);
            }
        }
        return bridges;
    }

    private void dfs(int node, int parent, List<List<Integer>> graph, int[] discovery, int[] low,
        List<List<Integer>> bridges) {
        discovery[node] = low[node] = ++time;

        for (int neighbor : graph.get(node)) {
            if (neighbor == parent) {
                continue;
            }
            if (discovery[neighbor] == 0) {
                dfs(neighbor, node, graph, discovery, low, bridges);
                low[node] = Math.min(low[node], low[neighbor]);
                if (low[neighbor] > discovery[node]) {
                    bridges.add(List.of(node, neighbor));
                }
            } else {
                low[node] = Math.min(low[node], discovery[neighbor]);
            }
        }
    }
}
```

## Go

```go
func criticalConnections(nodeCount int, connections [][]int) [][]int {
	graph := make([][]int, nodeCount)
	for _, edge := range connections {
		left, right := edge[0], edge[1]
		graph[left] = append(graph[left], right)
		graph[right] = append(graph[right], left)
	}

	discovery := make([]int, nodeCount)
	low := make([]int, nodeCount)
	bridges := [][]int{}
	time := 0

	var dfs func(int, int)
	dfs = func(node, parent int) {
		time++
		discovery[node], low[node] = time, time

		for _, neighbor := range graph[node] {
			if neighbor == parent {
				continue
			}
			if discovery[neighbor] == 0 {
				dfs(neighbor, node)
				low[node] = min(low[node], low[neighbor])
				if low[neighbor] > discovery[node] {
					bridges = append(bridges, []int{node, neighbor})
				}
			} else {
				low[node] = min(low[node], discovery[neighbor])
			}
		}
	}

	for node := 0; node < nodeCount; node++ {
		if discovery[node] == 0 {
			dfs(node, -1)
		}
	}
	return bridges
}
```

## Common mistakes

- Using `low[neighbor]` instead of `discovery[neighbor]` for a back edge.
- Forgetting to skip the DFS parent edge.
- Testing `>=` instead of the strict bridge condition `>`.
