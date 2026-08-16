# Focus300 155: LeetCode 7 - Reverse Integer

**Source:** [LeetCode 7](https://leetcode.com/problems/reverse-integer/)  
**Difficulty:** Medium  
**Pattern:** decimal digit extraction with pre-overflow checks

## Exact contract

Reverse the decimal digits of a signed 32-bit integer. Preserve its sign and
discard leading zeros created by reversal. Return `0` when the reversed value
falls outside `[-2^31, 2^31-1]`.

## First principles

Repeatedly pop the last digit with `% 10` and append it with
`reversed_value*10 + digit`. Before appending, compare against the sign-specific
limit using `(limit-digit)//10`; this detects overflow before constructing an
out-of-range fixed-width value.


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

- Reversing `0` returns `0`.
- Trailing input zeros disappear from the result.
- The negative bound has magnitude `2^31`, one larger than the positive bound.
- The input itself must already be a signed 32-bit integer.
- Overflow returns zero rather than raising or clamping.

## Brute force: reverse a decimal string

```python
LOWER_BOUND = -(2**31)
UPPER_BOUND = 2**31 - 1


def reverse_integer_brute(number: int) -> int:
    if type(number) is not int or not LOWER_BOUND <= number <= UPPER_BOUND:
        raise ValueError("number must be a signed 32-bit integer")

    magnitude = int(str(abs(number))[::-1])
    reversed_number = -magnitude if number < 0 else magnitude
    return reversed_number if LOWER_BOUND <= reversed_number <= UPPER_BOUND else 0
```

This is concise but allocates strings and uses arbitrary-precision conversion.

## Better insight: check the next decimal append against the bound

The sign is fixed, so reverse only the nonnegative magnitude. A single division
comparison proves whether multiplying by ten and adding the next digit is safe.

## Expert solution: arithmetic reversal with guarded append

```python
LOWER_BOUND = -(2**31)
UPPER_BOUND = 2**31 - 1


def reverse_integer(number: int) -> int:
    if type(number) is not int or not LOWER_BOUND <= number <= UPPER_BOUND:
        raise ValueError("number must be a signed 32-bit integer")

    negative = number < 0
    magnitude = abs(number)
    limit = 2**31 if negative else UPPER_BOUND
    reversed_value = 0
    while magnitude:
        magnitude, digit = divmod(magnitude, 10)
        if reversed_value > (limit - digit) // 10:
            return 0
        reversed_value = reversed_value * 10 + digit
    return -reversed_value if negative else reversed_value
```

The guard maintains `reversed_value <= limit` after every digit append, so the
final signed result is valid exactly when the function does not return early.

**Complexity:** `O(log10(abs(number)+1))` time and `O(1)` space.
