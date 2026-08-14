# Focus300 146: LeetCode 902 - Numbers At Most N Given Digit Set

**Source:** [LeetCode 902](https://leetcode.com/problems/numbers-at-most-n-given-digit-set/)  
**Difficulty:** Hard  
**Pattern:** positional counting with a tight prefix

## Exact contract

Given distinct digit strings from `"1"` through `"9"`, count positive integers
at most `limit` whose every decimal digit belongs to that set. A digit may be
used any number of times.

## First principles

All allowed numbers shorter than `limit` contribute `k^length`. At a position
of equal-length numbers, every allowed digit smaller than the limit digit frees
the remaining positions, contributing `k^remaining`. An equal digit keeps the
prefix tight; if equality is impossible, counting stops.

## Cases that decide correctness

- Zero is not a valid number and zero is absent from the source digit set.
- Repetition of an allowed digit is permitted.
- Every shorter allowed number is automatically below the limit.
- Equal-length counting stops at the first limit digit not in the set.
- If every position matches, include the limit itself.

## Brute force: inspect every positive integer

```python
def at_most_n_brute(digits: list[str], limit: int) -> int:
    if (
        not digits
        or len(set(digits)) != len(digits)
        or any(len(digit) != 1 or digit not in "123456789" for digit in digits)
    ):
        raise ValueError("digits must be distinct strings from 1 through 9")
    if limit < 1:
        raise ValueError("limit must be positive")

    allowed = set(digits)
    return sum(
        all(character in allowed for character in str(value))
        for value in range(1, limit + 1)
    )
```

This takes `O(limit * log limit)` time.

## Better solution: generate only allowed numbers

```python
def at_most_n_generated(digits: list[str], limit: int) -> int:
    if (
        not digits
        or len(set(digits)) != len(digits)
        or any(len(digit) != 1 or digit not in "123456789" for digit in digits)
    ):
        raise ValueError("digits must be distinct strings from 1 through 9")
    if limit < 1:
        raise ValueError("limit must be positive")

    allowed = [int(digit) for digit in digits]
    stack = allowed[:]
    answer = 0
    while stack:
        value = stack.pop()
        if value > limit:
            continue
        answer += 1
        for digit in allowed:
            candidate = value * 10 + digit
            if candidate <= limit:
                stack.append(candidate)
    return answer
```

Generation costs `O(answer * k)` transitions and `O(answer)` worst-case space.

## Expert solution: count shorter lengths and tight prefixes

```python
def at_most_n_given_digit_set(digits: list[str], limit: int) -> int:
    if (
        not digits
        or len(set(digits)) != len(digits)
        or any(len(digit) != 1 or digit not in "123456789" for digit in digits)
    ):
        raise ValueError("digits must be distinct strings from 1 through 9")
    if limit < 1:
        raise ValueError("limit must be positive")

    allowed = sorted(digits)
    bound = str(limit)
    choices = len(allowed)
    answer = sum(choices**length for length in range(1, len(bound)))

    for index, bound_digit in enumerate(bound):
        remaining = len(bound) - index - 1
        smaller = sum(digit < bound_digit for digit in allowed)
        answer += smaller * choices**remaining
        if bound_digit not in allowed:
            return answer
    return answer + 1
```

At each position, the smaller-digit term counts every suffix exactly once, and
the equality path is unique.

**Complexity:** `O(k log limit)` time and `O(k)` space for the sorted digits.
