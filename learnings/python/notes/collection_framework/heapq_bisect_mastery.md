# `heapq` and `bisect`
## 1. Core truth

`heapq` gives you a priority queue built on a list.
`bisect` gives you fast boundary search on a sorted list.

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

`heappop()` removes the smallest value first, and the next smallest value becomes the new root of the heap.

## 2. Heap and sorted-list foundations

### `heapq` keeps the smallest value at the front

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

The heap always keeps the smallest value at index `0`.

Practical takeaway: `heapq` is the right tool when you repeatedly need the smallest item.

### `bisect` finds boundaries in sorted data

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

`bisect_left()` finds the first position for `20`, and `bisect_right()` finds the position just after the last `20`.

Practical takeaway: use `bisect` when you need a stable insertion boundary or range count.

### `insort` inserts while keeping sort order

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

`insort()` finds the correct position and inserts the value there.

Practical takeaway: use `insort` only when the list is small enough that shifting items is still acceptable.

## 3. Heap and bisection operations

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

## 4. Practical selection patterns

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

- Use `heapq` for job schedulers, event queues, and top-k scoring.
- Use `bisect` for threshold lookups, range counts, and maintaining small sorted lists.
- Use `sorted()` when you need the full order once and not repeated priority extraction.

## 5. Correctness mistakes

### Mistake 1: Thinking a heap is a fully sorted list

A heap only guarantees the front item.

### Mistake 2: Using `bisect` on unsorted data

`bisect` assumes the list is already sorted. If it is not, the index it returns is meaningless.

### Mistake 3: Expecting `insort()` to be O(log n) overall

The search is fast, but the insertion still shifts items, so the total work is O(n).

### Mistake 4: Forgetting tie-breaking in priority queues

If two tasks can have the same priority, add a counter so the queue stays deterministic.

## 6. Selection decision guide

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

## 7. Complexity and safety

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

## 8. Advanced selection behavior

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

## 9. Mental model

| Need | Use | Remember |
| --- | --- | --- |
| Repeated min extraction | `heapq` | Smallest item stays at the front |
| Top-k results | `heapq.nlargest()` / `nsmallest()` | Better than sorting everything |
| Search sorted boundaries | `bisect_left()` / `bisect_right()` | Requires sorted input |
| Insert into sorted list | `insort()` | Still costs linear time |
| Max-heap behavior | max-heap APIs on Python 3.14+ | Largest item stays at the front |

## 10. Native max-heaps on Python 3.14+

Python 3.14 adds explicit max-heap operations, avoiding negation tricks and their
edge cases.

```python
import heapq

values = [3, 1, 4, 2]
heapq.heapify_max(values)
print(heapq.heappop_max(values))
print(values[0])
```

Output on Python 3.14+:

```text
4
3
```

Use `heappush_max`, `heappop_max`, `heappushpop_max`, and `heapreplace_max` only
when the supported runtime is Python 3.14 or newer.

## 11. Keyed bisection

`bisect` accepts `key=` for records. The key function is applied to elements in
the list but not to the search value, so pass the search key itself.

```python
from bisect import bisect_left

records = [{"score": 10}, {"score": 20}, {"score": 30}]
index = bisect_left(records, 25, key=lambda record: record["score"])
print(index)
```

Output:

```text
2
```

Repeated key computation can dominate searches. Cache keys in a parallel list
when profiling proves it matters and keep both lists updated together.
