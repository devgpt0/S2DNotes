# 148. Magic Numbers — Codeforces 628D

**Source:** [Codeforces 628D - Magic Numbers](https://codeforces.com/problemset/problem/628/D)  
**Difficulty:** 2200

## 1. Problem in plain words

Count integers in the inclusive decimal-string range `[lower, upper]` that are divisible by `m` and satisfy a positional rule: digit `d` appears at every even one-based position and never appears at an odd one-based position. Print the count modulo `1_000_000_007`.

Source endpoints have equal length and no leading zero.

## 2. First principles

Build the number left to right. At zero-based position `i`, require `d` when `i` is odd and forbid `d` when `i` is even. A remainder state updates as `(old × 10 + digit) mod m`.

A tight flag counts valid fixed-length numbers not exceeding one bound. Inclusive range counting is `count(≤ upper) - count(≤ lower) + valid(lower)`.

## 3. Cases that define correctness

- The first digit cannot be zero.
- Digit `d` is forbidden at positions `1, 3, 5, ...` in one-based numbering.
- Lower and upper are included.
- Divisibility is checked only after all digits are placed.

## 4. Brute force

Inspect every integer in the range and check both conditions.

```python
MODULO = 1_000_000_007


def count_magic_numbers_brute_force(
    modulus: int, required_digit: int, lower: str, upper: str
) -> int:
    if (
        modulus <= 0
        or not 0 <= required_digit <= 9
        or len(lower) != len(upper)
        or not lower.isdigit()
        or not upper.isdigit()
        or lower[0] == "0"
        or upper[0] == "0"
        or int(lower) > int(upper)
    ):
        raise ValueError("invalid source parameters")

    def valid(text: str) -> bool:
        return int(text) % modulus == 0 and all(
            (int(character) == required_digit) == (index % 2 == 1)
            for index, character in enumerate(text)
        )

    answer = 0
    for value in range(int(lower), int(upper) + 1):
        answer += valid(str(value))
    return answer % MODULO
```

Time is `O((upper-lower+1) · digits)` and space is `O(digits)`.

## 5. Better approach: generate only positional candidates

Recursively place only digits allowed by the parity rule, then test the completed number's range and remainder.

```python
MODULO = 1_000_000_007


def count_magic_numbers_generated(
    modulus: int, required_digit: int, lower: str, upper: str
) -> int:
    if (
        modulus <= 0
        or not 0 <= required_digit <= 9
        or len(lower) != len(upper)
        or not lower.isdigit()
        or not upper.isdigit()
        or lower[0] == "0"
        or upper[0] == "0"
        or int(lower) > int(upper)
    ):
        raise ValueError("invalid source parameters")

    length = len(lower)
    answer = 0

    def generate(position: int, value: int, remainder: int) -> None:
        nonlocal answer
        if position == length:
            if int(lower) <= value <= int(upper) and remainder == 0:
                answer += 1
            return
        if position % 2:
            digits = (required_digit,)
        else:
            digits = tuple(digit for digit in range(10) if digit != required_digit)
        for digit in digits:
            if position == 0 and digit == 0:
                continue
            generate(
                position + 1,
                value * 10 + digit,
                (remainder * 10 + digit) % modulus,
            )

    generate(0, 0, 0)
    return answer % MODULO
```

This explores only positional candidates, but still takes exponential time in roughly half the digit positions.

## 6. Expert solution: tight remainder digit DP

For one upper bound, store counts by remainder and whether the constructed prefix is tight. Only source-legal digits are transitioned.

```python
MODULO = 1_000_000_007


def count_magic_numbers(
    modulus: int, required_digit: int, lower: str, upper: str
) -> int:
    if (
        modulus <= 0
        or not 0 <= required_digit <= 9
        or len(lower) != len(upper)
        or not lower.isdigit()
        or not upper.isdigit()
        or lower[0] == "0"
        or upper[0] == "0"
        or int(lower) > int(upper)
    ):
        raise ValueError("invalid source parameters")

    def count_at_most(bound: str) -> int:
        dp = [[0, 0] for _ in range(modulus)]
        dp[0][1] = 1
        for position, character in enumerate(bound):
            bound_digit = int(character)
            next_dp = [[0, 0] for _ in range(modulus)]
            for remainder in range(modulus):
                for tight in (0, 1):
                    ways = dp[remainder][tight]
                    if ways == 0:
                        continue
                    maximum = bound_digit if tight else 9
                    for digit in range(maximum + 1):
                        if position == 0 and digit == 0:
                            continue
                        if position % 2 == 1:
                            if digit != required_digit:
                                continue
                        elif digit == required_digit:
                            continue
                        next_remainder = (remainder * 10 + digit) % modulus
                        next_tight = int(tight == 1 and digit == bound_digit)
                        next_dp[next_remainder][next_tight] = (
                            next_dp[next_remainder][next_tight] + ways
                        ) % MODULO
            dp = next_dp
        return (dp[0][0] + dp[0][1]) % MODULO

    def lower_is_valid() -> bool:
        return int(lower) % modulus == 0 and all(
            (int(character) == required_digit) == (position % 2 == 1)
            for position, character in enumerate(lower)
        )

    return (
        count_at_most(upper) - count_at_most(lower) + int(lower_is_valid())
    ) % MODULO
```

## 7. Why the expert solution is correct

Each fixed-length positive number up to the bound follows one tight/non-tight path. Transitions allow exactly the required digit at even one-based positions and exclude it elsewhere, while the remainder transition equals decimal concatenation modulo `m`. Ending in remainder zero counts exactly valid divisible numbers; inclusive prefix subtraction handles both endpoints.

Time is `O(digits · m · 10)` and space is `O(m)`.
