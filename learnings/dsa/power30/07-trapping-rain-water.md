# Problem 7: Trapping Rain Water (LeetCode #42)

**Difficulty:** Hard · **Pattern:** Two pointers

## Problem

Given an array `height`, where `height[i]` is the height of a vertical bar,
return the total amount of rainwater trapped between the bars.

## Example

```text
height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
output = 6
```

## Visualization

```text
                █
        █~~~~~~~██
    █~~~██~█~~~~███
____████████████████
0   1 0 2 1 0 1 3 2 1 2 1

~ = trapped water
█ = bar
```

At index `5`, the bar height is `0`. The highest wall on its left is `2`, and
the highest wall on its right is `3`. Therefore this index stores
`min(2, 3) - 0 = 2` units of water.

## Constraints

`1 <= height.length <= 2 * 10^4`; `0 <= height[i] <= 10^5`.

## Main observation

Water above one index is limited by the shorter of its best left and right
walls:

```text
water[i] = min(leftMax[i], rightMax[i]) - height[i]
```

If this value is negative, that index stores `0` water.

## Pattern to remember

> When an answer at each index depends on information from both directions,
> first think about prefix/suffix arrays. Then ask whether two pointers can keep
> only the information needed at the current boundaries.

## Solution 1: Brute Force

### Observation

For every index, independently find:

- the tallest bar from the start through the current index;
- the tallest bar from the current index through the end.

The shorter maximum determines the water level at that index.

### Algorithm

1. Initialize `answer = 0`.
2. For every index `i`, scan from `0` to `i` to find `leftMax`.
3. Scan from `i` to `n - 1` to find `rightMax`.
4. Add `min(leftMax, rightMax) - height[i]` to the answer.
5. Return the answer.

### C++ code

```cpp
class Solution {
   public:
    int trap(vector<int>& height) {
        int answer = 0;

        for (int index = 0; index < static_cast<int>(height.size()); ++index) {
            int leftMax = 0;
            int rightMax = 0;

            for (int left = 0; left <= index; ++left) {
                leftMax = max(leftMax, height[left]);
            }

            for (int right = index; right < static_cast<int>(height.size());
                 ++right) {
                rightMax = max(rightMax, height[right]);
            }

            answer += min(leftMax, rightMax) - height[index];
        }

        return answer;
    }
};
```

### Complexity

- Time: `O(n^2)` because both sides are scanned for every index.
- Space: `O(1)`.

## How we derive the optimal solution

```text
Brute force
Find leftMax and rightMax again for every index
                    |
                    v
Remove repeated scans
Precompute leftMax[] and rightMax[]
                    |
                    v
O(n) time, but O(n) extra space
                    |
                    v
Observe that boundary processing needs only current maxima
Keep leftMax and rightMax as two running variables
                    |
                    v
Two pointers
O(n) time and O(1) extra space
```

The prefix/suffix solution removes repeated work. The two-pointer solution then
removes the arrays: whichever boundary is shorter can be finalized immediately,
because the opposite side already provides a wall at least that tall.

## Solution 2: Optimized with Prefix/Suffix Maxima

Precompute the maximum height on both sides of every bar. Time: `O(n)`. Space: `O(n)`.

### C++

```cpp
int trapArrays(vector<int>& h) {
    int n = h.size(), water = 0;
    vector<int> left(n), right(n);
    for (int i = 1; i < n; ++i) left[i] = max(left[i - 1], h[i - 1]);
    for (int i = n - 2; i >= 0; --i) right[i] = max(right[i + 1], h[i + 1]);
    for (int i = 0; i < n; ++i) water += max(0, min(left[i], right[i]) - h[i]);
    return water;
}
```

### Python

```python
def trap_arrays(height: list[int]) -> int:
    left, right = [0] * len(height), [0] * len(height)
    for i in range(1, len(height)):
        left[i] = max(left[i - 1], height[i - 1])
    for i in range(len(height) - 2, -1, -1):
        right[i] = max(right[i + 1], height[i + 1])
    return sum(max(0, min(left[i], right[i]) - value) for i, value in enumerate(height))
```

### Java

```java
int trapArrays(int[] h) {
    int n = h.length, water = 0;
    int[] left = new int[n], right = new int[n];
    for (int i = 1; i < n; i++) left[i] = Math.max(left[i - 1], h[i - 1]);
    for (int i = n - 2; i >= 0; i--) right[i] = Math.max(right[i + 1], h[i + 1]);
    for (int i = 0; i < n; i++) water += Math.max(0, Math.min(left[i], right[i]) - h[i]);
    return water;
}
```

### Go

```go
func trapArrays(h []int) int {
	left, right := make([]int, len(h)), make([]int, len(h))
	for i := 1; i < len(h); i++ {
		left[i] = max(left[i-1], h[i-1])
	}
	for i := len(h) - 2; i >= 0; i-- {
		right[i] = max(right[i+1], h[i+1])
	}
	water := 0
	for i, v := range h {
		water += max(0, min(left[i], right[i])-v)
	}
	return water
}
```

## Solution 3: Competitive Programming Approach (Two Pointers)

Advance the shorter side; its water level is already determined by its side maximum. Time: `O(n)`. Space: `O(1)`.

### C++

```cpp
int trap(vector<int>& h) {
    int l = 0, r = h.size() - 1, left = 0, right = 0, water = 0;
    while (l < r)
        if (h[l] < h[r]) {
            left = max(left, h[l]);
            water += left - h[l++];
        } else {
            right = max(right, h[r]);
            water += right - h[r--];
        }
    return water;
}
```

### Python

```python
def trap(height: list[int]) -> int:
    left, right, left_max, right_max, water = 0, len(height) - 1, 0, 0, 0
    while left < right:
        if height[left] < height[right]:
            left_max = max(left_max, height[left])
            water += left_max - height[left]
            left += 1
        else:
            right_max = max(right_max, height[right])
            water += right_max - height[right]
            right -= 1
    return water
```

### Java

```java
int trap(int[] h) {
    int l = 0, r = h.length - 1, left = 0, right = 0, water = 0;
    while (l < r) {
        if (h[l] < h[r]) {
            left = Math.max(left, h[l]);
            water += left - h[l++];
        } else {
            right = Math.max(right, h[r]);
            water += right - h[r--];
        }
    }
    return water;
}
```

### Go

```go
func trap(h []int) int {
	l, r, left, right, water := 0, len(h)-1, 0, 0, 0
	for l < r {
		if h[l] < h[r] {
			left = max(left, h[l])
			water += left - h[l]
			l++
		} else {
			right = max(right, h[r])
			water += right - h[r]
			r--
		}
	}
	return water
}
```

## Comparison

| Approach | Time | Space |
| --- | --- | --- |
| Brute force | `O(n^2)` | `O(1)` |
| Max arrays | `O(n)` | `O(n)` |
| Two pointers | `O(n)` | `O(1)` |
