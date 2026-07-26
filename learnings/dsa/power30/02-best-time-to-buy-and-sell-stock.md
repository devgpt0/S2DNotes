# Problem 2: Best Time to Buy and Sell Stock (LeetCode #121)

**Difficulty:** Easy · **Pattern:** Greedy

## Problem Statement

Given daily prices, choose one day to buy and a later day to sell. Return the largest possible profit, or `0` if no profit is possible.

## Example

`prices = [7, 1, 5, 3, 6, 4]` → `5` (buy at `1`, sell at `6`).

## Constraints

`1 <= prices.length <= 10^5`; `0 <= prices[i] <= 10^4`.

## Observation

The best sale today only needs the cheapest prior buy price.

## Learning diagram

```text
price -> update minimum buy -> compute today's profit -> update best
```

## Algorithm for the optimal approach

Track the lowest earlier price and treat every current price as a possible sale.

## Pattern to remember

> One buy before one sell -> remember the best past buy.

## Solution 1: Brute Force

### Observation

Try every buy/sell pair. Time: `O(n^2)`. Space: `O(1)`.

### Algorithm

1. Choose every day as a possible buy day.
2. Try every later day as a possible sell day.
3. Compute `sellPrice - buyPrice`.
4. Keep the largest non-negative profit.

### C++ code

```cpp
class Solution {
   public:
    int maxProfit(vector<int>& prices) {
        int bestProfit = 0;

        for (int buy = 0; buy < static_cast<int>(prices.size()); ++buy) {
            for (int sell = buy + 1; sell < static_cast<int>(prices.size());
                 ++sell) {
                bestProfit = max(bestProfit, prices[sell] - prices[buy]);
            }
        }

        return bestProfit;
    }
};
```

### Complexity

- Time: `O(n^2)`
- Space: `O(1)`

## How we derive the optimal solution

```text
Try every buy/sell pair
        |
        v
For a fixed sell day, only the cheapest earlier price matters
        |
        v
Precompute the minimum price up to every day
        |
        v
Observe that only the current minimum is needed
        |
        v
One-pass greedy: O(n) time, O(1) space
```

## Solution 2: Optimized (Prefix Minimum)

Store the minimum price through each day and calculate today's profit from it. Time: `O(n)`. Space: `O(n)`.

### C++

```cpp
int maxProfitPrefix(vector<int>& prices) {
    vector<int> minimum(prices.size());
    minimum[0] = prices[0];
    int best = 0;
    for (int i = 1; i < (int)prices.size(); ++i) {
        minimum[i] = min(minimum[i - 1], prices[i]);
        best = max(best, prices[i] - minimum[i]);
    }
    return best;
}
```

### Python

```python
def max_profit_prefix(prices: list[int]) -> int:
    minimum = [prices[0]] * len(prices)
    best = 0
    for index in range(1, len(prices)):
        minimum[index] = min(minimum[index - 1], prices[index])
        best = max(best, prices[index] - minimum[index])
    return best
```

### Java

```java
int maxProfitPrefix(int[] prices) {
    int[] minimum = new int[prices.length];
    minimum[0] = prices[0];
    int best = 0;
    for (int i = 1; i < prices.length; i++) {
        minimum[i] = Math.min(minimum[i - 1], prices[i]);
        best = Math.max(best, prices[i] - minimum[i]);
    }
    return best;
}
```

### Go

```go
func maxProfitPrefix(prices []int) int {
	minimum := make([]int, len(prices))
	minimum[0] = prices[0]
	best := 0
	for i := 1; i < len(prices); i++ {
		minimum[i] = min(minimum[i-1], prices[i])
		best = max(best, prices[i]-minimum[i])
	}
	return best
}
```

## Approach 3 — Competitive Programming (One-Pass Greedy)

Keep only the current minimum and best profit. Time: `O(n)`. Space: `O(1)`.

### C++

```cpp
int maxProfit(vector<int>& prices) {
    int low = INT_MAX, best = 0;
    for (int p : prices) {
        low = min(low, p);
        best = max(best, p - low);
    }
    return best;
}
```

### Python

```python
def max_profit(prices: list[int]) -> int:
    low, best = float("inf"), 0
    for price in prices:
        low, best = min(low, price), max(best, price - low)
    return best
```

### Java

```java
int maxProfit(int[] prices) {
    int low = Integer.MAX_VALUE, best = 0;
    for (int price : prices) {
        low = Math.min(low, price);
        best = Math.max(best, price - low);
    }
    return best;
}
```

### Go

```go
func maxProfit(prices []int) int {
	low, best := math.MaxInt, 0
	for _, p := range prices {
		low = min(low, p)
		best = max(best, p-low)
	}
	return best
}
```

## Comparison

| Approach | Time | Space |
| --- | --- | --- |
| Brute force | `O(n^2)` | `O(1)` |
| Prefix minimum | `O(n)` | `O(n)` |
| Greedy | `O(n)` | `O(1)` |
