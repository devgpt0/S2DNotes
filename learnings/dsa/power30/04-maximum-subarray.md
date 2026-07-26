# Problem 4: Maximum Subarray (LeetCode #53)

**Difficulty:** Medium · **Pattern:** Kadane's algorithm

## Problem Statement

Return the largest sum of a non-empty contiguous subarray.

## Example

`nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]` → `6` from `[4, -1, 2, 1]`.

## Constraints

`1 <= nums.length <= 10^5`; values fit in a signed 32-bit integer.

## Observation

A negative running sum can never improve a future subarray, so discard it.

## Learning diagram

```text
current = max(value, current + value) -> best = max(best, current)
```

## Algorithm for the optimal approach

At each value, either restart the subarray or extend the best subarray ending before it.

## Pattern to remember

> Best range ending here -> extend or restart.

## Solution 1: Brute Force

### Observation

Start at every index and extend a running sum. Time: `O(n^2)`. Space: `O(1)`.

### Algorithm

1. Choose every index as a possible subarray start.
2. Extend the subarray one position at a time.
3. Maintain its running sum instead of recomputing it.
4. Update the best sum after every extension.

### C++ code

```cpp
class Solution {
   public:
    int maxSubArray(vector<int>& nums) {
        int best = nums[0];

        for (int start = 0; start < static_cast<int>(nums.size()); ++start) {
            int sum = 0;
            for (int end = start; end < static_cast<int>(nums.size()); ++end) {
                sum += nums[end];
                best = max(best, sum);
            }
        }

        return best;
    }
};
```

### Complexity

- Time: `O(n^2)`
- Space: `O(1)`

## How we derive the optimal solution

```text
Enumerate every start and end
          |
          v
At index i, ask only for the best subarray ending at i
          |
          v
Either extend the previous subarray or restart at nums[i]
          |
          v
Store every ending answer in dp[]
          |
          v
Observe that only dp[i-1] is needed
          |
          v
Kadane: O(n) time, O(1) space
```

## Solution 2: Optimized (DP Array)

Store the best subarray sum ending at every index. Time: `O(n)`. Space: `O(n)`.

### C++

```cpp
int maxSubArrayDp(vector<int>& a) {
    vector<int> dp = a;
    for (int i = 1; i < (int)a.size(); ++i) dp[i] = max(a[i], a[i] + dp[i - 1]);
    return *max_element(dp.begin(), dp.end());
}
```

### Python

```python
def max_subarray_dp(nums: list[int]) -> int:
    dp = nums[:]
    for i in range(1, len(nums)):
        dp[i] = max(nums[i], nums[i] + dp[i - 1])
    return max(dp)
```

### Java

```java
int maxSubArrayDp(int[] a) {
    int[] dp = a.clone();
    int best = dp[0];
    for (int i = 1; i < a.length; i++) {
        dp[i] = Math.max(a[i], a[i] + dp[i - 1]);
        best = Math.max(best, dp[i]);
    }
    return best;
}
```

### Go

```go
func maxSubArrayDP(a []int) int {
	dp := append([]int(nil), a...)
	best := dp[0]
	for i := 1; i < len(a); i++ {
		dp[i] = max(a[i], a[i]+dp[i-1])
		best = max(best, dp[i])
	}
	return best
}
```

## Approach 3 — Competitive Programming (Kadane's Algorithm)

Keep the best sum ending here and the global best. Time: `O(n)`. Space: `O(1)`.

### C++

```cpp
int maxSubArray(vector<int>& a) {
    int current = a[0], best = a[0];
    for (int i = 1; i < (int)a.size(); ++i) {
        current = max(a[i], current + a[i]);
        best = max(best, current);
    }
    return best;
}
```

### Python

```python
def max_subarray(nums: list[int]) -> int:
    current = best = nums[0]
    for value in nums[1:]:
        current, best = max(value, current + value), max(best, current)
    return best
```

### Java

```java
int maxSubArray(int[] a) {
    int current = a[0], best = a[0];
    for (int i = 1; i < a.length; i++) {
        current = Math.max(a[i], current + a[i]);
        best = Math.max(best, current);
    }
    return best;
}
```

### Go

```go
func maxSubArray(a []int) int {
	current, best := a[0], a[0]
	for _, value := range a[1:] {
		current = max(value, current+value)
		best = max(best, current)
	}
	return best
}
```

## Comparison

| Approach | Time | Space |
| --- | --- | --- |
| Brute force | `O(n^2)` | `O(1)` |
| DP array | `O(n)` | `O(n)` |
| Kadane | `O(n)` | `O(1)` |
