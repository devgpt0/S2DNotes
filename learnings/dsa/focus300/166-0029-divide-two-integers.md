# Focus300 166: LeetCode 29 - Divide Two Integers

**Source:** [LeetCode 29](https://leetcode.com/problems/divide-two-integers/)  
**Difficulty:** Medium  
**Pattern:** binary long division with shifts

## Exact contract

Divide two signed 32-bit integers without using multiplication, division, or
modulo. Truncate the quotient toward zero. The divisor is nonzero; clamp the
sole overflowing result, `-2^31 / -1`, to `2^31 - 1`.

## First principles

Work with nonnegative magnitudes and apply the sign at the end. Subtracting one
divisor at a time constructs the quotient but is slow. Binary long division
instead tests shifted divisor multiples from largest to smallest; accepting
`divisor << bit` adds exactly `1 << bit` to the quotient.

## Cases that decide correctness

- A zero dividend returns zero.
- Magnitude smaller than the divisor returns zero.
- Opposite signs produce a negative truncated quotient.
- `-2^31 / -1` is the only mathematical result above the signed 32-bit range.
- Python floor division is not equivalent to truncation for negative values.

## Brute force: repeated subtraction

```python
LOWER_BOUND = -(2**31)
UPPER_BOUND = 2**31 - 1


def divide_integers_brute(dividend: int, divisor: int) -> int:
    if type(dividend) is not int or not LOWER_BOUND <= dividend <= UPPER_BOUND:
        raise ValueError("dividend must be a signed 32-bit integer")
    if (
        type(divisor) is not int
        or divisor == 0
        or not LOWER_BOUND <= divisor <= UPPER_BOUND
    ):
        raise ValueError("divisor must be a nonzero signed 32-bit integer")
    if dividend == LOWER_BOUND and divisor == -1:
        return UPPER_BOUND

    remainder = abs(dividend)
    divisor_magnitude = abs(divisor)
    quotient = 0
    while remainder >= divisor_magnitude:
        remainder -= divisor_magnitude
        quotient += 1
    return -quotient if (dividend < 0) != (divisor < 0) else quotient
```

Its running time is proportional to the quotient magnitude.

## Better insight: subtract powers-of-two multiples in descending order

A shifted divisor represents a quotient bit. Greedily accepting every shifted
multiple that fits is ordinary binary long division and leaves a remainder
smaller than the divisor.

## Expert solution: bitwise long division

```python
LOWER_BOUND = -(2**31)
UPPER_BOUND = 2**31 - 1


def divide_integers(dividend: int, divisor: int) -> int:
    if type(dividend) is not int or not LOWER_BOUND <= dividend <= UPPER_BOUND:
        raise ValueError("dividend must be a signed 32-bit integer")
    if (
        type(divisor) is not int
        or divisor == 0
        or not LOWER_BOUND <= divisor <= UPPER_BOUND
    ):
        raise ValueError("divisor must be a nonzero signed 32-bit integer")
    if dividend == LOWER_BOUND and divisor == -1:
        return UPPER_BOUND

    remainder = abs(dividend)
    divisor_magnitude = abs(divisor)
    quotient = 0
    for bit in range(31, -1, -1):
        shifted = divisor_magnitude << bit
        if shifted <= remainder:
            remainder -= shifted
            quotient |= 1 << bit
    return -quotient if (dividend < 0) != (divisor < 0) else quotient
```

Each accepted bit subtracts its exact divisor multiple, so the final quotient
and remainder satisfy truncating integer division on magnitudes.

**Complexity:** `O(32)` time and `O(1)` space for signed 32-bit inputs.
