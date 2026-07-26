# Problem 15: Find Median from Data Stream (LeetCode #295)

**Difficulty:** Hard · **Pattern:** Two heaps

## Problem Statement

Support adding integers and returning the current median.

## Example

`addNum(1), addNum(2), findMedian()` → `1.5`; after `addNum(3)` → `2.0`.

## Observation

The median only depends on the largest value in the lower half and the smallest
value in the upper half. Two heaps expose exactly those values.

## Learning diagram

```text
max-heap lower half | median | min-heap upper half
```

## Algorithm for the optimal approach

Insert into one heap, rebalance sizes, then read one or both heap roots.

## Pattern to remember

> Online median -> two balanced heaps.

## Solution 1: Brute Force

### Observation

Store values and sort for each median request. Add: `O(1)`; median: `O(n log n)`.

### Algorithm

1. Append every incoming number to a list.
2. When the median is requested, copy and sort the list.
3. Return the middle value for odd size.
4. Average the two middle values for even size.

### C++ code

```cpp
class MedianFinder {
   private:
    vector<int> values;

   public:
    void addNum(int number) { values.push_back(number); }

    double findMedian() {
        vector<int> sorted = values;
        sort(sorted.begin(), sorted.end());

        int middle = sorted.size() / 2;
        if (sorted.size() % 2 == 1) {
            return sorted[middle];
        }
        return (sorted[middle - 1] + sorted[middle]) / 2.0;
    }
};
```

### Complexity

- `addNum`: `O(1)` amortized
- `findMedian`: `O(n log n)` time and `O(n)` space

## How we derive the optimal solution

```text
Sort all values for every median query
                |
                v
Keep values sorted after every insertion: query O(1), insert O(n)
                |
                v
Median only needs the largest lower value and smallest upper value
                |
                v
Use a max-heap for lower half and min-heap for upper half
                |
                v
Insert O(log n), median O(1)
```

## Optimized and Competitive Programming Approach — Max Heap + Min Heap

Keep the lower half in a max heap and upper half in a min heap; rebalance sizes. Add: `O(log n)`; median: `O(1)`; space: `O(n)`.

### C++

```cpp
class MedianFinder {
    priority_queue<int> lo;
    priority_queue<int, vector<int>, greater<int>> hi;

   public:
    void addNum(int x) {
        if (lo.empty() || x <= lo.top())
            lo.push(x);
        else
            hi.push(x);
        if (lo.size() > hi.size() + 1) {
            hi.push(lo.top());
            lo.pop();
        }
        if (hi.size() > lo.size()) {
            lo.push(hi.top());
            hi.pop();
        }
    }
    double findMedian() {
        return lo.size() > hi.size() ? lo.top() : (lo.top() + hi.top()) / 2.0;
    }
};
```

### Python

```python
class MedianFinder:
    def __init__(self):
        self.lower: list[int] = []
        self.upper: list[int] = []

    def add_num(self, value: int) -> None:
        heappush(self.lower, -value) if not self.lower or value <= -self.lower[
            0
        ] else heappush(self.upper, value)
        if len(self.lower) > len(self.upper) + 1:
            heappush(self.upper, -heappop(self.lower))
        if len(self.upper) > len(self.lower):
            heappush(self.lower, -heappop(self.upper))

    def find_median(self) -> float:
        return (
            -self.lower[0]
            if len(self.lower) > len(self.upper)
            else (-self.lower[0] + self.upper[0]) / 2
        )
```

### Java

```java
class MedianFinder {
    PriorityQueue<Integer> lo = new PriorityQueue<>(Comparator.reverseOrder()),
                           hi = new PriorityQueue<>();
    void addNum(int x) {
        if (lo.isEmpty() || x <= lo.peek())
            lo.offer(x);
        else
            hi.offer(x);
        if (lo.size() > hi.size() + 1)
            hi.offer(lo.poll());
        if (hi.size() > lo.size())
            lo.offer(hi.poll());
    }
    double findMedian() {
        return lo.size() > hi.size() ? lo.peek() : (lo.peek() + hi.peek()) / 2.0;
    }
}
```

### Go

```go
type intHeap struct {
	values []int
	min    bool
}

func (items intHeap) Len() int { return len(items.values) }
func (items intHeap) Less(left, right int) bool {
	if items.min {
		return items.values[left] < items.values[right]
	}
	return items.values[left] > items.values[right]
}
func (items intHeap) Swap(left, right int) {
	items.values[left], items.values[right] = items.values[right], items.values[left]
}
func (items *intHeap) Push(value any) {
	items.values = append(items.values, value.(int))
}
func (items *intHeap) Pop() any {
	last := items.values[len(items.values)-1]
	items.values = items.values[:len(items.values)-1]
	return last
}
func (items intHeap) Top() int { return items.values[0] }

type MedianFinder struct {
	lower *intHeap
	upper *intHeap
}

func NewMedianFinder() MedianFinder {
	lower := &intHeap{min: false}
	upper := &intHeap{min: true}
	heap.Init(lower)
	heap.Init(upper)
	return MedianFinder{lower: lower, upper: upper}
}

func (finder *MedianFinder) AddNum(value int) {
	if finder.lower.Len() == 0 || value <= finder.lower.Top() {
		heap.Push(finder.lower, value)
	} else {
		heap.Push(finder.upper, value)
	}

	if finder.lower.Len() > finder.upper.Len()+1 {
		heap.Push(finder.upper, heap.Pop(finder.lower))
	}
	if finder.upper.Len() > finder.lower.Len() {
		heap.Push(finder.lower, heap.Pop(finder.upper))
	}
}

func (finder *MedianFinder) FindMedian() float64 {
	if finder.lower.Len() > finder.upper.Len() {
		return float64(finder.lower.Top())
	}
	return float64(finder.lower.Top()+finder.upper.Top()) / 2.0
}
```

## Key Invariant

`lower` has either the same number of values as `upper` or exactly one more, and every lower value is at most every upper value.
