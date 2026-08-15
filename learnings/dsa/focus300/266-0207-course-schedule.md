# Focus300 266: LeetCode 207 - Course Schedule

**Source:** [LeetCode 207](https://leetcode.com/problems/course-schedule/)  
**Difficulty:** Medium  
**Pattern:** graph traversal / connectivity reasoning

## Exact contract

Solve the graph problem 'Course Schedule' by exploring the reachable structure and returning the required result.

## First principles

Graph problems are about connectivity, ordering, or shortest routes. Once the state space and visitation rule are explicit, BFS, DFS, or topological sorting usually reveal the answer.

## Cases that decide correctness

- Cycles must be handled without infinite repetition.
- Disconnected components may or may not matter depending on the statement.
- Traversal order can affect the shape of the returned answer.
- A visited structure is often required to prevent repeated work.

## Brute force

```python
def can_finish_brute(num_courses, prerequisites):
    graph = [[] for _ in range(num_courses)]
    for course, prereq in prerequisites:
        graph[course].append(prereq)

    visiting = set()
    visited = set()

    def dfs(course):
        if course in visiting:
            return False
        if course in visited:
            return True
        visiting.add(course)
        for prereq in graph[course]:
            if not dfs(prereq):
                return False
        visiting.remove(course)
        visited.add(course)
        return True

    return all(dfs(course) for course in range(num_courses))
```

Re-explore the same neighborhood from scratch for every starting point.

## Better insight

Keep a visited set, queue, or indegree structure so each vertex or edge is processed once.

## Expert solution

```python
from collections import deque, defaultdict

def can_finish(num_courses, prerequisites):
    graph = defaultdict(list)
    indegree = [0] * num_courses
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        indegree[course] += 1
    queue = deque([i for i in range(num_courses) if indegree[i] == 0])
    taken = 0
    while queue:
        course = queue.popleft()
        taken += 1
        for nxt in graph[course]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return taken == num_courses
```

Choose the traversal style that matches the target property: BFS for layers, DFS for reachability, or topological order for dependency constraints.

**Complexity:** Usually O(V+E) time and O(V) space.
