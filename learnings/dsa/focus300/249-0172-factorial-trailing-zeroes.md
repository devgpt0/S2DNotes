# Focus300 249: LeetCode 172 - Factorial Trailing Zeroes

**Source:** [LeetCode 172](https://leetcode.com/problems/factorial-trailing-zeroes/)  
**Difficulty:** Easy  
**Pattern:** counting factors of five

## Exact contract

Return how many trailing zeroes appear in `n!`.

## First principles

A trailing zero comes from a factor pair of `2` and `5`, and factorials contain far more twos than fives. Counting factors of five therefore determines the answer.

## Cases that decide correctness

- Each multiple of `5` contributes one factor of five.
- Each multiple of `25` contributes an extra factor of five.
- The same logic continues for `125`, `625`, and so on.
- Small values of `n` may yield zero trailing zeroes.

## Brute force

```python
def trailing_zeroes_brute(n):
    count = 0
    while n:
        n //= 5
        count += n
    return count
```

Compute `n!` directly and count the ending zeroes.

## Better insight

Count the multiples of powers of five instead of expanding the factorial.

## Expert solution

```python
def trailing_zeroes(n):
    count = 0
    while n:
        n //= 5
        count += n
    return count
```

Repeatedly divide `n` by five and accumulate the quotients to count all five factors.

**Complexity:** O(log_5 n) time and O(1) space.
