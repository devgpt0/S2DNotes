# Focus300 014: LeetCode 65 - Valid Number

**Source:** [LeetCode 65](https://leetcode.com/problems/valid-number/)  
**Difficulty:** Hard  
**Pattern:** finite-state parsing

## Exact contract

Return whether a nonempty string is a valid decimal number. The mantissa is an
integer or decimal with an optional leading sign. It may be followed by `e` or
`E` and a signed or unsigned integer exponent. No other characters, internal
spaces, repeated signs, repeated decimal points, or fractional exponents are
valid.

## First principles

The grammar has three independent obligations: the mantissa needs at least one
digit, a decimal point may occur only before an exponent, and an exponent marker
must be followed by an integer containing at least one digit. A finite-state
machine records exactly which token may legally follow the parsed prefix.

## Cases that decide correctness

- `.1`, `3.`, `+6`, and `46.e3` are valid.
- `.`, `+`, `e9`, `1e`, and `1e+` are invalid.
- A sign is legal only at the start or immediately after `e` or `E`.
- The exponent cannot contain a decimal point.
- Leading or trailing whitespace is invalid.

## Brute force: split and validate grammar parts

```python
def is_number_parts(text: str) -> bool:
    if not text:
        return False

    def unsigned_digits(part: str) -> bool:
        return bool(part) and all("0" <= character <= "9" for character in part)

    def integer(part: str) -> bool:
        if part[:1] in {"+", "-"}:
            part = part[1:]
        return unsigned_digits(part)

    def decimal(part: str) -> bool:
        if part[:1] in {"+", "-"}:
            part = part[1:]
        if part.count(".") != 1:
            return False
        whole, fraction = part.split(".")
        return (
            (not whole or unsigned_digits(whole))
            and (not fraction or unsigned_digits(fraction))
            and bool(whole or fraction)
        )

    exponent_positions = [
        index for index, character in enumerate(text) if character in {"e", "E"}
    ]
    if len(exponent_positions) > 1:
        return False
    if not exponent_positions:
        return integer(text) or decimal(text)
    index = exponent_positions[0]
    return (integer(text[:index]) or decimal(text[:index])) and integer(
        text[index + 1 :]
    )
```

This mirrors the grammar directly but creates several substrings and rescans
parts.

## Better approach: track token obligations in one pass

```python
def is_number_flags(text: str) -> bool:
    if not text:
        return False
    seen_digit = False
    seen_decimal = False
    seen_exponent = False
    digit_after_exponent = True
    for index, character in enumerate(text):
        if "0" <= character <= "9":
            seen_digit = True
            if seen_exponent:
                digit_after_exponent = True
        elif character in {"+", "-"}:
            if index > 0 and text[index - 1] not in {"e", "E"}:
                return False
        elif character == ".":
            if seen_decimal or seen_exponent:
                return False
            seen_decimal = True
        elif character in {"e", "E"}:
            if seen_exponent or not seen_digit:
                return False
            seen_exponent = True
            digit_after_exponent = False
        else:
            return False
    return seen_digit and digit_after_exponent
```

The flags encode the same grammar in `O(n)` time and `O(1)` space.

## Expert solution: deterministic finite-state machine

```python
def is_number(text: str) -> bool:
    if not text:
        return False

    transitions = {
        0: {"sign": 1, "digit": 2, "dot": 3},
        1: {"digit": 2, "dot": 3},
        2: {"digit": 2, "dot": 4, "exponent": 6},
        3: {"digit": 5},
        4: {"digit": 5, "exponent": 6},
        5: {"digit": 5, "exponent": 6},
        6: {"sign": 7, "digit": 8},
        7: {"digit": 8},
        8: {"digit": 8},
    }

    state = 0
    for character in text:
        if "0" <= character <= "9":
            symbol = "digit"
        elif character in {"+", "-"}:
            symbol = "sign"
        elif character == ".":
            symbol = "dot"
        elif character in {"e", "E"}:
            symbol = "exponent"
        else:
            return False
        if symbol not in transitions[state]:
            return False
        state = transitions[state][symbol]
    return state in {2, 4, 5, 8}
```

Every state represents one valid grammar prefix, and every transition is one
legal next token. The accepting states are precisely complete integers,
decimals, or exponent integers.

**Complexity:** `O(n)` time and `O(1)` state space.
