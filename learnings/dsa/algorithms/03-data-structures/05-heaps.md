# Heaps and Priority Queues

## Idea

A heap keeps the smallest or largest item available without fully sorting all
items. Reading the top is `O(1)`; insertion and removal are `O(log n)`.

## Visual model

```text
min-heap: every parent <= its children -> root is the minimum
```

## Classroom board: keep the three largest

```text
read 5 -> heap [5]
read 1 -> heap [1,5]
read 9 -> heap [1,5,9]
read 3 -> four values; remove smallest 1 -> heap holds 3,5,9
read 8 -> remove smallest 3            -> heap holds 5,8,9
```

The heap is not fully sorted. It only guarantees that the smallest chosen
value is available for eviction.

## Steps

For the `k` largest values:

1. Keep a min-heap of chosen values.
2. Push each value.
3. If the heap grows past `k`, remove its smallest value.
4. The heap now contains exactly the `k` largest values seen.

## First-principles derivation

Keeping all items fully sorted is unnecessary when only the smallest or largest
item is needed repeatedly. A heap stores just enough order to expose that
extreme.

The root is always the extreme item; the rest is only partially ordered.

## Pattern recognition

Use a heap for repeated best-item extraction, top `k`, merging sorted streams,
scheduling, Dijkstra, or maintaining a running median.

## Implementation: `k` largest values

### C++

```cpp
std::vector<int> kLargest(const std::vector<int>& values, int k) {
    std::priority_queue<int, std::vector<int>, std::greater<>> heap;
    for (int value : values) {
        heap.push(value);
        if (static_cast<int>(heap.size()) > k) heap.pop();
    }
    std::vector<int> answer;
    while (!heap.empty()) {
        answer.push_back(heap.top());
        heap.pop();
    }
    std::reverse(answer.begin(), answer.end());
    return answer;
}
```

### Python

```python
import heapq


def k_largest(values: list[int], k: int) -> list[int]:
    heap: list[int] = []
    for value in values:
        heapq.heappush(heap, value)
        if len(heap) > k:
            heapq.heappop(heap)
    return sorted(heap, reverse=True)
```

### Java

```java
static List<Integer> kLargest(int[] values, int k) {
    PriorityQueue<Integer> heap = new PriorityQueue<>();
    for (int value : values) {
        heap.add(value);
        if (heap.size() > k) heap.remove();
    }
    List<Integer> answer = new ArrayList<>(heap);
    answer.sort(Comparator.reverseOrder());
    return answer;
}
```

## Why it works

Whenever more than `k` candidates exist, the smallest cannot belong to the
final `k` largest, so removing it is safe.

## Complexity

Time is `O(n log k)` and heap space is `O(k)`.

## Common mistakes

- Choosing a max-heap when the smallest chosen value must be evicted.
- Assuming heap iteration is sorted.
- Forgetting stale heap entries in algorithms that push updated priorities.
