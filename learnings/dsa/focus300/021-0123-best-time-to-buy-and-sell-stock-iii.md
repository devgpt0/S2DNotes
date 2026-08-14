# Focus300 021: LeetCode 123 - Best Time to Buy and Sell Stock III

**Source:** [LeetCode 123](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iii/)  
**Difficulty:** Hard  
**Pattern:** finite-state transaction DP

## Exact contract

Given daily stock prices, return the maximum profit from at most two completed
buy-sell transactions. Only one share may be held at a time, so transactions
cannot overlap.

## First principles

After each price, only four best balances matter: after the first buy, first
sale, second buy, and second sale. Each state either keeps yesterday's value or
performs its defining action today from the preceding state.

Allowing fewer than two transactions is represented by sale states initialized
to zero. Same-day sell then buy transitions do not create profit and are safe.

## Cases that decide correctness

- Empty and one-day price lists return zero.
- Prices may repeat.
- Falling prices should perform no transaction.
- The second buy must use profit available after the first sale.
- "At most two" includes zero or one transaction.

## Brute force: enumerate ordered transaction endpoints

```python
def max_profit_two_transactions_brute(prices: list[int]) -> int:
    answer = 0
    for first_buy in range(len(prices)):
        for first_sell in range(first_buy, len(prices)):
            first_profit = prices[first_sell] - prices[first_buy]
            answer = max(answer, first_profit)
            for second_buy in range(first_sell, len(prices)):
                for second_sell in range(second_buy, len(prices)):
                    answer = max(
                        answer,
                        first_profit + prices[second_sell] - prices[second_buy],
                    )
    return answer
```

This takes `O(n^4)` time.

## Better approach: combine prefix and suffix single-transaction profits

```python
def max_profit_two_transactions_arrays(prices: list[int]) -> int:
    if not prices:
        return 0
    prefix = [0] * len(prices)
    minimum = prices[0]
    for index, price in enumerate(prices[1:], start=1):
        minimum = min(minimum, price)
        prefix[index] = max(prefix[index - 1], price - minimum)

    suffix = [0] * len(prices)
    maximum = prices[-1]
    for index in range(len(prices) - 2, -1, -1):
        maximum = max(maximum, prices[index])
        suffix[index] = max(suffix[index + 1], maximum - prices[index])
    return max(prefix[index] + suffix[index] for index in range(len(prices)))
```

This is `O(n)` time and `O(n)` space.

## Expert solution: four transaction states

```python
def max_profit_two_transactions(prices: list[int]) -> int:
    first_buy = float("-inf")
    first_sale = 0
    second_buy = float("-inf")
    second_sale = 0
    for price in prices:
        first_buy = max(first_buy, -price)
        first_sale = max(first_sale, first_buy + price)
        second_buy = max(second_buy, first_sale - price)
        second_sale = max(second_sale, second_buy + price)
    return int(second_sale)
```

The four values are the complete DP frontier; earlier prices affect the future
only through those best balances.

**Complexity:** `O(n)` time and `O(1)` space.
