# Sliding Window

## Idea

A sliding window maintains information about one contiguous range while its
boundaries move only forward. It is usually `O(n)` because each element enters
and leaves at most once.

## Visual model

```text
[ outside | left ... valid window ... right | unseen ]
             remove <-             -> add
```

## Example: shortest subarray with sum at least `target`

This version requires **positive** values. Positivity makes the window
monotone: expanding cannot decrease its sum, and shrinking cannot increase it.

## Classroom board: shortest sum at least 7

```text
positive values = [2, 3, 1, 2, 4, 3]

right arrives     window           sum    action
2                 [2]                2    expand
3                 [2,3]              5    expand
1                 [2,3,1]            6    expand
2                 [2,3,1,2]          8    valid; best=4, remove 2
4                 [3,1,2,4]         10    shrink until invalid; best=3
3                 [4,3]              7    best=2
```

Each value enters once from the right and leaves once from the left.

## Steps

1. Move `right` forward and add the new value.
2. While the window is valid, record its answer.
3. Remove `values[left]` and move `left` forward to search for a tighter window.

## First-principles derivation

Neighboring subarrays overlap. Instead of recomputing a whole subarray, update
only the element entering and the element leaving.

The window invariant describes exactly what `[left, right)` contains and why
moving either boundary is safe.

## Pattern recognition

Use a sliding window for contiguous subarrays/substrings when adding or
removing one endpoint updates the condition cheaply and movement is monotone.

## Implementation

### C++

```cpp
int minimumLengthAtLeast(const std::vector<int>& values, long long target) {
    int answer = static_cast<int>(values.size()) + 1;
    int left = 0;
    long long sum = 0;
    for (int right = 0; right < static_cast<int>(values.size()); ++right) {
        sum += values[right];
        while (sum >= target) {
            answer = std::min(answer, right - left + 1);
            sum -= values[left++];
        }
    }
    return answer > static_cast<int>(values.size()) ? 0 : answer;
}
```

### Python

```python
def minimum_length_at_least(values: list[int], target: int) -> int:
    answer = len(values) + 1
    left = 0
    total = 0
    for right, value in enumerate(values):
        total += value
        while total >= target:
            answer = min(answer, right - left + 1)
            total -= values[left]
            left += 1
    return 0 if answer > len(values) else answer
```

### Java

```java
static int minimumLengthAtLeast(int[] values, long target) {
    int answer = values.length + 1;
    int left = 0;
    long sum = 0;
    for (int right = 0; right < values.length; right++) {
        sum += values[right];
        while (sum >= target) {
            answer = Math.min(answer, right - left + 1);
            sum -= values[left++];
        }
    }
    return answer > values.length ? 0 : answer;
}
```

## Why it works

For each right endpoint, the inner loop tries every useful left endpoint. No
discarded left endpoint can produce a shorter valid window later.

## Complexity

Time is `O(n)` and extra space is `O(1)`.

## Fixed and variable windows

- Fixed size `k`: add the arriving item and remove the item `k` positions back.
- Variable size: expand until a condition changes, then shrink while restoring
  the invariant.
- Character-frequency windows: store counts and a small “missing” or “distinct”
  counter instead of comparing whole maps.

> [!WARNING]
> A sum-based window usually fails with negative values because movement is no
> longer monotone. Consider prefix sums, a hash map, or a monotonic deque.

## Common mistakes

- Using a sum window when negative values are allowed.
- Updating the answer before the window becomes valid.
- Forgetting to remove the old left value before advancing `left`.
