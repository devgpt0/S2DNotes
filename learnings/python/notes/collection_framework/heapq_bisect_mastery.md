# `heapq` and `bisect`: Beginner-to-Expert Notes

## 1. Learning goals

By the end of this note, you should be able to:

- use `heapq` for priority-based work and top-k problems;
- use `bisect` to search and insert into sorted lists;
- explain the difference between a heap, a sorted list, and a binary search boundary;
- avoid the most common performance and correctness mistakes.

## 2. Prerequisites

- Lists, tuples, loops, and functions
- Basic sorting knowledge
- A rough idea of big-O notation

## 3. Topic at a glance

`heapq` gives you a priority queue built on a list.
`bisect` gives you fast boundary search on a sorted list.

### Minimal first example

```python
import heapq

nums = []
for value in [5, 1, 9, 3]:
    heapq.heappush(nums, value)

print(heapq.heappop(nums))
print(nums[0])
```

Output:

```text
1
3
```

Why this output?

`heappop()` removes the smallest value first, and the next smallest value becomes the new root of the heap.

Roadmap: first we build the mental model, then we learn heap and bisect operations, then we compare them, and finally we practice choosing the right tool.

## 4. Core vocabulary

| Term | Plain-language meaning | Example |
| --- | --- | --- |
| Heap | A structure that keeps the smallest item at the front | `heapq.heappush()` |
| Min-heap | A heap where the smallest value has highest priority | Python's default heap style |
| Priority queue | A queue that removes the most important item first | `heapq` |
| Binary search | A fast search method on sorted data | `bisect_left()` |
| Insertion point | The index where a value can be inserted while keeping order | `insort()` |
| Top-k | The largest or smallest k items | `nlargest(3, scores)` |

## 5. Mental model

```mermaid
flowchart TD
    A[Need repeated smallest or highest-priority item?] --> B[Use heapq]
    A --> C[Need a position inside sorted data?]
    C --> D[Use bisect]
    A --> E[Need one full sorted result once?]
    E --> F[Use sorted()]
```

Use `heapq` when you keep taking the next best item.
Use `bisect` when the data is already sorted and you need search boundaries or ordered insertion points.

## 6. Foundations

### 6.1 `heapq` keeps the smallest value at the front

```python
import heapq

heap = []
for value in [5, 1, 9, 3]:
    heapq.heappush(heap, value)

print(heapq.heappop(heap))
print(heap[0])
```

Output:

```text
1
3
```

Why this output?

The heap always keeps the smallest value at index `0`.

Practical takeaway: `heapq` is the right tool when you repeatedly need the smallest item.

### 6.2 `bisect` finds boundaries in sorted data

```python
from bisect import bisect_left, bisect_right

scores = [10, 20, 20, 30]
print(bisect_left(scores, 20))
print(bisect_right(scores, 20))
```

Output:

```text
1
3
```

Why this output?

`bisect_left()` finds the first position for `20`, and `bisect_right()` finds the position just after the last `20`.

Practical takeaway: use `bisect` when you need a stable insertion boundary or range count.

### 6.3 `insort` inserts while keeping sort order

```python
from bisect import insort

scores = [10, 20, 20, 30]
insort(scores, 25)
print(scores)
```

Output:

```text
[10, 20, 20, 25, 30]
```

Why this output?

`insort()` finds the correct position and inserts the value there.

Practical takeaway: use `insort` only when the list is small enough that shifting items is still acceptable.

## 7. How it works

### Heap behavior

`heapq` stores a heap inside a plain Python list.
The list is not fully sorted; it only guarantees that the smallest item is at the front.

### Bisect behavior

`bisect` uses binary search to find an index in a sorted list.
The search is fast, but insertion into a Python list is still linear because the items after the insertion point must move.

## 8. Core operations or methods

### `heapq.heappush()` and `heapq.heappop()`

- `heappush(heap, value)` adds a value.
- `heappop(heap)` removes the smallest value.

```python
import heapq

heap = []
heapq.heappush(heap, 4)
heapq.heappush(heap, 1)
heapq.heappush(heap, 7)

print(heapq.heappop(heap))
print(heap)
```

Output:

```text
1
[4, 7]
```

### `heapq.nlargest()` and `heapq.nsmallest()`

```python
import heapq

scores = [50, 80, 20, 90, 60, 70]
print(heapq.nlargest(3, scores))
print(heapq.nsmallest(2, scores))
```

Output:

```text
[90, 80, 70]
[20, 50]
```

### Priority queues with tie-breaking

Use a counter when two tasks can have the same priority.

```python
import heapq
from itertools import count

counter = count()
pq = []

def push(priority: int, task: str) -> None:
    heapq.heappush(pq, (priority, next(counter), task))

push(1, "payment")
push(1, "audit")

print(heapq.heappop(pq))
print(heapq.heappop(pq))
```

Output:

```text
(1, 0, 'payment')
(1, 1, 'audit')
```

### `bisect_left()` and `bisect_right()`

- `bisect_left()` finds the first valid position.
- `bisect_right()` finds the position after duplicates.

### `insort()`

- Inserts while preserving order.

## 9. Guided examples

### Example 1: Top-k leaderboard

```python
import heapq

scores = [50, 80, 20, 90, 60, 70]
top_three = heapq.nlargest(3, scores)

print(top_three)
```

Output:

```text
[90, 80, 70]
```

### Example 2: Keep a sorted list and insert a new value

```python
from bisect import insort

values = [1, 3, 5]
insort(values, 4)

print(values)
```

Output:

```text
[1, 3, 4, 5]
```

