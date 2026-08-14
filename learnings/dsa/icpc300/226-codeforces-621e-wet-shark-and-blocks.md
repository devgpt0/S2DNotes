# ICPC300 226: Codeforces 621E - Wet Shark and Blocks

**Source:** [Codeforces 621E - Wet Shark and Blocks](https://codeforces.com/problemset/problem/621/E)  
**Rating:** 2200  
**Pattern:** remainder transition matrix exponentiation  
**Goal:** Choose a digit from the given list for each of `length` positions.
Count sequences whose decimal value has the target remainder, modulo
`1_000_000_007`. Equal digits at different list positions are distinct choices.

## 1. First principles

Appending digit `d` transforms remainder `r` into

```text
(10 * r + d) % remainder_modulus
```

The same linear transition is applied at every position. Build a matrix whose
entry `(new, old)` counts list digits causing that transition, then raise the
matrix to `length`. The initial vector has one empty prefix at remainder zero.

## 2. Cases that decide correctness

- Digit zero is a valid choice and may create leading zeros.
- Duplicate list digits contribute duplicate transition counts.
- Every position independently chooses from the full list.
- The target must be a valid remainder.
- All matrix arithmetic uses `1_000_000_007`.

## 3. Brute force: enumerate every digit sequence

```python
from itertools import product


MODULO = 1_000_000_007


def block_remainder_count_brute(
    digits: list[int], length: int, target: int, remainder_modulus: int
) -> int:
    if (
        not digits
        or any(not 0 <= digit <= 9 for digit in digits)
        or length <= 0
        or remainder_modulus <= 0
        or not 0 <= target < remainder_modulus
    ):
        raise ValueError("invalid digits or remainder parameters")

    answer = 0
    for sequence in product(digits, repeat=length):
        remainder = 0
        for digit in sequence:
            remainder = (10 * remainder + digit) % remainder_modulus
        answer += remainder == target
    return answer % MODULO
```

**Complexity:** `O(length * len(digits)^length)` time and `O(length)` space.

## 4. Better transition: exponentiate the repeated linear step

A length-by-remainder DP applies the same matrix `length` times. Binary
exponentiation composes those identical transitions in logarithmically many
matrix multiplications.

## 5. Expert solution: transition matrix power

```python
MODULO = 1_000_000_007


def block_remainder_count(
    digits: list[int], length: int, target: int, remainder_modulus: int
) -> int:
    if (
        not digits
        or any(not 0 <= digit <= 9 for digit in digits)
        or length <= 0
        or remainder_modulus <= 0
        or not 0 <= target < remainder_modulus
    ):
        raise ValueError("invalid digits or remainder parameters")

    size = remainder_modulus
    transition = [[0] * size for _ in range(size)]
    for old_remainder in range(size):
        for digit in digits:
            new_remainder = (10 * old_remainder + digit) % size
            transition[new_remainder][old_remainder] += 1

    def multiply(first: list[list[int]], second: list[list[int]]) -> list[list[int]]:
        result = [[0] * size for _ in range(size)]
        for row in range(size):
            for middle in range(size):
                if first[row][middle] == 0:
                    continue
                coefficient = first[row][middle]
                for column in range(size):
                    result[row][column] = (
                        result[row][column] + coefficient * second[middle][column]
                    ) % MODULO
        return result

    def apply(matrix: list[list[int]], vector: list[int]) -> list[int]:
        return [
            sum(matrix[row][column] * vector[column] for column in range(size)) % MODULO
            for row in range(size)
        ]

    vector = [0] * size
    vector[0] = 1
    power = transition
    exponent = length
    while exponent:
        if exponent & 1:
            vector = apply(power, vector)
        power = multiply(power, power)
        exponent >>= 1
    return vector[target]
```

### Why the expert code is correct

One transition matrix application enumerates every possible next digit with
its multiplicity and sends each prefix to its exact new remainder. Matrix
composition represents consecutive positions, so the `length`-th power counts
all complete sequences. Applying it to the empty-prefix vector yields the exact
count for every final remainder.

**Complexity:** `O(x^3 log length)` time and `O(x^2)` space for modulus `x`.

## 6. What to remember

```text
append digit -> deterministic remainder transition
digit multiset -> transition multiplicities
same step many times -> matrix exponentiation
```
