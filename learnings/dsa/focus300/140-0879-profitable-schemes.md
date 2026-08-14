# Focus300 140: LeetCode 879 - Profitable Schemes

**Source:** [LeetCode 879](https://leetcode.com/problems/profitable-schemes/)  
**Difficulty:** Hard  
**Pattern:** capacity DP with capped profit

## Exact contract

Choose a subset of crimes. Crime `i` uses `group[i]` members and earns
`profit[i]`. Count subsets using at most `n` members and earning at least
`min_profit`, modulo `1_000_000_007`. The source bounds all counts, `n`, and
`min_profit` by 100.

## First principles

Exact profit above the threshold is irrelevant, so cap every accumulated
profit at `min_profit`. A DP state `(members_used, capped_profit)` counts
subsets. Processing member counts backward ensures each crime is selected at
most once.

## Cases that decide correctness

- The empty subset counts when `min_profit` is zero.
- Member usage is at most `n`, not exactly `n`.
- Distinct crimes remain distinct even with equal group and profit values.
- All profits at or above the threshold share one capped state.
- Descending member iteration prevents reusing the current crime.

## Brute force: enumerate every crime subset

```python
MODULO = 1_000_000_007


def profitable_schemes_brute(
    member_limit: int,
    minimum_profit: int,
    group: list[int],
    profit: list[int],
) -> int:
    if type(member_limit) is not int or type(minimum_profit) is not int:
        raise TypeError("member_limit and minimum_profit must be integers")
    if not 1 <= member_limit <= 100 or not 0 <= minimum_profit <= 100:
        raise ValueError("member or profit limit is outside source bounds")
    if (
        type(group) is not list
        or type(profit) is not list
        or any(type(value) is not int for value in group + profit)
    ):
        raise TypeError("group and profit must be lists of integers")
    if not 1 <= len(group) == len(profit) <= 100:
        raise ValueError("crime arrays must have equal length between 1 and 100")
    if any(members <= 0 for members in group) or any(value < 0 for value in profit):
        raise ValueError("member costs must be positive and profits non-negative")

    answer = 0
    for mask in range(1 << len(group)):
        members = sum(
            group[index] for index in range(len(group)) if mask & (1 << index)
        )
        earned = sum(
            profit[index] for index in range(len(group)) if mask & (1 << index)
        )
        if members <= member_limit and earned >= minimum_profit:
            answer += 1
    return answer % MODULO
```

This takes `O(2^m * m)` time for `m` crimes and `O(1)` auxiliary space.

## Better approach: retain exact profit in a three-dimensional DP

A crime-index DP over exact member and profit totals is correct but wastes
states above the required profit. Capping profit removes that unbounded
dimension, and rolling the crime dimension permits in-place updates.

## Expert solution: update capped states backward

```python
MODULO = 1_000_000_007


def profitable_schemes(
    member_limit: int,
    minimum_profit: int,
    group: list[int],
    profit: list[int],
) -> int:
    if type(member_limit) is not int or type(minimum_profit) is not int:
        raise TypeError("member_limit and minimum_profit must be integers")
    if not 1 <= member_limit <= 100 or not 0 <= minimum_profit <= 100:
        raise ValueError("member or profit limit is outside source bounds")
    if (
        type(group) is not list
        or type(profit) is not list
        or any(type(value) is not int for value in group + profit)
    ):
        raise TypeError("group and profit must be lists of integers")
    if not 1 <= len(group) == len(profit) <= 100:
        raise ValueError("crime arrays must have equal length between 1 and 100")
    if any(members <= 0 for members in group) or any(value < 0 for value in profit):
        raise ValueError("member costs must be positive and profits non-negative")

    ways = [[0] * (minimum_profit + 1) for _ in range(member_limit + 1)]
    ways[0][0] = 1
    for required_members, earned_profit in zip(group, profit, strict=True):
        for used_members in range(member_limit, required_members - 1, -1):
            for capped_profit in range(minimum_profit, -1, -1):
                next_profit = min(minimum_profit, capped_profit + earned_profit)
                ways[used_members][next_profit] = (
                    ways[used_members][next_profit]
                    + ways[used_members - required_members][capped_profit]
                ) % MODULO
    return sum(ways[used][minimum_profit] for used in range(member_limit + 1)) % MODULO
```

Each transition either excludes the crime implicitly or includes it from a
lower-member state. The capped profit coordinate preserves exactly the only
threshold distinction the result needs.

**Complexity:** `O(crimes * n * min_profit)` time and
`O(n * min_profit)` space.
