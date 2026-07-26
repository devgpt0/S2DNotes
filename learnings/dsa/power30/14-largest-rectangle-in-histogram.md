# Problem 14: Largest Rectangle in Histogram (LeetCode #84)

**Difficulty:** Hard · **Pattern:** Monotonic stack

## Problem Statement

Return the largest rectangle area that can be formed by adjacent histogram bars.

## Example

`[2,1,5,6,2,3]` → `10`.

## Observation

A bar's maximum rectangle is known once we find the first shorter bar on both
sides. An increasing stack delays a bar until its right shorter boundary
appears.

## Learning diagram

```text
increasing stack -> lower bar arrives -> pop -> width boundaries become known
```

## Algorithm for the optimal approach

Keep increasing bar indices; a lower bar finalizes every taller popped rectangle.

## Pattern to remember

> Nearest smaller boundaries -> monotonic stack.

## Solution 1: Brute Force

### Observation

For each range, find its minimum height. Time: `O(n^2)`. Space: `O(1)`.

### Algorithm

1. Choose every bar as the left boundary.
2. Extend the right boundary one bar at a time.
3. Maintain the smallest height in that range.
4. Compute `minimumHeight * width` and update the best area.

### C++ code

```cpp
class Solution {
   public:
    int largestRectangleArea(vector<int>& heights) {
        int best = 0;

        for (int left = 0; left < static_cast<int>(heights.size()); ++left) {
            int minimumHeight = heights[left];

            for (int right = left; right < static_cast<int>(heights.size());
                 ++right) {
                minimumHeight = min(minimumHeight, heights[right]);
                int width = right - left + 1;
                best = max(best, minimumHeight * width);
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
Try every range and track its minimum height
                 |
                 v
For each bar, ask how far it can extend before a smaller bar
                 |
                 v
Need nearest smaller bar on both sides
                 |
                 v
Keep unresolved increasing heights on a stack
                 |
                 v
A lower bar finalizes the popped bars' right boundary
O(n) time
```

## Optimized and Competitive Programming Approach — Increasing Stack

When a lower height arrives, finalize each taller bar's largest possible rectangle. Time: `O(n)`. Space: `O(n)`.

### C++

```cpp
int largestRectangleArea(vector<int>& h) {
    vector<int> st;
    int best = 0;
    for (int i = 0; i <= (int)h.size(); ++i) {
        int x = i == (int)h.size() ? 0 : h[i];
        while (!st.empty() && h[st.back()] >= x) {
            int height = h[st.back()];
            st.pop_back();
            int left = st.empty() ? -1 : st.back();
            best = max(best, height * (i - left - 1));
        }
        st.push_back(i);
    }
    return best;
}
```

### Python

```python
def largest_rectangle_area(heights: list[int]) -> int:
    stack: list[int] = []
    best = 0
    for i, height in enumerate(heights + [0]):
        while stack and heights[stack[-1]] >= height:
            value = heights[stack.pop()]
            left = stack[-1] if stack else -1
            best = max(best, value * (i - left - 1))
        stack.append(i)
    return best
```

### Java

```java
int largestRectangleArea(int[] h) {
    Deque<Integer> st = new ArrayDeque<>();
    int best = 0;
    for (int i = 0; i <= h.length; i++) {
        int x = i == h.length ? 0 : h[i];
        while (!st.isEmpty() && h[st.peek()] >= x) {
            int height = h[st.pop()], left = st.isEmpty() ? -1 : st.peek();
            best = Math.max(best, height * (i - left - 1));
        }
        st.push(i);
    }
    return best;
}
```

### Go

```go
func largestRectangleArea(h []int) int {
	st := []int{}
	best := 0
	for i := 0; i <= len(h); i++ {
		x := 0
		if i < len(h) {
			x = h[i]
		}
		for len(st) > 0 && h[st[len(st)-1]] >= x {
			height := h[st[len(st)-1]]
			st = st[:len(st)-1]
			left := -1
			if len(st) > 0 {
				left = st[len(st)-1]
			}
			best = max(best, height*(i-left-1))
		}
		st = append(st, i)
	}
	return best
}
```

## Key Invariant

Stack heights are increasing; a pop determines both boundaries of that height.
