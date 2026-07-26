# Problem 22: Network Delay Time (LeetCode #743)

**Difficulty:** Medium  
**Core pattern:** Dijkstra's shortest-path algorithm

## Problem statement

Each directed edge `[from, to, time]` has a non-negative travel time. A signal
starts at node `k`. Return the time when every node has received it, or `-1` if
some node is unreachable.

## Example

```text
times = [[2,1,1], [2,3,1], [3,4,1]], n = 4, source = 2

2 --1--> 1
|
1
v
3 --1--> 4

arrival times: node 1 = 1, node 3 = 1, node 4 = 2
answer = 2
```

## Observation

The signal reaches each node at its shortest distance from `k`. Once all
shortest distances are known, the answer is their maximum.

```text
source --2--> A --3--> C
   \                       shortest arrival times
    --1--> B --1--> C      source=0, B=1, C=2, A=2

Network delay = maximum shortest arrival time
```

## Solution 1: Repeated Edge Relaxation

### Observation

Relax every edge up to `V - 1` times. This supports negative weights but costs
`O(VE)` and is unnecessary here.

### Algorithm

1. Set the source distance to `0` and all others to infinity.
2. Repeat `n - 1` times.
3. For every edge, improve the destination through the source if possible.
4. Return the maximum final distance, or `-1` for an unreachable node.

### C++ code

```cpp
class Solution {
   public:
    int networkDelayTime(vector<vector<int>>& times, int n, int source) {
        vector<int> distance(n + 1, INT_MAX);
        distance[source] = 0;

        for (int iteration = 1; iteration < n; ++iteration) {
            vector<int> nextDistance = distance;

            for (const vector<int>& edge : times) {
                int from = edge[0];
                int to = edge[1];
                int weight = edge[2];

                if (distance[from] != INT_MAX) {
                    nextDistance[to] =
                        min(nextDistance[to], distance[from] + weight);
                }
            }

            distance = move(nextDistance);
        }

        int answer = 0;
        for (int node = 1; node <= n; ++node) {
            if (distance[node] == INT_MAX) {
                return -1;
            }
            answer = max(answer, distance[node]);
        }
        return answer;
    }
};
```

### Complexity

- Time: `O(VE)`
- Space: `O(V)`

## How we derive the optimal solution

```text
Relax every edge V-1 times
          |
          v
Weights are non-negative, so the nearest unfinished node can be finalized
          |
          v
Need fast access to the smallest candidate distance
          |
          v
Use a min-heap and relax only outgoing edges
          |
          v
Dijkstra: O((V+E) log V)
```

## Optimized / CP approach: Dijkstra + min-heap

### Algorithm

1. Build an adjacency list of `(neighbor, weight)` pairs.
2. Set the source distance to `0` and every other distance to infinity.
3. Pop the smallest candidate distance from a min-heap.
4. Ignore it if it is stale (not equal to the current stored distance).
5. Relax every outgoing edge and push improved distances.
6. Return the largest distance, or `-1` if any distance is infinity.

## Heap flow

```text
pop smallest distance
        |
        +-- stale? --> skip
        |
        v
for each edge (u -> v, weight)
        |
        +-- distance[u] + weight < distance[v]
                update distance[v]
                push new pair into heap
```

### Complexity

- Time: `O((V + E) log V)`
- Space: `O(V + E)`

## Pattern to remember

```text
Single source + non-negative weighted edges + shortest paths
        => Dijkstra

Final problem asks "when do all arrive?"
        => max(all shortest distances)
```

## C++

```cpp
class Solution {
   public:
    int networkDelayTime(vector<vector<int>>& times, int nodeCount,
                         int source) {
        vector<vector<pair<int, int>>> graph(nodeCount + 1);
        for (const vector<int>& edge : times) {
            graph[edge[0]].push_back({edge[1], edge[2]});
        }

        vector<int> distance(nodeCount + 1, INT_MAX);
        priority_queue<pair<int, int>, vector<pair<int, int>>,
                       greater<pair<int, int>>>
            candidates;

        distance[source] = 0;
        candidates.push({0, source});

        while (!candidates.empty()) {
            auto [currentDistance, node] = candidates.top();
            candidates.pop();

            if (currentDistance != distance[node]) {
                continue;
            }

            for (auto [neighbor, weight] : graph[node]) {
                int nextDistance = currentDistance + weight;
                if (nextDistance < distance[neighbor]) {
                    distance[neighbor] = nextDistance;
                    candidates.push({nextDistance, neighbor});
                }
            }
        }

        int delay = 0;
        for (int node = 1; node <= nodeCount; ++node) {
            if (distance[node] == INT_MAX) {
                return -1;
            }
            delay = max(delay, distance[node]);
        }
        return delay;
    }
};
```

