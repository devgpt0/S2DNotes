# Focus300 224: LeetCode 122 - Best Time to Buy and Sell Stock II

**Source:** [LeetCode 122](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/)  
**Difficulty:** Medium  
**Pattern:** greedy accumulation of positive price moves

## Exact contract

Compute the maximum profit with unlimited transactions, where each share must be sold before it can be bought again.

## First principles

Every profitable transaction can be decomposed into the positive day-to-day rises that it spans. If tomorrow is more expensive than today, capturing that rise never hurts.


## Classroom board: see the repeated work once

```text
brute force tries every choice.
the optimized solution keeps only the state that must survive to the
next step.
```



## Step-by-step transformation

1. Read the input and identify the smallest state that still determines the answer.
2. Process one element, node, or row at a time while preserving that state.
3. Discard work that can no longer change the result.
4. Convert the surviving state into the output the problem requests.

The examples and code below show this transformation on the specific problem instance.


## Diagram: input to output

```text

        input
            |
            v
        core invariant
            |
            v
        process one step at a time
            |
            v
        output
```

The note shows the main idea, the repeated work, and the small state that turns the input into the output.

## Cases that decide correctness

- A non-increasing price series yields zero profit.
- Multiple small gains can equal one larger multi-day gain.
- You cannot hold more than one share at a time.
- The answer is the sum of all positive adjacent differences.

## Brute force

```python
def max_profit_brute(prices):
    if not prices:
        return 0
    return sum(max(0, b - a) for a, b in zip(prices, prices[1:]))
```

Try every buy/sell pair or every transaction schedule.

## Better insight

Accumulate each positive difference and ignore the days that do not improve value.

## Expert solution

```python
def max_profit(prices):
    profit = 0
    for a, b in zip(prices, prices[1:]):
        if b > a:
            profit += b - a
    return profit
```

Scan once, add the rise whenever the next price exceeds the current price, and treat each rise as an independent profitable step.

**Complexity:** O(n) time and O(1) space.
