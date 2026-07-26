# Problem 11: Search in Rotated Sorted Array (LeetCode #33)

**Difficulty:** Medium · **Pattern:** Binary search

## Problem Statement

Return the index of `target` in a rotated, strictly increasing array, or `-1` when absent.

## Example

`[4,5,6,7,0,1,2]`, `target = 0` → `4`.

## Observation

Rotation breaks the array at one pivot, but at least one side of every midpoint
is still normally sorted. That sorted side tells us whether the target can be
inside it.

## Learning diagram

```text
midpoint -> identify sorted half -> target inside it? -> keep correct half
```

## Algorithm for the optimal approach

At every midpoint, use the sorted half's range to discard half the array.

## Pattern to remember

> Rotated sorted data -> one midpoint half remains sorted.

## Solution 1: Brute Force

### Observation

Scan the array. Time: `O(n)`. Space: `O(1)`.

### Algorithm

1. Scan indices from left to right.
2. Return the index when its value equals `target`.
3. Return `-1` after the scan if the target was not found.

### C++ code

```cpp
class Solution {
   public:
    int search(vector<int>& nums, int target) {
        for (int index = 0; index < static_cast<int>(nums.size()); ++index) {
            if (nums[index] == target) {
                return index;
            }
        }
        return -1;
    }
};
```

### Complexity

- Time: `O(n)`
- Space: `O(1)`

## How we derive the optimal solution

```text
Linear scan ignores that the array is mostly sorted
                    |
                    v
Use a midpoint as in binary search
                    |
                    v
Rotation means the whole interval may not be sorted
                    |
                    v
At least one half around the midpoint is always sorted
                    |
                    v
Use that half's value range to discard half the search space
O(log n) time
```

## Optimized and Competitive Programming Approach — Binary Search

At every midpoint, one half is sorted. Keep the half that can contain the target. Time: `O(log n)`. Space: `O(1)`.

### C++

```cpp
int search(vector<int>& a, int t) {
    for (int l = 0, r = a.size() - 1; l <= r;) {
        int m = l + (r - l) / 2;
        if (a[m] == t) return m;
        if (a[l] <= a[m]) {
            if (a[l] <= t && t < a[m])
                r = m - 1;
            else
                l = m + 1;
        } else {
            if (a[m] < t && t <= a[r])
                l = m + 1;
            else
                r = m - 1;
        }
    }
    return -1;
}
```

### Python

```python
def search(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        elif nums[mid] < target <= nums[right]:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

### Java

```java
int search(int[] a, int t) {
    for (int l = 0, r = a.length - 1; l <= r;) {
        int m = l + (r - l) / 2;
        if (a[m] == t)
            return m;
        if (a[l] <= a[m]) {
            if (a[l] <= t && t < a[m])
                r = m - 1;
            else
                l = m + 1;
        } else if (a[m] < t && t <= a[r])
            l = m + 1;
        else
            r = m - 1;
    }
    return -1;
}
```

### Go

```go
func search(a []int, t int) int {
	for l, r := 0, len(a)-1; l <= r; {
		m := l + (r-l)/2
		if a[m] == t {
			return m
		}
		if a[l] <= a[m] {
			if a[l] <= t && t < a[m] {
				r = m - 1
			} else {
				l = m + 1
			}
		} else if a[m] < t && t <= a[r] {
			l = m + 1
		} else {
			r = m - 1
		}
	}
	return -1
}
```

## Key Invariant

If `target` exists, it remains inside the current inclusive search range.
