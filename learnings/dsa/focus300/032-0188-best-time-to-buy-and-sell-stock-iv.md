# Focus300 032: LeetCode 188 - Best Time to Buy and Sell Stock IV

**Source:** [LeetCode 188 - Best Time to Buy and Sell Stock IV](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/)  
**Difficulty:** Hard  
**Pattern:** transaction-state dynamic programming  

## Exact contract

Given daily nonnegative prices and integer `transaction_limit`, maximize profit
using at most that many buy-then-sell transactions. Only one share may be held,
and a sale must follow its buy.

## First principles

At each price, a valid strategy is either holding no share with some completed
sales, or holding one share bought after that many completed sales. Buying
subtracts the price; selling adds it and completes one transaction.

## Cases that decide correctness

- Zero transactions or fewer than two prices gives zero.
- Falling prices never force a loss.
- A share still held after the final day has no valid realized profit.
- When `k >= n // 2`, every rising adjacent pair can be harvested.
- Multiple same-day state transitions add no positive profit.

## Brute force: enumerate every legal daily action

```python
def maximum_stock_profit_brute(transaction_limit: int, prices: list[int]) -> int:
    if type(transaction_limit) is not int or transaction_limit < 0:
        raise ValueError("transaction_limit must be nonnegative")
    if any(type(price) is not int or price < 0 for price in prices):
        raise ValueError("prices must be nonnegative integers")
    negative_infinity = -(10**100)

    def search(day: int, sales_left: int, holding: bool) -> int:
        if day == len(prices):
            return negative_infinity if holding else 0
        best = search(day + 1, sales_left, holding)
        if holding and sales_left:
            best = max(
                best,
                prices[day] + search(day + 1, sales_left - 1, False),
            )
        elif not holding and sales_left:
            best = max(
                best,
                -prices[day] + search(day + 1, sales_left, True),
            )
        return best

    return search(0, transaction_limit, False)
```

**Complexity:** `O(2^n)` time and `O(n)` recursion space.

## Better approach: transaction endpoint DP

For each transaction count and sell day, try every earlier buy day. This gives
the correct recurrence in `O(k n^2)` time and `O(k n)` space, but repeats the
same best buy balance.

## Expert solution: retain the best cash and holding states

```python
def maximum_stock_profit(transaction_limit: int, prices: list[int]) -> int:
    if type(transaction_limit) is not int or transaction_limit < 0:
        raise ValueError("transaction_limit must be nonnegative")
    if any(type(price) is not int or price < 0 for price in prices):
        raise ValueError("prices must be nonnegative integers")
    if transaction_limit == 0 or len(prices) < 2:
        return 0
    if transaction_limit >= len(prices) // 2:
        return sum(
            max(0, prices[day] - prices[day - 1]) for day in range(1, len(prices))
        )

    cash = [0] * (transaction_limit + 1)
    holding = [-(10**100)] * (transaction_limit + 1)
    for price in prices:
        for transaction in range(1, transaction_limit + 1):
            holding[transaction] = max(
                holding[transaction], cash[transaction - 1] - price
            )
            cash[transaction] = max(cash[transaction], holding[transaction] + price)
    return cash[transaction_limit]
```

`holding[t]` is the best balance after buying the share whose sale may become
transaction `t`; `cash[t]` is the best realized profit after at most `t` sales.
Both choices are exhaustive and retain only the dominant balance.

**Complexity:** `O(k n)` time and `O(k)` space, or `O(n)` time in the unlimited
shortcut.