### Example 3: Count values in a numeric range

```python
from bisect import bisect_left, bisect_right

data = [1, 2, 2, 3, 5, 8]
low = 2
high = 5

count = bisect_right(data, high) - bisect_left(data, low)
print(count)
```

Output:

```text
4
```

## 10. Common patterns and real-world applications

- Use `heapq` for job schedulers, event queues, and top-k scoring.
- Use `bisect` for threshold lookups, range counts, and maintaining small sorted lists.
- Use `sorted()` when you need the full order once and not repeated priority extraction.

## 11. Common mistakes, misconceptions, and failure cases

### Mistake 1: Thinking a heap is a fully sorted list

A heap only guarantees the front item.

### Mistake 2: Using `bisect` on unsorted data

`bisect` assumes the list is already sorted. If it is not, the index it returns is meaningless.

### Mistake 3: Expecting `insort()` to be O(log n) overall

The search is fast, but the insertion still shifts items, so the total work is O(n).

### Mistake 4: Forgetting tie-breaking in priority queues

If two tasks can have the same priority, add a counter so the queue stays deterministic.

## 12. Comparison and decision guide

| Need | Best choice | Why | Avoid when |
| --- | --- | --- | --- |
| Repeated smallest-item extraction | `heapq` | Fast priority queue behavior | You only need one final sort |
| Search a position in sorted data | `bisect` | Fast boundary search | The data is unsorted |
| Insert while preserving order | `insort()` | Simple ordered insertion | The list is large and updated often |
| One complete sorted result | `sorted()` | Simpler and usually clearer | You need repeated priority operations |

Selection rule:

- Use `heapq` for ongoing priority work.
- Use `bisect` for sorted-list search and small ordered inserts.
- Use `sorted()` for one-time batch ordering.

## 13. Efficiency, limitations, safety, and best practices

| Operation | Typical cost | Note |
| --- | --- | --- |
| `heappush()` / `heappop()` | O(log n) | Good for repeated priority updates |
| `heapify()` | O(n) | Fast way to build a heap from a list |
| `bisect_left()` / `bisect_right()` | O(log n) | Search is fast |
| `insort()` | O(n) | Search is fast, but insertion shifts items |

Best practices:

- Keep the heap data structure private and mutate it only through heap operations.
- Keep the list sorted before using `bisect`.
- Use tuples carefully in heaps so comparison order is predictable.

## 14. Advanced concepts

### Max-heap in Python 3.12

Python 3.12 does not give you a public max-heap API in `heapq`.
If you need one, store negative priorities.

```python
import heapq

heap = []
for value in [4, 10, 2]:
    heapq.heappush(heap, -value)

print(-heapq.heappop(heap))
```

Output:

```text
10
```

### Range queries with `bisect`

`bisect` is a clean way to count how many items fall between two boundaries in a sorted list.

## 15. Interview or assessment knowledge

- Why use `heapq` for top-k? It avoids sorting the whole dataset when you only need a few results.
- Why use `bisect` for thresholds? It finds the boundary quickly in sorted data.
- Why not always use a heap? If you need full sorted order once, `sorted()` is simpler.

## 16. Practice exercises

1. Use `heapq` to print the smallest value from `[7, 2, 9, 1]`.
2. Use `heapq.nlargest()` to find the top 2 scores from `[5, 8, 1, 9]`.
3. Use `bisect_left()` and `bisect_right()` on `[10, 20, 20, 30]` for the value `20`.
4. Use `insort()` to insert `6` into `[1, 4, 8]`.
5. Write a priority queue that keeps `"urgent"` before `"normal"` tasks.

### Solutions

#### Solution 1

```python
import heapq

values = [7, 2, 9, 1]
heapq.heapify(values)
print(heapq.heappop(values))
```

Output:

```text
1
```

#### Solution 2

```python
import heapq

print(heapq.nlargest(2, [5, 8, 1, 9]))
```

Output:

```text
[9, 8]
```

#### Solution 3

```python
from bisect import bisect_left, bisect_right

data = [10, 20, 20, 30]
print(bisect_left(data, 20))
print(bisect_right(data, 20))
```

Output:

```text
1
3
```

#### Solution 4

```python
from bisect import insort

values = [1, 4, 8]
insort(values, 6)
print(values)
```

Output:

```text
[1, 4, 6, 8]
```

#### Solution 5

```python
import heapq
from itertools import count

order = count()
pq = []

def push(priority: int, task: str) -> None:
    heapq.heappush(pq, (priority, next(order), task))

push(0, "urgent")
push(1, "normal")
print(heapq.heappop(pq)[2])
```

Output:

```text
urgent
```

## 17. Summary cheat sheet

| Need | Use | Remember |
| --- | --- | --- |
| Repeated min extraction | `heapq` | Smallest item stays at the front |
| Top-k results | `heapq.nlargest()` / `nsmallest()` | Better than sorting everything |
| Search sorted boundaries | `bisect_left()` / `bisect_right()` | Requires sorted input |
| Insert into sorted list | `insort()` | Still costs linear time |
| Max-heap behavior | Negative values | Python 3.12 uses a min-heap by default |

## 18. Mastery checklist and next steps

- [ ] I can explain the difference between a heap and a sorted list.
- [ ] I can use `heapq` for priority queues and top-k queries.
- [ ] I can use `bisect` for binary search boundaries.
- [ ] I know why `insort()` is not a free O(log n) insertion.
- [ ] I can choose between `heapq`, `bisect`, and `sorted()` quickly.

Next topics:

- `collections` module types
- `collections.abc` and typing
- specialized sequence types
- `itertools`
