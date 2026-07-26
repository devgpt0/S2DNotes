# Problem 29: Burst Balloons (LeetCode #312)

**Difficulty:** Hard  
**Core pattern:** Interval dynamic programming

## Problem statement

Burst every balloon. Bursting `i` earns `left * nums[i] * right`, where `left`
and `right` are its current neighbors. Return the maximum total coins.

## Example

```text
nums = [3, 1, 5, 8]

One optimal order: burst 1, then 5, then 3, then 8
coins = 3*1*5 + 3*5*8 + 1*3*8 + 1*8*1
      = 15 + 120 + 24 + 8
      = 167
```

## Observation

Choosing the **first** balloon is hard because its future neighbors change.
Choose the **last** balloon in an interval instead. Its neighbors are then fixed
at the interval boundaries.

```text
1 | ... left part ... | k | ... right part ... | 1
                            ^
                     k is burst last

coins = dp[left][k] + value[left]*value[k]*value[right]
                      + dp[k][right]
```

## Solution 1: Try Every Burst Order

### Observation

There are `n!` possible orders, so direct backtracking is too slow.

### Algorithm

1. Try each remaining balloon as the next balloon to burst.
2. Add coins from its current left and right neighbors.
3. Remove it, recurse, then restore it.
4. Keep the best total among all orders.

### C++ code

```cpp
class Solution {
   private:
    int search(vector<int>& balloons) {
        if (balloons.empty()) {
            return 0;
        }

        int best = 0;
        for (int index = 0; index < static_cast<int>(balloons.size());
             ++index) {
            int left = index == 0 ? 1 : balloons[index - 1];
            int right = index + 1 == static_cast<int>(balloons.size())
                            ? 1
                            : balloons[index + 1];
            int value = balloons[index];

            balloons.erase(balloons.begin() + index);
            best = max(best, left * value * right + search(balloons));
            balloons.insert(balloons.begin() + index, value);
        }
        return best;
    }

   public:
    int maxCoins(vector<int>& nums) { return search(nums); }
};
```

### Complexity

- Time: `O(n! * n)` because every burst order is explored
- Space: `O(n)` recursion space

## How we derive the optimal solution

```text
Choose the next balloon to burst
           |
           v
Its neighbors depend on all earlier choices, so states are hard to reuse
           |
           v
Reverse the viewpoint: choose the last balloon in an interval
           |
           v
Its final neighbors are fixed interval boundaries
           |
           v
Combine left interval + final burst + right interval
Interval DP: O(n^3)
```

## Optimized / CP approach: Interval DP

### Algorithm

1. Add virtual balloons of value `1` at both ends.
2. Let `dp[left][right]` mean the best score strictly inside that interval.
3. Process intervals from short to long.
4. Try each `last` balloon between the boundaries.
5. Combine the two smaller intervals and the final burst coins.

### Complexity

- Time: `O(n^3)`
- Space: `O(n^2)`

## Pattern to remember

```text
An operation changes neighboring elements
        => choose the last operation in an interval
        => interval DP
```

## C++

```cpp
class Solution {
   public:
    int maxCoins(vector<int>& nums) {
        vector<int> values{1};
        values.insert(values.end(), nums.begin(), nums.end());
        values.push_back(1);

        int size = values.size();
        vector<vector<int>> dp(size, vector<int>(size, 0));

        for (int width = 2; width < size; ++width) {
            for (int left = 0; left + width < size; ++left) {
                int right = left + width;
                for (int last = left + 1; last < right; ++last) {
                    dp[left][right] =
                        max(dp[left][right],
                            dp[left][last] +
                                values[left] * values[last] * values[right] +
                                dp[last][right]);
                }
            }
        }
        return dp[0][size - 1];
    }
};
```

## Python

```python
class Solution:
    def max_coins(self, nums: list[int]) -> int:
        values = [1, *nums, 1]
        size = len(values)
        dp = [[0] * size for _ in range(size)]

        for width in range(2, size):
            for left in range(size - width):
                right = left + width
                for last in range(left + 1, right):
                    coins = (
                        dp[left][last]
                        + values[left] * values[last] * values[right]
                        + dp[last][right]
                    )
                    dp[left][right] = max(dp[left][right], coins)

        return dp[0][size - 1]
```

## Java

```java
class Solution {
    public int maxCoins(int[] nums) {
        int[] values = new int[nums.length + 2];
        values[0] = values[values.length - 1] = 1;
        System.arraycopy(nums, 0, values, 1, nums.length);

        int[][] dp = new int[values.length][values.length];
        for (int width = 2; width < values.length; width++) {
            for (int left = 0; left + width < values.length; left++) {
                int right = left + width;
                for (int last = left + 1; last < right; last++) {
                    int coins = dp[left][last] + values[left] * values[last] * values[right]
                        + dp[last][right];
                    dp[left][right] = Math.max(dp[left][right], coins);
                }
            }
        }
        return dp[0][values.length - 1];
    }
}
```

## Go

```go
func maxCoins(nums []int) int {
	values := make([]int, 0, len(nums)+2)
	values = append(values, 1)
	values = append(values, nums...)
	values = append(values, 1)

	size := len(values)
	dp := make([][]int, size)
	for index := range dp {
		dp[index] = make([]int, size)
	}

	for width := 2; width < size; width++ {
		for left := 0; left+width < size; left++ {
			right := left + width
			for last := left + 1; last < right; last++ {
				coins := dp[left][last]
				coins += values[left] * values[last] * values[right]
				coins += dp[last][right]
				dp[left][right] = max(dp[left][right], coins)
			}
		}
	}
	return dp[0][size-1]
}
```

## Common mistakes

- Defining the transition around the first balloon instead of the last.
- Forgetting the virtual boundary balloons.
- Filling large intervals before their smaller subintervals.
