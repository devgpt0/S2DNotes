# Monotonic Queue

## Idea

A monotonic queue is a deque of useful candidates in sorted order. For a
sliding maximum, values decrease from front to back, so the front is maximum.

## Visual model

```text
front [largest useful ... smaller useful] back
expired <- remove                 remove dominated <- new value
```

## Classroom board: window maximum, size 3

```text
values = [1, 3, 2, 5]

read 1 -> deque [1]
read 3 -> remove dominated 1; deque [3]
read 2 -> deque [3,2]       first window max = 3
read 5 -> remove 2 and 3;   deque [5]   next max = 5
```

`1` can never win after the newer `3` arrives, so keeping it would be useless.

## Steps

1. Remove the front index if it is outside the window.
2. Remove back indices whose values are no larger than the new value.
3. Add the new index.
4. Once the first window is complete, record the front value.

## First-principles derivation

A window maximum does not need every element. When a newer value is at least as
large as an older one, the older value will expire first and can never become
the maximum.

The deque stores only useful candidates in decreasing value order and
increasing index order.

## Pattern recognition

Use it for the minimum/maximum of every sliding window or a DP transition over
a moving range.

## Implementation: sliding-window maximum

### C++

```cpp
std::vector<int> windowMaximum(const std::vector<int>& values, int k) {
    std::deque<int> deque;
    std::vector<int> answer;
    for (int index = 0; index < static_cast<int>(values.size()); ++index) {
        if (!deque.empty() && deque.front() <= index - k) deque.pop_front();
        while (!deque.empty() && values[deque.back()] <= values[index]) deque.pop_back();
        deque.push_back(index);
        if (index + 1 >= k) answer.push_back(values[deque.front()]);
    }
    return answer;
}
```

### Python

```python
from collections import deque


def window_maximum(values: list[int], k: int) -> list[int]:
    candidates: deque[int] = deque()
    answer: list[int] = []
    for index, value in enumerate(values):
        if candidates and candidates[0] <= index - k:
            candidates.popleft()
        while candidates and values[candidates[-1]] <= value:
            candidates.pop()
        candidates.append(index)
        if index + 1 >= k:
            answer.append(values[candidates[0]])
    return answer
```

### Java

```java
static int[] windowMaximum(int[] values, int k) {
    int[] answer = new int[values.length - k + 1];
    int write = 0;
    Deque<Integer> candidates = new ArrayDeque<>();
    for (int index = 0; index < values.length; index++) {
        if (!candidates.isEmpty() && candidates.peekFirst() <= index - k) candidates.removeFirst();
        while (!candidates.isEmpty() && values[candidates.peekLast()] <= values[index]) candidates.removeLast();
        candidates.addLast(index);
        if (index + 1 >= k) answer[write++] = values[candidates.peekFirst()];
    }
    return answer;
}
```

## Why it works

A smaller value behind a newer larger value can never become a future maximum,
so removing it is safe. The front is therefore the largest unexpired value.

## Complexity

Time is `O(n)` and space is `O(k)`.

## Common mistakes

- Storing values instead of indices, making expiry impossible.
- Removing dominated items from the wrong end.
- Recording answers before the first full window exists.
