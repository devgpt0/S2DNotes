# Problem 5: Subarray Sum Equals K (LeetCode #560)

**Difficulty:** Medium · **Pattern:** Prefix sum + hash map

## Problem Statement

Count contiguous subarrays whose elements sum to `k`.

## Example

`nums = [1, 1, 1]`, `k = 2` → `2`.

## Constraints

`1 <= nums.length <= 2 * 10^4`; values may be negative.

## Observation

If the current prefix is `sum`, every earlier prefix `sum - k` starts a valid subarray here.

## Learning diagram

```text
prefix[j] - prefix[i] = k -> find earlier prefix[i] = prefix[j] - k
```

## Algorithm for the optimal approach

Count earlier prefix sums equal to the current prefix minus `k`.

## Pattern to remember

> Target-sum subarrays with negatives -> prefix-frequency map.

## Solution 1: Brute Force

### Observation

Try every start and extend its sum. Time: `O(n^2)`. Space: `O(1)`.

### Algorithm

1. Choose every index as a subarray start.
2. Extend to every later end index.
3. Add the new value to a running sum.
4. Increment the answer whenever the sum equals `k`.

### C++ code

```cpp
class Solution {
   public:
    int subarraySum(vector<int>& nums, int k) {
        int answer = 0;

        for (int start = 0; start < static_cast<int>(nums.size()); ++start) {
            int sum = 0;
            for (int end = start; end < static_cast<int>(nums.size()); ++end) {
                sum += nums[end];
                if (sum == k) {
                    ++answer;
                }
            }
        }

        return answer;
    }
};
```

### Complexity

- Time: `O(n^2)`
- Space: `O(1)`

## How we derive the optimal solution

```text
Enumerate every subarray
          |
          v
Represent range sum as prefix[right] - prefix[left]
          |
          v
Need an earlier prefix equal to currentPrefix - k
          |
          v
Store frequencies of earlier prefix sums in a hash map
          |
          v
O(n) expected time, O(n) space
```

## Solution 2: Optimized (Prefix Array)

Build prefix sums, then compare every pair of prefix positions. Time: `O(n^2)`. Space: `O(n)`.

### C++

```cpp
int subarraySumPrefix(vector<int>& a, int k) {
    vector<int> prefix(a.size() + 1);
    for (int i = 0; i < (int)a.size(); ++i) prefix[i + 1] = prefix[i] + a[i];
    int count = 0;
    for (int l = 0; l < (int)a.size(); ++l)
        for (int r = l + 1; r <= (int)a.size(); ++r)
            count += prefix[r] - prefix[l] == k;
    return count;
}
```

### Python

```python
def subarray_sum_prefix(nums: list[int], k: int) -> int:
    prefix = [0]
    for value in nums:
        prefix.append(prefix[-1] + value)
    return sum(
        prefix[right] - prefix[left] == k
        for left in range(len(nums))
        for right in range(left + 1, len(nums) + 1)
    )
```

### Java

```java
int subarraySumPrefix(int[] a, int k) {
    int[] prefix = new int[a.length + 1];
    for (int i = 0; i < a.length; i++) prefix[i + 1] = prefix[i] + a[i];
    int count = 0;
    for (int left = 0; left < a.length; left++)
        for (int right = left + 1; right <= a.length; right++)
            if (prefix[right] - prefix[left] == k)
                count++;
    return count;
}
```

### Go

```go
func subarraySumPrefix(a []int, k int) int {
	prefix := make([]int, len(a)+1)
	for i, value := range a {
		prefix[i+1] = prefix[i] + value
	}
	count := 0
	for left := range a {
		for right := left + 1; right <= len(a); right++ {
			if prefix[right]-prefix[left] == k {
				count++
			}
		}
	}
	return count
}
```

## Approach 3 — Competitive Programming (Prefix Frequency Map)

Track counts of prior prefix sums. Initialize the empty prefix as one occurrence. Time: `O(n)` expected. Space: `O(n)`.

### C++

```cpp
int subarraySum(vector<int>& a, int k) {
    unordered_map<int, int> count{{0, 1}};
    int sum = 0, answer = 0;
    for (int value : a) {
        sum += value;
        answer += count[sum - k];
        ++count[sum];
    }
    return answer;
}
```

### Python

```python
def subarray_sum(nums: list[int], k: int) -> int:
    count, prefix, answer = {0: 1}, 0, 0
    for value in nums:
        prefix += value
        answer += count.get(prefix - k, 0)
        count[prefix] = count.get(prefix, 0) + 1
    return answer
```

### Java

```java
int subarraySum(int[] a, int k) {
    Map<Integer, Integer> count = new HashMap<>();
    count.put(0, 1);
    int sum = 0, answer = 0;
    for (int value : a) {
        sum += value;
        answer += count.getOrDefault(sum - k, 0);
        count.put(sum, count.getOrDefault(sum, 0) + 1);
    }
    return answer;
}
```

### Go

```go
func subarraySum(a []int, k int) int {
	count, sum, answer := map[int]int{0: 1}, 0, 0
	for _, value := range a {
		sum += value
		answer += count[sum-k]
		count[sum]++
	}
	return answer
}
```

## Comparison

| Approach | Time | Space |
| --- | --- | --- |
| Brute force | `O(n^2)` | `O(1)` |
| Prefix array | `O(n^2)` | `O(n)` |
| Prefix map | `O(n)` expected | `O(n)` |
