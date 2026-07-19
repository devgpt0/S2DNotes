# `heapq` and `bisect` Mastery

These tools are essential for collection-heavy problem solving and performance-aware code.

## 1) `heapq` Mental Model

Python heap is a min-heap stored in a list:
- smallest element is always at index 0.
- push/pop operations are O(log n).
- heap creation (`heapify`) is O(n).

```python
import heapq

nums = [5, 1, 9, 3]
heapq.heapify(nums)
print(nums[0])  # smallest
```

## 2) Core Heap Operations

```python
import heapq

h = []
heapq.heappush(h, 4)
heapq.heappush(h, 1)
heapq.heappush(h, 7)
print(heapq.heappop(h))  # 1
```

Useful combined operations:
- `heappushpop(heap, x)`
- `heapreplace(heap, x)`

## 3) Top-K Patterns

```python
import heapq

scores = [50, 80, 20, 90, 60, 70]
print(heapq.nlargest(3, scores))   # [90, 80, 70]
print(heapq.nsmallest(2, scores))  # [20, 50]
```

Use cases:
- top-k leaderboard
- smallest k latency values
- streaming ranking

## 4) Max-Heap Pattern in Python

Python default is min-heap. Max-heap is usually simulated by negating values.

```python
import heapq

h = []
for x in [4, 10, 2]:
    heapq.heappush(h, -x)
print(-heapq.heappop(h))  # 10
```

## 5) Priority Queue with Tie-Breaking

```python
import heapq
from itertools import count

counter = count()
pq = []

def push(priority, task):
    heapq.heappush(pq, (priority, next(counter), task))

push(2, "email")
push(1, "payment")
push(1, "audit")
print(heapq.heappop(pq))  # stable tie-breaking by insertion counter
```

## 6) `bisect` Mental Model

`bisect` does binary search on sorted lists.
- search is O(log n)
- insertion into list remains O(n) due to shifting

```python
from bisect import bisect_left, bisect_right

arr = [10, 20, 20, 30]
print(bisect_left(arr, 20))   # 1
print(bisect_right(arr, 20))  # 3
```

## 7) Sorted Insert with `insort`

```python
from bisect import insort

arr = [1, 3, 5]
insort(arr, 4)
print(arr)  # [1, 3, 4, 5]
```

Good for:
- moderate-size continuously sorted lists
- maintaining quantiles/threshold slices in simple systems

## 8) Range Query Pattern with `bisect`

Count values in [low, high]:

```python
from bisect import bisect_left, bisect_right

arr = [1, 2, 2, 3, 5, 8]
low, high = 2, 5
count = bisect_right(arr, high) - bisect_left(arr, low)
print(count)  # 4
```

## 9) Choosing Heap vs Bisect vs Sort

- one-time order + batch processing: `sorted()`
- repeated top-priority extraction: `heapq`
- repeated binary search/range position in sorted list: `bisect`

## 10) Common Pitfalls

- forgetting heap is not fully sorted list.
- using `bisect` on unsorted lists.
- assuming `bisect` insertion is O(log n) overall (it is O(n) due to shift).
- inconsistent tuple key ordering in heap priorities.

## 11) Interview Quick Answers

1. Why heap for top-k?
   Keeps only needed candidates, efficient repeated extraction.
2. Why bisect for thresholds?
   Fast boundary index search in sorted data.
3. Why not always use heap?
   If full sorted order is needed once, plain sort may be simpler.
