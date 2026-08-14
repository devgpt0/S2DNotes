# Focus300 156: LeetCode 8 - String to Integer (atoi)

**Source:** [LeetCode 8](https://leetcode.com/problems/string-to-integer-atoi/)  
**Difficulty:** Medium  
**Pattern:** deterministic prefix parser with saturation

## Exact contract

Skip leading space characters, consume at most one `+` or `-`, then consume the
longest following ASCII digit run. Ignore the remaining suffix. Return zero when
no digit is consumed, otherwise clamp the signed value to
`[-2^31, 2^31-1]`.

## First principles

Parsing is a one-way state sequence: leading spaces, optional sign, digits,
stop. While accumulating the magnitude, compare before `value*10 + digit` to
the sign-specific bound. Once overflow is certain, the clamped result is final;
later digits cannot bring a nonnegative magnitude back down.

## Cases that decide correctness

- Only the literal space character is skipped; tabs are not leading spaces.
- A sign without a following digit returns zero.
- Parsing stops at the first nondigit after the optional sign.
- Leading zeros do not affect overflow handling.
- Positive and negative clamping bounds differ by one in magnitude.

## Brute force: extract the prefix with a regular expression

```python
import re


LOWER_BOUND = -(2**31)
UPPER_BOUND = 2**31 - 1


def parse_integer_brute(text: str) -> int:
    if type(text) is not str or len(text) > 200:
        raise ValueError("text must be a string of length at most 200")
    if any(
        not character.isascii()
        or not (character.isalpha() or character.isdigit() or character in " + -.")
        for character in text
    ):
        raise ValueError("text contains a character outside the source contract")

    match = re.match(r"^ *([+-]?)([0-9]+)", text)
    if match is None:
        return 0
    magnitude = int(match.group(2))
    value = -magnitude if match.group(1) == "-" else magnitude
    return max(LOWER_BOUND, min(UPPER_BOUND, value))
```

This delegates prefix recognition and arbitrary-precision conversion to Python.

## Better insight: make every accepted transition explicit

An index and three short phases are enough. Accumulating manually also permits
an early bound check without constructing a huge integer.

## Expert solution: single-pass guarded parser

```python
LOWER_BOUND = -(2**31)
UPPER_BOUND = 2**31 - 1


def parse_integer(text: str) -> int:
    if type(text) is not str or len(text) > 200:
        raise ValueError("text must be a string of length at most 200")
    if any(
        not character.isascii()
        or not (character.isalpha() or character.isdigit() or character in " + -.")
        for character in text
    ):
        raise ValueError("text contains a character outside the source contract")

    index = 0
    while index < len(text) and text[index] == " ":
        index += 1

    sign = 1
    if index < len(text) and text[index] in "+-":
        sign = -1 if text[index] == "-" else 1
        index += 1

    limit = 2**31 if sign < 0 else UPPER_BOUND
    magnitude = 0
    while index < len(text) and "0" <= text[index] <= "9":
        digit = ord(text[index]) - ord("0")
        if magnitude > (limit - digit) // 10:
            return LOWER_BOUND if sign < 0 else UPPER_BOUND
        magnitude = magnitude * 10 + digit
        index += 1
    return sign * magnitude
```

The parser consumes exactly the allowed prefix, and the append invariant keeps
the magnitude within the appropriate signed bound.

**Complexity:** `O(n)` time and `O(1)` space.
