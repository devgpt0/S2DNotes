# Problem 1: Two Sum (LeetCode #1)

**Difficulty:** Easy · **Pattern:** Hash map / two pointers

## Problem Statement

Given `nums` and `target`, return indices of two different elements whose sum is `target`. One valid answer exists.

## Example

`nums = [2, 7, 11, 15]`, `target = 9` → `[0, 1]`.

## Constraints

`2 <= nums.length <= 10^4`; values and `target` fit in a signed 32-bit integer.

## Observation

For a value `x`, the required partner is `target - x`.

## Learning diagram

```text
current x -> need target-x -> map lookup -> answer or store x
```

## Algorithm for the optimal approach

Scan left to right; look up the complement before storing the current value.

## Pattern to remember

> Pair target and indices -> complement lookup in a hash map.

## Solution 1: Brute Force

### Observation

Check every pair. Time: `O(n^2)`. Space: `O(1)`.

### Algorithm

1. Choose the first index `i`.
2. Try every later index `j`.
3. Return `[i, j]` when `nums[i] + nums[j] == target`.

### C++ code

```cpp
class Solution {
   public:
    vector<int> twoSum(vector<int>& nums, int target) {
        for (int first = 0; first < static_cast<int>(nums.size()); ++first) {
            for (int second = first + 1; second < static_cast<int>(nums.size());
                 ++second) {
                if (nums[first] + nums[second] == target) {
                    return {first, second};
                }
            }
        }
        return {};
    }
};
```

### Complexity

- Time: `O(n^2)`
- Space: `O(1)`

## How we derive the optimal solution

```text
Try every pair
      |
      v
For current value x, the partner must be target - x
      |
      v
Repeatedly searching for that partner is the expensive work
      |
      v
Remember previously seen values in a hash map
      |
      v
One pass: O(n) expected time, O(n) space
```

## Solution 2: Optimized (Hash Map)

Scan left to right. Check whether the complement was seen before inserting the current value. Time: `O(n)` expected. Space: `O(n)`.

### C++

```cpp
vector<int> twoSum(vector<int>& a, int target) {
    unordered_map<int, int> seen;
    for (int i = 0; i < (int)a.size(); ++i) {
        auto it = seen.find(target - a[i]);
        if (it != seen.end()) return {it->second, i};
        seen[a[i]] = i;
    }
    return {};
}
```

### Python

```python
def two_sum(nums: list[int], target: int) -> list[int]:
    seen: dict[int, int] = {}
    for index, value in enumerate(nums):
        if target - value in seen:
            return [seen[target - value], index]
        seen[value] = index
    return []
```

### Java

```java
int[] twoSum(int[] nums, int target) {
    Map<Integer, Integer> seen = new HashMap<>();
    for (int i = 0; i < nums.length; i++) {
        Integer match = seen.get(target - nums[i]);
        if (match != null)
            return new int[] {match, i};
        seen.put(nums[i], i);
    }
    return new int[0];
}
```

### Go

```go
func twoSum(nums []int, target int) []int {
	seen := map[int]int{}
	for i, value := range nums {
		if match, ok := seen[target-value]; ok {
			return []int{match, i}
		}
		seen[value] = i
	}
	return nil
}
```

## Approach 3 — Competitive Programming (Sort + Two Pointers)

Pair values with original indices, sort, and move the left or right pointer according to the sum. Time: `O(n log n)`. Space: `O(n)`.

### C++

```cpp
vector<int> twoSumCp(vector<int> a, int target) {
    vector<pair<int, int>> b;
    for (int i = 0; i < (int)a.size(); ++i) b.push_back({a[i], i});
    sort(b.begin(), b.end());
    for (int l = 0, r = (int)b.size() - 1; l < r;) {
        int sum = b[l].first + b[r].first;
        if (sum == target) return {b[l].second, b[r].second};
        sum < target ? ++l : --r;
    }
    return {};
}
```

### Python

```python
def two_sum_cp(nums: list[int], target: int) -> list[int]:
    values = sorted((value, index) for index, value in enumerate(nums))
    left, right = 0, len(values) - 1
    while left < right:
        total = values[left][0] + values[right][0]
        if total == target:
            return [values[left][1], values[right][1]]
        if total < target:
            left += 1
        else:
            right -= 1
    return []
```

### Java

```java
int[] twoSumCp(int[] nums, int target) {
    int[][] values = new int[nums.length][2];
    for (int i = 0; i < nums.length; i++) values[i] = new int[] {nums[i], i};
    Arrays.sort(values, Comparator.comparingInt(pair -> pair[0]));
    for (int left = 0, right = values.length - 1; left < right;) {
        int sum = values[left][0] + values[right][0];
        if (sum == target)
            return new int[] {values[left][1], values[right][1]};
        if (sum < target)
            left++;
        else
            right--;
    }
    return new int[0];
}
```

### Go

```go
func twoSumCP(nums []int, target int) []int {
	type pair struct{ value, index int }
	values := make([]pair, len(nums))
	for i, value := range nums {
		values[i] = pair{value, i}
	}
	sort.Slice(values, func(i, j int) bool { return values[i].value < values[j].value })
	for left, right := 0, len(values)-1; left < right; {
		sum := values[left].value + values[right].value
		if sum == target {
			return []int{values[left].index, values[right].index}
		}
		if sum < target {
			left++
		} else {
			right--
		}
	}
	return nil
}
```

## Comparison

| Approach | Time | Space | Best use |
| --- | --- | --- | --- |
| Brute force | `O(n^2)` | `O(1)` | Learn the pair search |
| Hash map | `O(n)` expected | `O(n)` | Standard interview answer |
| Sort + two pointers | `O(n log n)` | `O(n)` | Sorting-based CP variants |