## Python

```python
from heapq import heappop, heappush


class Solution:
    def network_delay_time(
        self,
        times: list[list[int]],
        node_count: int,
        source: int,
    ) -> int:
        graph = [[] for _ in range(node_count + 1)]
        for start, end, weight in times:
            graph[start].append((end, weight))

        infinity = float("inf")
        distance = [infinity] * (node_count + 1)
        distance[source] = 0
        candidates = [(0, source)]

        while candidates:
            current_distance, node = heappop(candidates)
            if current_distance != distance[node]:
                continue

            for neighbor, weight in graph[node]:
                next_distance = current_distance + weight
                if next_distance < distance[neighbor]:
                    distance[neighbor] = next_distance
                    heappush(candidates, (next_distance, neighbor))

        delay = max(distance[1:])
        return -1 if delay == infinity else int(delay)
```

## Java

```java
class Solution {
    public int networkDelayTime(int[][] times, int nodeCount, int source) {
        List<List<int[]>> graph = new ArrayList<>();
        for (int node = 0; node <= nodeCount; node++) {
            graph.add(new ArrayList<>());
        }
        for (int[] edge : times) {
            graph.get(edge[0]).add(new int[] {edge[1], edge[2]});
        }

        int[] distance = new int[nodeCount + 1];
        Arrays.fill(distance, Integer.MAX_VALUE);
        distance[source] = 0;

        PriorityQueue<int[]> candidates =
            new PriorityQueue<>(Comparator.comparingInt(candidate -> candidate[0]));
        candidates.offer(new int[] {0, source});

        while (!candidates.isEmpty()) {
            int[] candidate = candidates.poll();
            int currentDistance = candidate[0];
            int node = candidate[1];

            if (currentDistance != distance[node]) {
                continue;
            }

            for (int[] edge : graph.get(node)) {
                int neighbor = edge[0];
                int nextDistance = currentDistance + edge[1];
                if (nextDistance < distance[neighbor]) {
                    distance[neighbor] = nextDistance;
                    candidates.offer(new int[] {nextDistance, neighbor});
                }
            }
        }

        int delay = 0;
        for (int node = 1; node <= nodeCount; node++) {
            if (distance[node] == Integer.MAX_VALUE) {
                return -1;
            }
            delay = Math.max(delay, distance[node]);
        }
        return delay;
    }
}
```

## Go

```go
type candidate struct {
	distance int
	node     int
}

type minHeap []candidate

func (heap minHeap) Len() int           { return len(heap) }
func (heap minHeap) Less(i, j int) bool { return heap[i].distance < heap[j].distance }
func (heap minHeap) Swap(i, j int)      { heap[i], heap[j] = heap[j], heap[i] }
func (heap *minHeap) Push(value any)    { *heap = append(*heap, value.(candidate)) }
func (heap *minHeap) Pop() any {
	old := *heap
	last := old[len(old)-1]
	*heap = old[:len(old)-1]
	return last
}

func networkDelayTime(times [][]int, nodeCount int, source int) int {
	type edge struct{ node, weight int }
	graph := make([][]edge, nodeCount+1)
	for _, item := range times {
		graph[item[0]] = append(graph[item[0]], edge{item[1], item[2]})
	}

	const infinity = int(^uint(0) >> 1)
	distance := make([]int, nodeCount+1)
	for node := 1; node <= nodeCount; node++ {
		distance[node] = infinity
	}
	distance[source] = 0

	candidates := &minHeap{{distance: 0, node: source}}
	heap.Init(candidates)

	for candidates.Len() > 0 {
		current := heap.Pop(candidates).(candidate)
		if current.distance != distance[current.node] {
			continue
		}

		for _, next := range graph[current.node] {
			nextDistance := current.distance + next.weight
			if nextDistance < distance[next.node] {
				distance[next.node] = nextDistance
				heap.Push(candidates, candidate{nextDistance, next.node})
			}
		}
	}

	delay := 0
	for node := 1; node <= nodeCount; node++ {
		if distance[node] == infinity {
			return -1
		}
		delay = max(delay, distance[node])
	}
	return delay
}
```

## Common mistakes

- Using BFS when edge weights differ.
- Marking a node permanently visited when pushed instead of when its best
  distance is popped.
- Returning the sum of distances instead of the maximum distance.
