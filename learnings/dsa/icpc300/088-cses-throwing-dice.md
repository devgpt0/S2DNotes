# ICPC300 088: CSES - Throwing Dice

**Source:** [CSES - Throwing Dice](https://cses.fi/problemset/task/1096/)  
**Pattern:** linear-recurrence matrix exponentiation  
**Goal:** Count ordered sequences of die results `1..6` whose sum is `n`,
modulo `1_000_000_007`.

## 1. First principles

Let `ways[s]` count sequences totaling `s`. The final die contributes one of
six values:

```text
ways[s] = ways[s-1] + ... + ways[s-6]
ways[0] = 1
```

This order-six linear recurrence is a fixed `6 x 6` state transition. Raising
that matrix to power `n` handles enormous `n`.

## 2. Cases that decide correctness

- Sum zero has one empty sequence.
- Negative remaining sums contribute zero.
- Order matters: `1,2` and `2,1` are different.
- For `n <= 6`, one single-roll sequence is among the answers.
- Modulo reduction is required during multiplication.

## 3. Brute force: try every next roll

```python
def throwing_dice_brute(n: int, modulo: int = 1_000_000_007) -> int:
    if n < 0 or modulo <= 0:
        raise ValueError("n must be nonnegative and modulo positive")

    def count(remaining: int) -> int:
        if remaining == 0:
            return 1
        if remaining < 0:
            return 0
        return sum(count(remaining - roll) for roll in range(1, 7)) % modulo

    return count(n)
```

**Complexity:** `O(6^n)` upper-bound time and `O(n)` recursion space.

## 4. Better: linear dynamic programming

```python
def throwing_dice_dynamic_programming(n: int, modulo: int = 1_000_000_007) -> int:
    if n < 0 or modulo <= 0:
        raise ValueError("n must be nonnegative and modulo positive")

    ways = [0] * (n + 1)
    ways[0] = 1
    for total in range(1, n + 1):
        ways[total] = (
            sum(ways[total - roll] for roll in range(1, min(6, total) + 1)) % modulo
        )
    return ways[n]
```

**Complexity:** `O(n)` time and `O(n)` space.

## 5. Expert solution: matrix exponentiation

The state is `(ways[s], ways[s-1], ..., ways[s-5])`. The first transition row
sums the state; lower rows shift it.

```python
def throwing_dice_matrix(n: int, modulo: int = 1_000_000_007) -> int:
    if n < 0 or modulo <= 0:
        raise ValueError("n must be nonnegative and modulo positive")

    dimension = 6

    def multiply(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
        result = [[0] * dimension for _ in range(dimension)]
        for row in range(dimension):
            for middle in range(dimension):
                if left[row][middle] == 0:
                    continue
                for column in range(dimension):
                    result[row][column] += left[row][middle] * right[middle][column]
                    result[row][column] %= modulo
        return result

    transition = [[0] * dimension for _ in range(dimension)]
    transition[0] = [1] * dimension
    for row in range(1, dimension):
        transition[row][row - 1] = 1

    result = [
        [int(row == column) for column in range(dimension)] for row in range(dimension)
    ]
    power = transition
    exponent = n
    while exponent > 0:
        if exponent & 1:
            result = multiply(result, power)
        exponent //= 2
        if exponent > 0:
            power = multiply(power, power)

    return result[0][0]
```

### Why the expert code is correct

The initial state at sum zero is `(1,0,0,0,0,0)`. One transition applies the
six-term recurrence and shifts prior values. Therefore transition power `n`
produces `ways[n]` in its first state entry.

**Complexity:** `O(6^3 log n)` time and `O(6^2)` space.

## 6. What to remember

```text
fixed-order linear recurrence
-> keep the last six values as a state
-> exponentiate the constant transition matrix
```
