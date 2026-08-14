# Focus300 038: LeetCode 233 - Number of Digit One

**Source:** [LeetCode 233 - Number of Digit One](https://leetcode.com/problems/number-of-digit-one/)  
**Difficulty:** Hard  
**Pattern:** decimal positional contribution counting  

## Exact contract

For nonnegative integer `upper_bound`, count how many digit `1` occurrences
appear in the decimal representations of every integer from `0` through
`upper_bound`, inclusive.

## First principles

At decimal factor `f`, split the number into digits higher than the position,
the current digit, and lower digits. Every complete block of `10*f` contributes
`f` ones at that position. The partial block contributes zero, `lower + 1`, or
`f` depending on whether the current digit is below, equal to, or above one.

## Cases that decide correctness

- Zero contributes no digit one.
- The interval is inclusive, hence the `lower + 1` term.
- Digit one in separate positions is counted separately.
- Powers of ten expose boundary off-by-one errors.
- The loop stops after the highest occupied decimal position.

## Brute force: convert every number to decimal text

```python
def count_digit_one_brute(upper_bound: int) -> int:
    if type(upper_bound) is not int or upper_bound < 0:
        raise ValueError("upper_bound must be a nonnegative integer")
    return sum(str(value).count("1") for value in range(upper_bound + 1))
```

**Complexity:** `O(n log n)` time and `O(log n)` temporary space.

## Better approach: decimal digit DP

A digit DP can track position, tightness, and accumulated occurrences in
`O(log n)` states. Positional counting removes the state machinery entirely.

## Expert solution: sum each position's complete and partial blocks

```python
def count_digit_one(upper_bound: int) -> int:
    if type(upper_bound) is not int or upper_bound < 0:
        raise ValueError("upper_bound must be a nonnegative integer")
    answer = 0
    factor = 1
    while factor <= upper_bound:
        lower = upper_bound % factor
        current = upper_bound // factor % 10
        higher = upper_bound // (factor * 10)
        answer += higher * factor
        if current == 1:
            answer += lower + 1
        elif current > 1:
            answer += factor
        factor *= 10
    return answer
```

Complete high-digit blocks provide `higher * factor` occurrences. The current
digit case accounts for exactly the remaining partial block, so summing all
positions counts every occurrence once.

**Complexity:** `O(log n)` time and `O(1)` space.

