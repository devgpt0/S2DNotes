# ICPC300 012: CSES - Coin Collector

**Source:** [CSES - Coin Collector](https://cses.fi/problemset/task/1686/)  
**Pattern:** strongly connected components plus longest path on a DAG  
**Goal:** Start in any room, follow directed tunnels, and maximize the value of
coins collected. A room's coins count only the first time it is visited.

## 1. Problem in plain words

Cycles make an ordinary longest-path algorithm unsafe: a walk may revisit
rooms forever, but revisits add no coins. The finite object that matters is the
set of rooms collected.

If rooms `0, 1, 2` form a directed cycle with values `4, 7, 3`, entering that
cycle allows all `14` coins to be collected and still allows departure from
any suitable exit. The whole cycle can act like one weighted node.

## 2. First principles

Inside a strongly connected component (SCC), every room reaches every other
room. After entering an SCC, a walk can visit all its rooms and finish at the
tail of any outgoing tunnel. With nonnegative source coin values, collecting
the entire SCC is always optimal.

Collapse every SCC into one node whose weight is the sum of its coins. The
result cannot contain a directed cycle; otherwise those nodes would have been
one SCC. The original problem is now a maximum-weight path in a DAG.

## 3. Cases that decide correctness

| Case | Required result |
| --- | --- |
| One room | Its coin value. |
| Several disconnected regions | The walk may start in the best region. |
| A self-loop | It does not collect the room twice. |
| Parallel tunnels | They create only one useful DAG dependency. |
| A large SCC with several exits | Add its weight once, then choose the best exit. |

## 4. Brute force: remember the collected set

For tiny graphs, a state is `(current_room, collected_mask)`. There are only
`n * 2^n` such states even though walks themselves can be infinite.

```python
def maximum_coins_brute_force(coins: list[int], edges: list[tuple[int, int]]) -> int:
    room_count = len(coins)
    if room_count == 0:
        raise ValueError("at least one room is required")

    graph: list[list[int]] = [[] for _ in range(room_count)]
    for source, destination in edges:
        graph[source].append(destination)

    seen: set[tuple[int, int]] = set()
    stack = [(room, 1 << room, coins[room]) for room in range(room_count)]
    answer = max(coins)

    while stack:
        room, collected, total = stack.pop()
        state = (room, collected)
        if state in seen:
            continue
        seen.add(state)
        answer = max(answer, total)

        for neighbor in graph[room]:
            bit = 1 << neighbor
            if collected & bit:
                stack.append((neighbor, collected, total))
            else:
                stack.append((neighbor, collected | bit, total + coins[neighbor]))

    return answer
```

**Why it works:** the state records exactly the information that changes future
reward. Reaching the same room with the same collected set has the same future.

**Complexity:** `O((n + m) 2^n)` time and `O(n 2^n)` memory.

## 5. Better when the input is already a DAG

In a DAG, process rooms in topological order. `best[v]` is the largest coin sum
of a path ending at `v`. Initializing it with `coins[v]` permits starting at
any room.

```python
from collections import deque


def maximum_coins_dag(coins: list[int], edges: list[tuple[int, int]]) -> int:
    room_count = len(coins)
    graph: list[list[int]] = [[] for _ in range(room_count)]
    indegree = [0] * room_count
    for source, destination in edges:
        graph[source].append(destination)
        indegree[destination] += 1

    queue = deque(room for room in range(room_count) if indegree[room] == 0)
    best = coins.copy()
    processed = 0

    while queue:
        room = queue.popleft()
        processed += 1
        for neighbor in graph[room]:
            best[neighbor] = max(best[neighbor], best[room] + coins[neighbor])
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    if processed != room_count:
        raise ValueError("the graph is not acyclic")
    return max(best)
```

**Complexity:** `O(n + m)` time and `O(n + m)` memory. The source graph is not
guaranteed to be a DAG, so SCC contraction is still required.

## 6. Expert solution: contract SCCs, then run DAG DP

Kosaraju's two graph passes label the SCCs. Sum room values by component,
deduplicate condensation edges, and run the same topological recurrence.

```python
from collections import deque


def maximum_coins_scc(coins: list[int], edges: list[tuple[int, int]]) -> int:
    room_count = len(coins)
    if room_count == 0:
        raise ValueError("at least one room is required")

    graph: list[list[int]] = [[] for _ in range(room_count)]
    reverse_graph: list[list[int]] = [[] for _ in range(room_count)]
    for source, destination in edges:
        graph[source].append(destination)
        reverse_graph[destination].append(source)

    visited = [False] * room_count
    finish_order: list[int] = []
    for start in range(room_count):
        if visited[start]:
            continue
        visited[start] = True
        stack = [(start, 0)]
        while stack:
            room, edge_index = stack[-1]
            if edge_index == len(graph[room]):
                finish_order.append(room)
                stack.pop()
                continue
            neighbor = graph[room][edge_index]
            stack[-1] = (room, edge_index + 1)
            if not visited[neighbor]:
                visited[neighbor] = True
                stack.append((neighbor, 0))

    component = [-1] * room_count
    component_count = 0
    for start in reversed(finish_order):
        if component[start] != -1:
            continue
        component[start] = component_count
        stack = [start]
        while stack:
            room = stack.pop()
            for neighbor in reverse_graph[room]:
                if component[neighbor] == -1:
                    component[neighbor] = component_count
                    stack.append(neighbor)
        component_count += 1

    component_coins = [0] * component_count
    for room, value in enumerate(coins):
        component_coins[component[room]] += value

    dag_sets: list[set[int]] = [set() for _ in range(component_count)]
    for source, destination in edges:
        source_component = component[source]
        destination_component = component[destination]
        if source_component != destination_component:
            dag_sets[source_component].add(destination_component)

    indegree = [0] * component_count
    for neighbors in dag_sets:
        for neighbor in neighbors:
            indegree[neighbor] += 1

    queue = deque(node for node in range(component_count) if indegree[node] == 0)
    best = component_coins.copy()

    while queue:
        node = queue.popleft()
        for neighbor in dag_sets[node]:
            best[neighbor] = max(best[neighbor], best[node] + component_coins[neighbor])
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    return max(best)
```

### Why the expert code is correct

- A walk can collect every room in an entered SCC before taking its chosen exit.
- SCCs never need to be entered twice: the condensation graph is acyclic.
- Every original walk maps to a DAG path with the same collected value, and
  every condensation path can be realized by an original walk.
- Topological DP considers every possible final component and predecessor.

**Complexity:** `O(n + m)` expected time and `O(n + m)` memory. Set insertion
is expected `O(1)` and removes parallel condensation edges.

## 7. What to remember

When a directed cycle gives a one-time reward, compress mutual reachability
first. The infinite-walk problem then becomes a finite DAG path problem.
