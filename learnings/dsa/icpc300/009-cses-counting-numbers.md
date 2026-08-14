# ICPC300 009: CSES - Counting Numbers

**Source:** [CSES - Counting Numbers](https://cses.fi/problemset/task/2220/)  
**Pattern:** digit DP  
**Goal:** Count integers in `[lower, upper]` whose decimal representation has
no two equal adjacent digits.

## 1. First principles

Count valid numbers from `0` through a limit, then use:

```text
answer(lower, upper) = count(upper) - count(lower - 1)
```

Build the limit-length representation from left to right. The future needs
only four facts: digit position, previous real digit, whether a real digit has
started, and whether the prefix still equals the limit's prefix.

Leading zeros are padding, not decimal digits. Thus `0007` represents `7` and
does not contain an equal adjacent pair. The all-padding path represents `0`,
which is valid.

## 2. Cases that decide correctness

| Case | Required behavior |
| --- | --- |
| Range contains `0` | Count `0` once. |
| Number such as `7` | Leading padding zeros do not invalidate it. |
| `100` | Reject because the two real zeros are adjacent. |
| `101` | Accept. |
| `lower = upper` | Return either `0` or `1`. |

## 3. Brute force: inspect every number

Convert each integer to decimal text and compare adjacent characters.

```python
def counting_numbers_brute(lower: int, upper: int) -> int:
    if lower < 0 or lower > upper:
        raise ValueError("expected 0 <= lower <= upper")

    answer = 0
    for number in range(lower, upper + 1):
        digits = str(number)
        if all(digits[index] != digits[index - 1] for index in range(1, len(digits))):
            answer += 1
    return answer
```

**Complexity:** `O((upper - lower + 1) * digits)` time and `O(digits)` space.

## 4. Better: generate only valid numbers

Start positive numbers with `1` through `9`; every next digit may be anything
except the previous digit. Count generated values inside the range.

```python
def counting_numbers_backtracking(lower: int, upper: int) -> int:
    if lower < 0 or lower > upper:
        raise ValueError("expected 0 <= lower <= upper")

    answer = 1 if lower == 0 else 0

    def extend(value: int, previous_digit: int) -> None:
        nonlocal answer
        for digit in range(10):
            if digit == previous_digit:
                continue
            candidate = value * 10 + digit
            if candidate > upper:
                break
            if candidate >= lower:
                answer += 1
            extend(candidate, digit)

    for first_digit in range(1, 10):
        if first_digit > upper:
            break
        if first_digit >= lower:
            answer += 1
        extend(first_digit, first_digit)

    return answer
```

**Complexity:** proportional to the valid numbers up to `upper`, about
`O(9^digits)` in the worst case, with `O(digits)` recursion space.

## 5. Expert solution: digit DP

Memoize states. Once `tight` becomes false, all prefixes with the same
position, previous digit, and started flag share one answer.

```python
from functools import cache


def counting_numbers_digit_dp(lower: int, upper: int) -> int:
    if lower < 0 or lower > upper:
        raise ValueError("expected 0 <= lower <= upper")

    def count_up_to(limit: int) -> int:
        if limit < 0:
            return 0

        digits = tuple(int(character) for character in str(limit))
        no_previous_digit = 10

        @cache
        def count_suffixes(
            position: int,
            previous_digit: int,
            tight: bool,
            started: bool,
        ) -> int:
            if position == len(digits):
                return 1

            maximum_digit = digits[position] if tight else 9
            total = 0
            for digit in range(maximum_digit + 1):
                next_tight = tight and digit == maximum_digit
                if not started and digit == 0:
                    total += count_suffixes(
                        position + 1,
                        no_previous_digit,
                        next_tight,
                        False,
                    )
                elif digit != previous_digit:
                    total += count_suffixes(position + 1, digit, next_tight, True)
            return total

        return count_suffixes(0, no_previous_digit, True, False)

    return count_up_to(upper) - count_up_to(lower - 1)
```

### Why the expert code is correct

- The state contains every fact that can affect legal next digits; earlier
  digits have no other influence.
- A real next digit is accepted exactly when it differs from the previous real
  digit.
- `tight` prevents prefixes from exceeding the limit, while the terminal state
  counts each represented integer once, including zero.

**Complexity:** `O(digits * 11 * 2 * 2 * 10)` time and
`O(digits * 11 * 2 * 2)` cached states.

## 6. What to remember

```text
range answer = prefix count at upper - prefix count before lower
digit-DP state = position, previous digit, started, tight
leading zero padding does not participate in adjacency
```
