# Focus300 046: LeetCode 312 - Burst Balloons

**Source:** [LeetCode 312](https://leetcode.com/problems/burst-balloons/)  
**Difficulty:** Hard  
**Pattern:** interval DP choosing the last action

## Exact contract

Given a nonempty list of balloon values from 0 through 100, burst every balloon.
Bursting the current balloon at index `i` earns
`left_value * value[i] * right_value`, where left and right are its surviving
neighbors; a missing outside neighbor has value one. Return the maximum total.

## First principles

Choosing the first balloon makes future neighbors depend on earlier choices.
Choosing the last balloon inside an interval removes that dependency: its
surviving neighbors are exactly the interval boundaries. The left and right
subintervals are then independent.

## Cases that decide correctness

- Outside virtual balloons have value one and are never burst.
- Zero-valued balloons may still change which positive balloons become adjacent.
- A one-balloon interval has one possible last choice.
- Every original balloon is burst exactly once.
- Interval boundaries are excluded from the subproblem.

## Brute force: simulate every bursting order

```python
from itertools import permutations


def maximum_coins_brute(numbers: list[int]) -> int:
    if not numbers or any(not 0 <= number <= 100 for number in numbers):
        raise ValueError("balloon values must be between 0 and 100")

    answer = 0
    for order in permutations(range(len(numbers))):
        balloons = list(enumerate(numbers))
        coins = 0
        for original_index in order:
            position = next(
                index
                for index, (index_value, _number) in enumerate(balloons)
                if index_value == original_index
            )
            left = balloons[position - 1][1] if position else 1
            right = balloons[position + 1][1] if position + 1 < len(balloons) else 1
            coins += left * balloons[position][1] * right
            balloons.pop(position)
        answer = max(answer, coins)
    return answer
```

This takes `O(n! * n^2)` time with list searches and removals.

## Better approach: memoize the last balloon in each interval

```python
from functools import cache


def maximum_coins_memoized(numbers: list[int]) -> int:
    if not numbers or any(not 0 <= number <= 100 for number in numbers):
        raise ValueError("balloon values must be between 0 and 100")

    values = [1, *numbers, 1]

    @cache
    def solve(left: int, right: int) -> int:
        return max(
            (
                solve(left, last)
                + values[left] * values[last] * values[right]
                + solve(last, right)
                for last in range(left + 1, right)
            ),
            default=0,
        )

    return solve(0, len(values) - 1)
```

Memoization evaluates each boundary pair once in `O(n^3)` time.

## Expert solution: bottom-up interval DP

```python
def maximum_coins(numbers: list[int]) -> int:
    if not numbers or any(not 0 <= number <= 100 for number in numbers):
        raise ValueError("balloon values must be between 0 and 100")

    values = [1, *numbers, 1]
    table = [[0] * len(values) for _ in values]
    for width in range(2, len(values)):
        for left in range(len(values) - width):
            right = left + width
            table[left][right] = max(
                table[left][last]
                + values[left] * values[last] * values[right]
                + table[last][right]
                for last in range(left + 1, right)
            )
    return table[0][-1]
```

For each possible last balloon, both smaller intervals have already been
solved. Its boundary product is the exact final reward in that interval, so
maximizing over last choices proves the recurrence by induction on width.

**Complexity:** `O(n^3)` time and `O(n^2)` space.
