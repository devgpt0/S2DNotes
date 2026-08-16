# Focus300 263: LeetCode 200 - Number of Islands

**Source:** [LeetCode 200](https://leetcode.com/problems/number-of-islands/)  
**Difficulty:** Medium  
**Pattern:** graph traversal / connectivity reasoning

## Exact contract

Solve the graph problem 'Number of Islands' by exploring the reachable structure and returning the required result.

## First principles

Graph problems are about connectivity, ordering, or shortest routes. Once the state space and visitation rule are explicit, BFS, DFS, or topological sorting usually reveal the answer.


## Classroom board: count connected land cells once

```text
    1 1 0
    0 1 0
    0 0 1

    the top-left cluster is one island, and the bottom-right cell is another.
```



## Step-by-step transformation

1. Choose a start state such as a cell, node, or partial path.
2. Mark the state as visited or temporarily commit the choice.
3. Expand to valid neighbors or next choices while the invariant still holds.
4. Undo the temporary choice when the branch finishes, then return the collected answer.

These problems transform the input into output by exploring one branch at a time and backtracking whenever a branch can no longer produce a valid solution.


## Diagram: search and undo

```text

            start state
                |
                v
            choose one path
                |
                v
            explore neighbors
                |
                v
            undo and try next path
                |
                v
            answer
```

These notes use search, visit markers, and backtracking to turn one starting state into the final valid path or count.

## Cases that decide correctness

- Cycles must be handled without infinite repetition.
- Disconnected components may or may not matter depending on the statement.
- Traversal order can affect the shape of the returned answer.
- A visited structure is often required to prevent repeated work.

## Brute force

```python
def num_islands_brute(grid):
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    seen = set()

    def dfs(r, c):
        if not (0 <= r < rows and 0 <= c < cols) or grid[r][c] == "0" or (r, c) in seen:
            return
        seen.add((r, c))
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    islands = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1" and (r, c) not in seen:
                islands += 1
                dfs(r, c)
    return islands
```

Re-explore the same neighborhood from scratch for every starting point.

## Better insight

Keep a visited set, queue, or indegree structure so each vertex or edge is processed once.

## Expert solution

```python
def num_islands(grid):
    rows = len(grid)
    cols = len(grid[0]) if rows else 0

    def dfs(r, c):
        if not (0 <= r < rows and 0 <= c < cols) or grid[r][c] != "1":
            return
        grid[r][c] = "0"
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    islands = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                islands += 1
                dfs(r, c)
    return islands
```

Choose the traversal style that matches the target property: BFS for layers, DFS for reachability, or topological order for dependency constraints.

**Complexity:** Usually O(V+E) time and O(V) space.
