# ICPC300 106: CSES - Bracket Sequences II

**Source:** [CSES - Bracket Sequences II](https://cses.fi/problemset/task/2187/)  
**Pattern:** ballot counting with modular binomial coefficients  
**Goal:** Count, modulo `1_000_000_007`, ways to append brackets to the given
prefix so the final string has total length `n` and is a regular bracket
sequence.

## 1. Problem in plain words

Interpret `(` as `+1` and `)` as `-1`. A regular bracket sequence never has a
negative prefix balance and finishes at balance zero.

The supplied prefix is fixed. If it has already gone negative, used too many
opening brackets, or is longer than `n`, no completion exists.

## 2. First principles

A full sequence needs exactly `n/2` opening and `n/2` closing brackets. After
validating the prefix, let `a` be remaining openings, `b` its current balance,
and `r` the number of remaining positions.

Ignoring the nonnegative rule gives `C(r,a)` completions. By the reflection
principle, completions that ever go below zero correspond to choosing `a-1`
openings, giving `C(r,a-1)` bad paths. Therefore:

`valid = C(r,a) - C(r,a-1)`.

## 3. Cases that decide correctness

| Case | Required result |
| --- | --- |
| Odd total length | `0`. |
| Prefix balance ever negative | `0`. |
| Prefix already complete at length `n` | `1` only when balanced. |
| Too many opening brackets used | `0`. |
| Empty remaining range | Binomial helper must support `C(0,0) = 1`. |

## 4. Brute force: try every appended bracket string

```python
from itertools import product


def count_bracket_completions_brute_force(total_length: int, prefix: str) -> int:
    if total_length < 0 or any(character not in "()" for character in prefix):
        raise ValueError("length must be nonnegative and prefix contain brackets")
    if len(prefix) > total_length:
        return 0

    answer = 0
    remaining = total_length - len(prefix)
    for suffix in product("()", repeat=remaining):
        balance = 0
        valid = True
        for character in prefix + "".join(suffix):
            balance += 1 if character == "(" else -1
            if balance < 0:
                valid = False
                break
        answer += valid and balance == 0
    return answer
```

**Complexity:** `O(2^r n)` time for `r` appended positions.

## 5. Better: DP by remaining position and balance

```python
MODULO = 1_000_000_007


def count_bracket_completions_dp(total_length: int, prefix: str) -> int:
    if total_length < 0 or any(character not in "()" for character in prefix):
        raise ValueError("length must be nonnegative and prefix contain brackets")
    if len(prefix) > total_length:
        return 0

    balance = 0
    for character in prefix:
        balance += 1 if character == "(" else -1
        if balance < 0:
            return 0

    dp = [0] * (total_length + 1)
    dp[balance] = 1
    for _ in range(total_length - len(prefix)):
        next_dp = [0] * (total_length + 1)
        for current_balance, ways in enumerate(dp):
            if ways == 0:
                continue
            if current_balance + 1 <= total_length:
                next_dp[current_balance + 1] += ways
            if current_balance > 0:
                next_dp[current_balance - 1] += ways
        dp = [ways % MODULO for ways in next_dp]
    return dp[0]
```

**Complexity:** `O(n^2)` time and `O(n)` memory.

## 6. Expert solution: reflection principle and factorials

```python
MODULO = 1_000_000_007


def count_bracket_completions(total_length: int, prefix: str) -> int:
    if total_length < 0 or any(character not in "()" for character in prefix):
        raise ValueError("length must be nonnegative and prefix contain brackets")
    if total_length % 2 == 1 or len(prefix) > total_length:
        return 0

    balance = 0
    used_openings = 0
    for character in prefix:
        if character == "(":
            balance += 1
            used_openings += 1
        else:
            balance -= 1
        if balance < 0:
            return 0

    remaining = total_length - len(prefix)
    remaining_openings = total_length // 2 - used_openings
    remaining_closings = remaining - remaining_openings
    if remaining_openings < 0 or remaining_closings < 0:
        return 0
    if balance + remaining_openings - remaining_closings != 0:
        return 0

    factorial = [1] * (remaining + 1)
    for value in range(1, remaining + 1):
        factorial[value] = factorial[value - 1] * value % MODULO
    inverse_factorial = [1] * (remaining + 1)
    inverse_factorial[remaining] = pow(factorial[remaining], MODULO - 2, MODULO)
    for value in range(remaining, 0, -1):
        inverse_factorial[value - 1] = inverse_factorial[value] * value % MODULO

    def binomial(size: int, chosen: int) -> int:
        if chosen < 0 or chosen > size:
            return 0
        return (
            factorial[size]
            * inverse_factorial[chosen]
            % MODULO
            * inverse_factorial[size - chosen]
            % MODULO
        )

    return (
        binomial(remaining, remaining_openings)
        - binomial(remaining, remaining_openings - 1)
    ) % MODULO
```

### Why the expert code is correct

- Prefix validation rejects exactly the prefixes no regular sequence can
  repair.
- Remaining opening and closing counts are forced by total balance and length.
- `C(r,a)` counts all strings with those counts.
- Reflection at the first step below zero bijects invalid completions with
  strings counted by `C(r,a-1)`, so the difference counts exactly valid ones.

**Complexity:** `O(n)` preprocessing time and memory, then constant-time
binomial evaluation.

## 7. What to remember

After validating a bracket prefix, completion counting is a ballot problem:
all fixed-count paths minus paths reflected at their first negative balance.
