# Bitmask Dynamic Programming

## Idea

When `n` is small, a bitmask records which items were used. Add a small extra
dimension for the information needed to continue, such as the last vertex.

## Visual model

For traveling salesperson:

```text
dp[mask][last] = minimum cost to start at 0,
                 visit exactly mask, and finish at last
```

## Classroom board: mask remembers visited cities

```text
cities 0,1,2
mask 001: visited only city 0
move 0->2 -> mask 101, last=2
move 2->1 -> mask 111, last=1
all visited -> add cost 1->0
```

The same visited set can have different futures depending on the last city, so
`last` must be part of the state.

## Steps

1. Start at mask containing only vertex `0`.
2. For each reachable `(mask, last)`, try every unvisited next vertex.
3. Set its bit and relax the new state.
4. After all vertices are visited, add the edge back to `0`.

## First-principles derivation

When future choices depend on exactly which small set of items was used, the
subset itself must be part of the state. A bitmask stores that subset compactly.

Add any unused item to create a larger state; the invariant is that the mask
matches the items already included in the partial solution.

## Pattern recognition

Use it when `n` is roughly at most `20` and the state depends on a chosen subset
plus one small property.

## Implementation: traveling salesperson

### C++

```cpp
long long travelingSalesperson(const std::vector<std::vector<int>>& cost) {
    const int size = cost.size();
    const long long infinity = std::numeric_limits<long long>::max() / 4;
    std::vector<std::vector<long long>> dp(1 << size, std::vector<long long>(size, infinity));
    dp[1][0] = 0;
    for (int mask = 1; mask < (1 << size); ++mask) {
        for (int last = 0; last < size; ++last) if (dp[mask][last] != infinity) {
            for (int next = 0; next < size; ++next) if ((mask & (1 << next)) == 0) {
                int nextMask = mask | (1 << next);
                dp[nextMask][next] = std::min(dp[nextMask][next], dp[mask][last] + cost[last][next]);
            }
        }
    }
    long long answer = infinity;
    const int full = (1 << size) - 1;
    for (int last = 0; last < size; ++last) answer = std::min(answer, dp[full][last] + cost[last][0]);
    return answer;
}
```

### Python

```python
def traveling_salesperson(cost: list[list[int]]) -> int:
    size = len(cost)
    infinity = 10**30
    dp = [[infinity] * size for _ in range(1 << size)]
    dp[1][0] = 0
    for mask in range(1 << size):
        for last in range(size):
            if dp[mask][last] == infinity:
                continue
            for next_vertex in range(size):
                if mask & (1 << next_vertex) == 0:
                    next_mask = mask | (1 << next_vertex)
                    dp[next_mask][next_vertex] = min(
                        dp[next_mask][next_vertex],
                        dp[mask][last] + cost[last][next_vertex],
                    )
    full = (1 << size) - 1
    return min(dp[full][last] + cost[last][0] for last in range(size))
```

### Java

```java
static long travelingSalesperson(int[][] cost) {
    int size = cost.length;
    long infinity = Long.MAX_VALUE / 4;
    long[][] dp = new long[1 << size][size];
    for (long[] row : dp) Arrays.fill(row, infinity);
    dp[1][0] = 0;
    for (int mask = 0; mask < 1 << size; mask++) {
        for (int last = 0; last < size; last++) {
            if (dp[mask][last] == infinity) continue;
            for (int next = 0; next < size; next++) if ((mask & (1 << next)) == 0) {
                int nextMask = mask | (1 << next);
                dp[nextMask][next] = Math.min(dp[nextMask][next], dp[mask][last] + cost[last][next]);
            }
        }
    }
    long answer = infinity;
    int full = (1 << size) - 1;
    for (int last = 0; last < size; last++) answer = Math.min(answer, dp[full][last] + cost[last][0]);
    return answer;
}
```

## Why it works

Every tour has a unique state immediately before each next vertex. The
transition tries every possible next choice and keeps the cheapest route to
each state.

## Complexity

Time is `O(n^2 2^n)` and space is `O(n 2^n)`.

## Common mistakes

- Using it beyond feasible `n`.
- Forgetting to require the start bit.
- Omitting the final return edge when the problem asks for a cycle.
