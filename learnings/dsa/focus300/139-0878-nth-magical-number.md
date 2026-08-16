# Focus300 139: LeetCode 878 - Nth Magical Number

**Source:** [LeetCode 878](https://leetcode.com/problems/nth-magical-number/)  
**Difficulty:** Hard  
**Pattern:** binary search on an inclusion-exclusion count

## Exact contract

A positive integer is magical when divisible by positive `a` or positive `b`.
Return the `n`th magical number modulo `1_000_000_007`, where `n` is at most
`1_000_000_000` and `a, b` are at most 40,000.

## First principles

Up to value `x`, there are `floor(x/a) + floor(x/b) - floor(x/lcm(a,b))`
magical numbers. This count is monotone, so the first `x` whose count reaches
`n` is exactly the `n`th magical number.


## Classroom board: discard half the search space

```text
binary search keeps the side that can still contain the answer and throws
away the side that cannot.
```



## Step-by-step transformation

1. Compare the middle position with the target rule or boundary condition.
2. Discard the half that cannot still contain a valid answer.
3. Repeat until the remaining interval is exactly the split or value the problem asks for.
4. Convert the final boundary positions into the required output.

Binary-search style notes transform the input by shrinking the search space until only one valid boundary or value remains.


## Diagram: discard half the search space

```text

            sorted input
                |
                v
            check middle
                |
                v
            keep the half that can still work
                |
                v
            final boundary / value
```

Binary search keeps shrinking the input until only the valid boundary or value is left.

## Cases that decide correctness

- Multiples of both divisors are counted once by inclusion-exclusion.
- Equal divisors reduce to ordinary multiples.
- Binary search returns the first qualifying value.
- Search the unmodded answer; apply the modulus only after locating it.
- `n * min(a, b)` is always a sufficient upper bound.

## Brute force: inspect positive integers in order

```python
MODULO = 1_000_000_007


def nth_magical_number_brute(index: int, first: int, second: int) -> int:
    if any(type(value) is not int for value in (index, first, second)):
        raise TypeError("index and divisors must be integers")
    if (
        not 1 <= index <= 1_000_000_000
        or not 1 <= first <= 40_000
        or not 1 <= second <= 40_000
    ):
        raise ValueError("index or divisor is outside the source bounds")

    found = 0
    value = 0
    while found < index:
        value += 1
        if value % first == 0 or value % second == 0:
            found += 1
    return value % MODULO
```

This takes `O(n * min(a, b))` divisibility checks in the worst case.

## Better approach: merge the two multiple streams

Advance the smaller of the next multiples of `a` and `b`, advancing both on a
tie. That is `O(n)` time and constant space; counting by value enables binary
search instead.

## Expert solution: lower-bound the monotone count

```python
from math import gcd


MODULO = 1_000_000_007


def nth_magical_number(index: int, first: int, second: int) -> int:
    if any(type(value) is not int for value in (index, first, second)):
        raise TypeError("index and divisors must be integers")
    if (
        not 1 <= index <= 1_000_000_000
        or not 1 <= first <= 40_000
        or not 1 <= second <= 40_000
    ):
        raise ValueError("index or divisor is outside the source bounds")

    common_multiple = first // gcd(first, second) * second
    low = min(first, second)
    high = index * low
    while low < high:
        middle = (low + high) // 2
        count = middle // first + middle // second - middle // common_multiple
        if count >= index:
            high = middle
        else:
            low = middle + 1
    return low % MODULO
```

The count predicate is false before the answer and true from the answer onward.
Standard lower-bound search therefore isolates the exact magical value.

**Complexity:** `O(log(n * min(a, b)))` time and `O(1)` space.
