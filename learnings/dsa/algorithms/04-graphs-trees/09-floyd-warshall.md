# Floyd-Warshall

## Idea

Floyd-Warshall finds shortest paths between every pair of vertices. It allows
negative edges but no negative cycles in the intended answer.

## Visual model

At step `k`, decide whether the best path from `i` to `j` uses vertex `k`:

```text
distance[i][j] = min(distance[i][j], distance[i][k] + distance[k][j])
```

## Classroom board: allow one new middle vertex

```text
known A->C = 10
A->B = 3 and B->C = 4
when B becomes allowed as a middle:
A->C = min(10, 3+4) = 7
```

Each outer-loop step asks one question: “Does going through this middle vertex
improve any pair?”

## Steps

1. Initialize diagonal distances to `0`, edges to their minimum weights, and
   missing edges to infinity.
2. For each intermediate vertex `k`, try it between every pair `(i, j)`.
3. A negative diagonal after completion identifies a negative cycle.

## First-principles derivation

For every pair `(i,j)`, either the best path avoids vertex `k`, or it uses
`k` and splits into `i -> k` plus `k -> j`.

After processing `k`, the invariant is that distances may use only vertices
`0..k` as intermediate vertices.

## Pattern recognition

Use it when all-pairs answers are needed and `V` is small (often at most a few
hundred), or for transitive closure with boolean operations.

## Implementation

### C++

```cpp
void floydWarshall(std::vector<std::vector<long long>>& distance) {
    const long long infinity = std::numeric_limits<long long>::max() / 4;
    const int size = distance.size();
    for (int middle = 0; middle < size; ++middle) {
        for (int from = 0; from < size; ++from) {
            if (distance[from][middle] == infinity) continue;
            for (int to = 0; to < size; ++to) {
                if (distance[middle][to] == infinity) continue;
                distance[from][to] = std::min(distance[from][to], distance[from][middle] + distance[middle][to]);
            }
        }
    }
}
```

### Python

```python
def floyd_warshall(distance: list[list[int]]) -> None:
    infinity = 10**30
    size = len(distance)
    for middle in range(size):
        for source in range(size):
            if distance[source][middle] == infinity:
                continue
            for target in range(size):
                if distance[middle][target] == infinity:
                    continue
                distance[source][target] = min(
                    distance[source][target],
                    distance[source][middle] + distance[middle][target],
                )
```

### Java

```java
static void floydWarshall(long[][] distance) {
    long infinity = Long.MAX_VALUE / 4;
    int size = distance.length;
    for (int middle = 0; middle < size; middle++) {
        for (int source = 0; source < size; source++) {
            if (distance[source][middle] == infinity) continue;
            for (int target = 0; target < size; target++) {
                if (distance[middle][target] == infinity) continue;
                distance[source][target] = Math.min(
                    distance[source][target],
                    distance[source][middle] + distance[middle][target]
                );
            }
        }
    }
}
```

## Why it works

After processing `k`, each stored path may use only vertices `0..k` as
intermediate points. The recurrence covers the two cases: skip `k`, or pass
through `k`.

## Complexity

Time is `O(V^3)` and space is `O(V^2)`.

## Common mistakes

- Failing to set `distance[i][i] = 0`.
- Overwriting parallel edges instead of keeping the minimum.
- Adding infinity values and overflowing.
- Moving the `middle` loop inside another loop; its order is essential.
