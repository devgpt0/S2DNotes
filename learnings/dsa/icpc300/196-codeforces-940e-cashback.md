# ICPC300 196: Codeforces 940E - Cashback

**Source:** [Codeforces 940E - Cashback](https://codeforces.com/problemset/problem/940/E)  
**Rating:** 2200  
**Pattern:** prefix DP with a monotone window minimum  
**Goal:** Buy all items in order. Items may be bought individually, or exactly
`group_size` consecutive items may be grouped so the cheapest item in that
group is free. Minimize total cost.

## 1. First principles

Let `dp[right]` be the minimum cost for the first `right` items. The last
decision is either one individual item or one discounted block:

```text
dp[right] = dp[right - 1] + price[right - 1]
dp[right] = min(dp[right],
                dp[right - group_size]
                + block_sum - block_minimum)
```

Prefix sums give `block_sum`. A monotone deque gives every fixed-size
`block_minimum` in amortized constant time.

## 2. Cases that decide correctness

- Discounted groups cannot overlap because each DP transition consumes a
  disjoint suffix.
- A group has exactly `group_size` consecutive items.
- With `group_size = 1`, every item can be free.
- Equal minimum prices are interchangeable.
- All prices are positive.

## 3. Brute force: enumerate individual and group decisions

```python
def minimum_cashback_cost_brute(prices: list[int], group_size: int) -> int:
    if not prices or any(price <= 0 for price in prices):
        raise ValueError("prices must be positive")
    if not 1 <= group_size <= len(prices):
        raise ValueError("group_size must fit the array")

    def solve(index: int) -> int:
        if index == len(prices):
            return 0
        answer = prices[index] + solve(index + 1)
        if index + group_size <= len(prices):
            group = prices[index : index + group_size]
            answer = min(answer, sum(group) - min(group) + solve(index + group_size))
        return answer

    return solve(0)
```

**Complexity:** `O(2^n * n)` time and `O(n)` recursion space.

## 4. Better transition: one-dimensional prefix DP

The recurrence has only `n+1` prefix states. Computing each block minimum by a
scan gives `O(n * group_size)` time; maintaining the minima of consecutive
windows removes that remaining repeated work.

## 5. Expert solution: DP with monotone deque minima

```python
from collections import deque


def minimum_cashback_cost(prices: list[int], group_size: int) -> int:
    if not prices or any(price <= 0 for price in prices):
        raise ValueError("prices must be positive")
    if not 1 <= group_size <= len(prices):
        raise ValueError("group_size must fit the array")

    prefix = [0] * (len(prices) + 1)
    for index, price in enumerate(prices, start=1):
        prefix[index] = prefix[index - 1] + price

    dp = [0] * (len(prices) + 1)
    minimum_indices: deque[int] = deque()
    for right in range(1, len(prices) + 1):
        index = right - 1
        while minimum_indices and prices[minimum_indices[-1]] >= prices[index]:
            minimum_indices.pop()
        minimum_indices.append(index)
        while minimum_indices[0] < right - group_size:
            minimum_indices.popleft()

        dp[right] = dp[right - 1] + prices[index]
        if right >= group_size:
            left = right - group_size
            group_cost = prefix[right] - prefix[left] - prices[minimum_indices[0]]
            dp[right] = min(dp[right], dp[left] + group_cost)
    return dp[-1]
```

### Why the expert code is correct

Every valid purchase plan ends with either one individually bought item or one
discounted group, so the recurrence covers all plans without overlap. The deque
front is exactly the minimum of the current length-`group_size` suffix, and
prefix differences give its exact sum. Induction over prefix length proves each
DP state optimal.

**Complexity:** `O(n)` time and `O(n)` space.

## 6. What to remember

```text
non-overlapping suffix choices -> prefix DP
fixed-size group discount -> window sum minus window minimum
all window minima -> monotone deque
```
