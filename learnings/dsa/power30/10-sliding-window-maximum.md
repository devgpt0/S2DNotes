# Problem 10: Sliding Window Maximum (LeetCode #239)

**Difficulty:** Hard · **Pattern:** Monotonic deque

## Problem Statement

Return the maximum value in every contiguous window of size `k`.

## Example

`nums = [1,3,-1,-3,5,3,6,7]`, `k = 3` → `[3,3,5,5,6,7]`.

## Constraints

`1 <= nums.length <= 10^5`; `1 <= k <= nums.length`.

## Observation

An element smaller than a later value can never become a future maximum, so discard it.

## Learning diagram

```text
remove expired front -> remove smaller back -> append index -> front is maximum
```

## Algorithm for the optimal approach

Maintain indices in decreasing value order inside a deque.

## Pattern to remember

> Window extrema -> monotonic deque.

## Solution 1: Brute Force

### Observation

Scan every window. Time: `O(nk)`. Space: `O(1)` excluding output.

### Algorithm

1. Place the left boundary at every valid window start.
2. Scan the `k` values inside that window.
3. Store the largest value.
4. Move to the next window.

### C++ code

```cpp
class Solution {
   public:
    vector<int> maxSlidingWindow(vector<int>& nums, int k) {
        vector<int> answer;

        for (int left = 0; left + k <= static_cast<int>(nums.size()); ++left) {
            int maximum = nums[left];

            for (int index = left; index < left + k; ++index) {
                maximum = max(maximum, nums[index]);
            }

            answer.push_back(maximum);
        }

        return answer;
    }
};
```

### Complexity

- Time: `O(nk)`
- Space: `O(1)` excluding output

## How we derive the optimal solution

```text
Scan all k values for every window
              |
              v
Keep candidates in a max-heap
              |
              v
O(n log k), but expired items need lazy removal
              |
              v
A later larger value permanently dominates earlier smaller values
              |
              v
Remove dominated values with a monotonic deque
O(n) time, O(k) space
```

## Solution 2: Optimized (Max Heap)

Keep indexed values in a max heap and lazily discard expired indices. Time: `O(n log k)`. Space: `O(k)`.

### C++

```cpp
vector<int> maxWindowHeap(vector<int>& a, int k) {
    priority_queue<pair<int, int>> heap;
    vector<int> out;
    for (int i = 0; i < (int)a.size(); ++i) {
        heap.push({a[i], i});
        while (heap.top().second <= i - k) heap.pop();
        if (i >= k - 1) out.push_back(heap.top().first);
    }
    return out;
}
```

### Python

```python
def max_window_heap(nums: list[int], k: int) -> list[int]:
    heap: list[tuple[int, int]] = []
    answer = []
    for i, value in enumerate(nums):
        heappush(heap, (-value, i))
        while heap[0][1] <= i - k:
            heappop(heap)
        if i >= k - 1:
            answer.append(-heap[0][0])
    return answer
```

### Java

```java
int[] maxWindowHeap(int[] a, int k) {
    PriorityQueue<int[]> heap = new PriorityQueue<>((x, y) -> Integer.compare(y[0], x[0]));
    int[] out = new int[a.length - k + 1];
    for (int i = 0; i < a.length; i++) {
        heap.offer(new int[] {a[i], i});
        while (heap.peek()[1] <= i - k) heap.poll();
        if (i >= k - 1)
            out[i - k + 1] = heap.peek()[0];
    }
    return out;
}
```

### Go

```go
type windowItem struct {
	value int
	index int
}

type windowMaxHeap []windowItem

func (items windowMaxHeap) Len() int { return len(items) }
func (items windowMaxHeap) Less(left, right int) bool {
	return items[left].value > items[right].value
}
func (items windowMaxHeap) Swap(left, right int) {
	items[left], items[right] = items[right], items[left]
}
func (items *windowMaxHeap) Push(value any) {
	*items = append(*items, value.(windowItem))
}
func (items *windowMaxHeap) Pop() any {
	old := *items
	last := old[len(old)-1]
	*items = old[:len(old)-1]
	return last
}

func maxWindowHeap(nums []int, k int) []int {
	candidates := &windowMaxHeap{}
	heap.Init(candidates)
	answer := make([]int, 0, len(nums)-k+1)

	for index, value := range nums {
		heap.Push(candidates, windowItem{value: value, index: index})

		for (*candidates)[0].index <= index-k {
			heap.Pop(candidates)
		}

		if index >= k-1 {
			answer = append(answer, (*candidates)[0].value)
		}
	}
	return answer
}
```

## Approach 3 — Competitive Programming (Monotonic Deque)

Store indices in decreasing value order. Remove expired indices from front and smaller values from back. Time: `O(n)`. Space: `O(k)`.

### C++

```cpp
vector<int> maxSlidingWindow(vector<int>& a, int k) {
    deque<int> q;
    vector<int> out;
    for (int i = 0; i < (int)a.size(); ++i) {
        while (!q.empty() && q.front() <= i - k) q.pop_front();
        while (!q.empty() && a[q.back()] <= a[i]) q.pop_back();
        q.push_back(i);
        if (i >= k - 1) out.push_back(a[q.front()]);
    }
    return out;
}
```

### Python

```python
def max_sliding_window(nums: list[int], k: int) -> list[int]:
    queue: deque[int] = deque()
    answer = []
    for i, value in enumerate(nums):
        while queue and queue[0] <= i - k:
            queue.popleft()
        while queue and nums[queue[-1]] <= value:
            queue.pop()
        queue.append(i)
        if i >= k - 1:
            answer.append(nums[queue[0]])
    return answer
```

### Java

```java
int[] maxSlidingWindow(int[] a, int k) {
    Deque<Integer> queue = new ArrayDeque<>();
    int[] out = new int[a.length - k + 1];
    for (int i = 0; i < a.length; i++) {
        while (!queue.isEmpty() && queue.peekFirst() <= i - k) queue.pollFirst();
        while (!queue.isEmpty() && a[queue.peekLast()] <= a[i]) queue.pollLast();
        queue.offerLast(i);
        if (i >= k - 1)
            out[i - k + 1] = a[queue.peekFirst()];
    }
    return out;
}
```

### Go

```go
func maxSlidingWindow(a []int, k int) []int {
	queue, out := []int{}, []int{}
	for i, value := range a {
		for len(queue) > 0 && queue[0] <= i-k {
			queue = queue[1:]
		}
		for len(queue) > 0 && a[queue[len(queue)-1]] <= value {
			queue = queue[:len(queue)-1]
		}
		queue = append(queue, i)
		if i >= k-1 {
			out = append(out, a[queue[0]])
		}
	}
	return out
}
```

## Comparison

| Approach | Time | Space |
| --- | --- | --- |
| Brute force | `O(nk)` | `O(1)` |
| Heap | `O(n log k)` | `O(k)` |
| Monotonic deque | `O(n)` | `O(k)` |
