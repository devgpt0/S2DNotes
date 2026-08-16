# Focus300 299: LeetCode 309 - Best Time to Buy and Sell Stock with Cooldown

**Source:** [LeetCode 309](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/)  
**Difficulty:** Medium  
**Pattern:** problem-specific recursion or scanning

## Exact contract

Solve the LeetCode problem 'Best Time to Buy and Sell Stock with Cooldown' according to the statement and constraints.

## First principles

Most interview-style problems reduce to the right state definition. Once that state is explicit, the rest is choosing the simplest way to preserve it.


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

- Check the empty and single-item boundary first.
- Look for duplicate handling and off-by-one errors.
- Confirm whether the answer is a boolean, count, value, or structure.
- Make sure the invariant survives every update step.

## Brute force

```python
from functools import lru_cache

def max_profit_brute(prices):
    @lru_cache(None)
    def solve(i, holding):
        if i >= len(prices):
            return 0
        if holding:
            return max(prices[i] + solve(i + 2, 0), solve(i + 1, 1))
        return max(-prices[i] + solve(i + 1, 1), solve(i + 1, 0))

    return solve(0, 0)
```

Try the most direct exhaustive solution.

## Better insight

Identify the state that can be reused and avoid recomputing it.

## Expert solution

```python
def max_profit(prices):
    if not prices:
        return 0
    hold = -prices[0]
    sold = 0
    rest = 0
    for price in prices[1:]:
        prev_hold = hold
        hold = max(hold, rest - price)
        rest = max(rest, sold)
        sold = prev_hold + price
    return max(sold, rest)
```

Use the smallest invariant that proves correctness and update it once per step.

**Complexity:** Usually linear or near-linear in the input size, with the exact bound determined by the pattern.
