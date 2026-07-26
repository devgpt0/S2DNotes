# Problem 19: Course Schedule (LeetCode #207)

**Difficulty:** Medium  
**Core pattern:** Cycle detection with topological sort

## Problem statement

There are `numCourses` courses numbered from `0` to `numCourses - 1`.
`[course, prerequisite]` means the prerequisite must be completed first. Return
whether all courses can be completed.

## Example

```text
numCourses = 4
prerequisites = [[1,0], [2,0], [3,1], [3,2]]

0 ---> 1 ---\
 \           >---> 3
  ---> 2 ---/

One valid order: 0, 1, 2, 3
Answer: true
```

## Observation

The only reason we cannot finish is a dependency cycle:

```text
0 requires 1
1 requires 2
2 requires 0

0 -> 1 -> 2 -> 0   (no course can be taken first)
```

A course with indegree `0` has no unfinished prerequisite and is ready now.

## Kahn's algorithm diagram

```text
Build graph and indegrees
          |
          v
Queue every indegree-0 course
          |
          v
Take one course and remove its outgoing edges
          |
          +-- neighbor indegree becomes 0 --> enqueue it
          |
          v
processed courses == numCourses ?
        yes: no cycle
        no:  cycle exists
```

## Solution 1: Brute Force Cycle Search from Every Course

### Observation

Starting a new DFS from every course without sharing state repeats work and can
take `O(V * (V + E))` time.

### Algorithm

1. Build a directed prerequisite graph.
2. Start DFS independently from every course.
3. Keep only the nodes in the current DFS path.
4. A return to a current-path node proves that a cycle exists.
5. Return `false` for a cycle and `true` otherwise.

### C++ code

```cpp
class Solution {
   private:
    bool hasCycle(int course, const vector<vector<int>>& graph,
                  vector<bool>& inCurrentPath) {
        if (inCurrentPath[course]) {
            return true;
        }

        inCurrentPath[course] = true;
        for (int nextCourse : graph[course]) {
            if (hasCycle(nextCourse, graph, inCurrentPath)) {
                return true;
            }
        }
        inCurrentPath[course] = false;
        return false;
    }

   public:
    bool canFinish(int numCourses, vector<vector<int>>& prerequisites) {
        vector<vector<int>> graph(numCourses);
        for (const vector<int>& edge : prerequisites) {
            graph[edge[1]].push_back(edge[0]);
        }

        for (int course = 0; course < numCourses; ++course) {
            vector<bool> inCurrentPath(numCourses, false);
            if (hasCycle(course, graph, inCurrentPath)) {
                return false;
            }
        }
        return true;
    }
};
```

### Complexity

- Time: `O(V * (V + E))` because completed work is not remembered
- Space: `O(V + E)`

## How we derive the optimal solution

```text
Restart cycle detection from every course
                |
                v
The same dependency paths are explored repeatedly
                |
                v
Remember DFS states, or process prerequisites globally
                |
                v
Courses with indegree 0 are immediately available
                |
                v
Repeatedly remove available courses with Kahn's algorithm
O(V+E) time
```

## Optimized / CP approach: Kahn's topological sort

### Algorithm

1. Build an edge `prerequisite -> course`.
2. Count each course's indegree.
3. Put all zero-indegree courses in a queue.
4. Remove a course from the queue and count it as completed.
5. Decrement the indegree of courses that depend on it.
6. Enqueue any course whose indegree becomes zero.
7. Return whether the number completed equals `numCourses`.

### Why it works

Kahn's algorithm removes every node that can appear next in a valid order. Nodes
inside a directed cycle never reach indegree zero, so they remain unprocessed.

### Complexity

- Time: `O(V + E)`
- Space: `O(V + E)`

## Pattern to remember

```text
Prerequisites / dependencies / build order
        => directed graph

Can everything finish? => cycle detection
Need an order?          => topological sort
```

## C++

```cpp
class Solution {
   public:
    bool canFinish(int numCourses, vector<vector<int>>& prerequisites) {
        vector<vector<int>> graph(numCourses);
        vector<int> indegree(numCourses, 0);

        for (const vector<int>& edge : prerequisites) {
            int course = edge[0];
            int prerequisite = edge[1];
            graph[prerequisite].push_back(course);
            ++indegree[course];
        }

        queue<int> ready;
        for (int course = 0; course < numCourses; ++course) {
            if (indegree[course] == 0) {
                ready.push(course);
            }
        }

        int completed = 0;
        while (!ready.empty()) {
            int course = ready.front();
            ready.pop();
            ++completed;

            for (int nextCourse : graph[course]) {
                --indegree[nextCourse];
                if (indegree[nextCourse] == 0) {
                    ready.push(nextCourse);
                }
            }
        }

        return completed == numCourses;
    }
};
```

## Python

```python
from collections import deque


class Solution:
    def can_finish(
        self,
        num_courses: int,
        prerequisites: list[list[int]],
    ) -> bool:
        graph = [[] for _ in range(num_courses)]
        indegree = [0] * num_courses

        for course, prerequisite in prerequisites:
            graph[prerequisite].append(course)
            indegree[course] += 1

        ready = deque(course for course in range(num_courses) if indegree[course] == 0)

        completed = 0
        while ready:
            course = ready.popleft()
            completed += 1

            for next_course in graph[course]:
                indegree[next_course] -= 1
                if indegree[next_course] == 0:
                    ready.append(next_course)

        return completed == num_courses
```

## Java

```java
class Solution {
    public boolean canFinish(int numCourses, int[][] prerequisites) {
        List<List<Integer>> graph = new ArrayList<>();
        for (int course = 0; course < numCourses; course++) {
            graph.add(new ArrayList<>());
        }

        int[] indegree = new int[numCourses];
        for (int[] edge : prerequisites) {
            int course = edge[0];
            int prerequisite = edge[1];
            graph.get(prerequisite).add(course);
            indegree[course]++;
        }

        Queue<Integer> ready = new ArrayDeque<>();
        for (int course = 0; course < numCourses; course++) {
            if (indegree[course] == 0) {
                ready.offer(course);
            }
        }

        int completed = 0;
        while (!ready.isEmpty()) {
            int course = ready.poll();
            completed++;

            for (int nextCourse : graph.get(course)) {
                indegree[nextCourse]--;
                if (indegree[nextCourse] == 0) {
                    ready.offer(nextCourse);
                }
            }
        }

        return completed == numCourses;
    }
}
```

## Go

```go
func canFinish(numCourses int, prerequisites [][]int) bool {
	graph := make([][]int, numCourses)
	indegree := make([]int, numCourses)

	for _, edge := range prerequisites {
		course := edge[0]
		prerequisite := edge[1]
		graph[prerequisite] = append(graph[prerequisite], course)
		indegree[course]++
	}

	ready := make([]int, 0, numCourses)
	for course := 0; course < numCourses; course++ {
		if indegree[course] == 0 {
			ready = append(ready, course)
		}
	}

	completed := 0
	for head := 0; head < len(ready); head++ {
		course := ready[head]
		completed++

		for _, nextCourse := range graph[course] {
			indegree[nextCourse]--
			if indegree[nextCourse] == 0 {
				ready = append(ready, nextCourse)
			}
		}
	}

	return completed == numCourses
}
```

## Common mistakes

- Reversing the edge direction.
- Enqueuing all courses instead of only zero-indegree courses.
- Returning `true` without checking how many courses were processed.
