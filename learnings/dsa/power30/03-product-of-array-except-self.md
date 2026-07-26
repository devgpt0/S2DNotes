# Problem 3: Product of Array Except Self (LeetCode #238)

**Difficulty:** Medium · **Pattern:** Prefix / suffix products

## Problem Statement

Return `answer[i]` as the product of all values in `nums` except `nums[i]`. Do not use division.

## Example

`nums = [1, 2, 3, 4]` → `[24, 12, 8, 6]`.

## Constraints

`2 <= nums.length <= 10^5`; prefix and suffix products fit in a signed 32-bit integer.

## Observation

Every answer is `product(left of i) * product(right of i)`.

## Learning diagram

```text
answer[i] = product(left of i) * product(right of i)
```

## Algorithm for the optimal approach

Write prefixes into the result, then multiply them by one rolling suffix product.

## Pattern to remember

> Exclude current item -> combine left and right information.

## Solution 1: Brute Force

### Observation

For each index, multiply every other index. Time: `O(n^2)`. Space: `O(1)` besides output.

### Algorithm

1. Choose an output index `i`.
2. Scan the whole array.
3. Multiply every value whose index is not `i`.
4. Store the product in `answer[i]`.

### C++ code

```cpp
class Solution {
   public:
    vector<int> productExceptSelf(vector<int>& nums) {
        vector<int> answer(nums.size(), 1);

        for (int excluded = 0; excluded < static_cast<int>(nums.size());
             ++excluded) {
            for (int index = 0; index < static_cast<int>(nums.size());
                 ++index) {
                if (index != excluded) {
                    answer[excluded] *= nums[index];
                }
            }
        }

        return answer;
    }
};
```

### Complexity

- Time: `O(n^2)`
- Space: `O(1)` excluding the required output array

## How we derive the optimal solution

```text
Multiply all other values for every index
              |
              v
Repeated left and right products cause O(n^2)
              |
              v
Precompute prefix products and suffix products
              |
              v
O(n) time and O(n) extra space
              |
              v
Store prefixes in the output and keep one rolling suffix
              |
              v
O(n) time and O(1) extra space
```

## Solution 2: Optimized (Two Product Arrays)

Build prefix and suffix product arrays, then multiply corresponding entries. Time: `O(n)`. Space: `O(n)`.

### C++

```cpp
vector<int> productExceptSelfArrays(vector<int>& a) {
    int n = a.size();
    vector<int> left(n, 1), right(n, 1), ans(n);
    for (int i = 1; i < n; ++i) left[i] = left[i - 1] * a[i - 1];
    for (int i = n - 2; i >= 0; --i) right[i] = right[i + 1] * a[i + 1];
    for (int i = 0; i < n; ++i) ans[i] = left[i] * right[i];
    return ans;
}
```

### Python

```python
def product_arrays(nums: list[int]) -> list[int]:
    n = len(nums)
    left = [1] * n
    right = [1] * n
    for i in range(1, n):
        left[i] = left[i - 1] * nums[i - 1]
    for i in range(n - 2, -1, -1):
        right[i] = right[i + 1] * nums[i + 1]
    return [left[i] * right[i] for i in range(n)]
```

### Java

```java
int[] productArrays(int[] a) {
    int n = a.length;
    int[] left = new int[n], right = new int[n], answer = new int[n];
    Arrays.fill(left, 1);
    Arrays.fill(right, 1);
    for (int i = 1; i < n; i++) left[i] = left[i - 1] * a[i - 1];
    for (int i = n - 2; i >= 0; i--) right[i] = right[i + 1] * a[i + 1];
    for (int i = 0; i < n; i++) answer[i] = left[i] * right[i];
    return answer;
}
```

### Go

```go
func productArrays(a []int) []int {
	n := len(a)
	left, right, answer := make([]int, n), make([]int, n), make([]int, n)
	left[0], right[n-1] = 1, 1
	for i := 1; i < n; i++ {
		left[i] = left[i-1] * a[i-1]
	}
	for i := n - 2; i >= 0; i-- {
		right[i] = right[i+1] * a[i+1]
	}
	for i := range a {
		answer[i] = left[i] * right[i]
	}
	return answer
}
```

## Approach 3 — Competitive Programming (Output + Rolling Suffix)

Write prefix products into the result, then multiply by a running suffix. Time: `O(n)`. Extra space: `O(1)` excluding output.

### C++

```cpp
vector<int> productExceptSelf(vector<int>& a) {
    vector<int> ans(a.size(), 1);
    for (int i = 1; i < (int)a.size(); ++i) ans[i] = ans[i - 1] * a[i - 1];
    for (int i = (int)a.size() - 1, suffix = 1; i >= 0; --i) {
        ans[i] *= suffix;
        suffix *= a[i];
    }
    return ans;
}
```

### Python

```python
def product_except_self(nums: list[int]) -> list[int]:
    answer = [1] * len(nums)
    for i in range(1, len(nums)):
        answer[i] = answer[i - 1] * nums[i - 1]
    suffix = 1
    for i in range(len(nums) - 1, -1, -1):
        answer[i], suffix = answer[i] * suffix, suffix * nums[i]
    return answer
```

### Java

```java
int[] productExceptSelf(int[] a) {
    int[] answer = new int[a.length];
    Arrays.fill(answer, 1);
    for (int i = 1; i < a.length; i++) answer[i] = answer[i - 1] * a[i - 1];
    for (int i = a.length - 1, suffix = 1; i >= 0; i--) {
        answer[i] *= suffix;
        suffix *= a[i];
    }
    return answer;
}
```

### Go

```go
func productExceptSelf(a []int) []int {
	answer := make([]int, len(a))
	answer[0] = 1
	for i := 1; i < len(a); i++ {
		answer[i] = answer[i-1] * a[i-1]
	}
	suffix := 1
	for i := len(a) - 1; i >= 0; i-- {
		answer[i] *= suffix
		suffix *= a[i]
	}
	return answer
}
```

## Comparison

| Approach | Time | Extra space |
| --- | --- | --- |
| Brute force | `O(n^2)` | `O(1)` |
| Prefix + suffix arrays | `O(n)` | `O(n)` |
| Rolling suffix | `O(n)` | `O(1)` |
