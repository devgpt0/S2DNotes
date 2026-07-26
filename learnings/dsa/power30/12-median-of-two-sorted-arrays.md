# Problem 12: Median of Two Sorted Arrays (LeetCode #4)

**Difficulty:** Hard · **Pattern:** Partition binary search

## Problem Statement

Return the median of two sorted arrays in `O(log(min(m, n)))` time.

## Example

`[1, 3]` and `[2]` → `2.0`.

## Observation

We do not need to merge the arrays. We only need a partition that places half
the values on the left and guarantees every left value is no larger than every
right value.

## Learning diagram

```text
Aleft | Aright    Bleft | Bright -> validate cross-boundaries
```

## Algorithm for the optimal approach

Binary-search a cut in the shorter array until both left partitions are no larger than both right partitions.

## Pattern to remember

> Two sorted arrays plus logarithmic requirement -> partition binary search.

## Solution 1: Brute Force

### Observation

Merge both arrays and take the middle. Time: `O(m+n)`. Space: `O(m+n)`.

### Algorithm

1. Merge both sorted arrays using two pointers.
2. Continue until all values are in sorted order.
3. Return the middle value for an odd total length.
4. Average the two middle values for an even total length.

### C++ code

```cpp
class Solution {
   public:
    double findMedianSortedArrays(vector<int>& first, vector<int>& second) {
        vector<int> merged;
        merged.reserve(first.size() + second.size());

        int left = 0;
        int right = 0;
        while (left < static_cast<int>(first.size()) &&
               right < static_cast<int>(second.size())) {
            if (first[left] <= second[right]) {
                merged.push_back(first[left++]);
            } else {
                merged.push_back(second[right++]);
            }
        }

        merged.insert(merged.end(), first.begin() + left, first.end());
        merged.insert(merged.end(), second.begin() + right, second.end());

        int middle = merged.size() / 2;
        if (merged.size() % 2 == 1) {
            return merged[middle];
        }
        return (merged[middle - 1] + merged[middle]) / 2.0;
    }
};
```

### Complexity

- Time: `O(m + n)`
- Space: `O(m + n)`

## How we derive the optimal solution

```text
Merge every value even though only the middle is needed
                    |
                    v
Merge only until the middle: less work, still O(m+n)
                    |
                    v
Think of the median as a partition with half the values on each side
                    |
                    v
Choose a cut in one array; the other cut is forced
                    |
                    v
Binary-search the cut in the shorter array
O(log(min(m,n))) time, O(1) space
```

## Optimized and Competitive Programming Approach — Partition the Shorter Array

Binary-search a partition where left-side values are no larger than right-side values. Time: `O(log(min(m,n)))`. Space: `O(1)`.

### C++

```cpp
double median(vector<int>& a, vector<int>& b) {
    if (a.size() > b.size()) return median(b, a);
    int m = a.size(), n = b.size();
    for (int l = 0, r = m; l <= r;) {
        int i = (l + r) / 2, j = (m + n + 1) / 2 - i;
        int al = i ? a[i - 1] : INT_MIN, ar = i < m ? a[i] : INT_MAX,
            bl = j ? b[j - 1] : INT_MIN, br = j < n ? b[j] : INT_MAX;
        if (al <= br && bl <= ar)
            return (m + n) & 1 ? max(al, bl)
                               : (max(al, bl) + min(ar, br)) / 2.0;
        if (al > br)
            r = i - 1;
        else
            l = i + 1;
    }
    return 0;
}
```

### Python

```python
def median(a: list[int], b: list[int]) -> float:
    if len(a) > len(b):
        return median(b, a)
    left, right, m, n = 0, len(a), len(a), len(b)
    while left <= right:
        i = (left + right) // 2
        j = (m + n + 1) // 2 - i
        al = a[i - 1] if i else float("-inf")
        ar = a[i] if i < m else float("inf")
        bl = b[j - 1] if j else float("-inf")
        br = b[j] if j < n else float("inf")
        if al <= br and bl <= ar:
            return max(al, bl) if (m + n) % 2 else (max(al, bl) + min(ar, br)) / 2
        if al > br:
            right = i - 1
        else:
            left = i + 1
    raise ValueError("inputs must be sorted")
```

### Java

```java
double median(int[] a, int[] b) {
    if (a.length > b.length)
        return median(b, a);
    int m = a.length, n = b.length;
    for (int l = 0, r = m; l <= r;) {
        int i = (l + r) / 2, j = (m + n + 1) / 2 - i;
        int al = i > 0 ? a[i - 1] : Integer.MIN_VALUE, ar = i < m ? a[i] : Integer.MAX_VALUE,
            bl = j > 0 ? b[j - 1] : Integer.MIN_VALUE, br = j < n ? b[j] : Integer.MAX_VALUE;
        if (al <= br && bl <= ar)
            return (m + n) % 2 == 1 ? Math.max(al, bl)
                                    : (Math.max(al, bl) + Math.min(ar, br)) / 2.0;
        if (al > br)
            r = i - 1;
        else
            l = i + 1;
    }
    throw new IllegalArgumentException("inputs must be sorted");
}
```

### Go

```go
func median(a, b []int) float64 {
	if len(a) > len(b) {
		return median(b, a)
	}
	m, n := len(a), len(b)
	for l, r := 0, m; l <= r; {
		i := (l + r) / 2
		j := (m+n+1)/2 - i
		al, ar := math.MinInt, math.MaxInt
		bl, br := math.MinInt, math.MaxInt
		if i > 0 {
			al = a[i-1]
		}
		if i < m {
			ar = a[i]
		}
		if j > 0 {
			bl = b[j-1]
		}
		if j < n {
			br = b[j]
		}
		if al <= br && bl <= ar {
			if (m+n)%2 == 1 {
				return float64(max(al, bl))
			}
			return float64(max(al, bl)+min(ar, br)) / 2
		}
		if al > br {
			r = i - 1
		} else {
			l = i + 1
		}
	}
	panic("inputs must be sorted")
}
```

## Key Invariant

The correct partition has `leftA <= rightB` and `leftB <= rightA`.
