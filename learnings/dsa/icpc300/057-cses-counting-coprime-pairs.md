# ICPC300 057: CSES - Counting Coprime Pairs

**Source:** [CSES - Counting Coprime Pairs](https://cses.fi/problemset/task/2417/)  
**Pattern:** divisor frequencies + Möbius inversion  
**Goal:** Count unordered index pairs whose values have greatest common divisor
`1`.

## 1. First principles

For every divisor `d`, count how many input values are divisible by `d`.
There are `choose(count[d], 2)` pairs whose gcd is a multiple of `d`.

Möbius inversion isolates gcd `1`:

```text
answer = sum over d of mu[d] * choose(count[d], 2)
```

The Möbius value is `0` when `d` contains a squared prime factor, `1` for an
even number of distinct prime factors, and `-1` for an odd number.

## 2. Cases that decide correctness

| Case | Required behavior |
| --- | --- |
| Fewer than two values | Return `0`. |
| Pair containing `1` | It is always coprime. |
| Equal values greater than `1` | They are not coprime. |
| Duplicate `1` values | Every pair of them counts. |
| Common divisor has several primes | Inclusion-exclusion must not double subtract. |

Input values must be positive, as in the source problem.

## 3. Brute force: test every pair

```python
from math import gcd


def counting_coprime_pairs_brute(values: list[int]) -> int:
    if any(value <= 0 for value in values):
        raise ValueError("values must be positive")

    answer = 0
    for first in range(len(values)):
        for second in range(first + 1, len(values)):
            if gcd(values[first], values[second]) == 1:
                answer += 1
    return answer
```

**Complexity:** `O(n^2 log A)` time and `O(1)` extra space.

## 4. Better: count pairs by their exact gcd

Process possible gcd values downward. Pairs divisible by `d` include pairs
whose exact gcd is `d, 2d, 3d, ...`; subtract the already known larger gcds.

```python
def counting_coprime_pairs_exact_gcd(values: list[int]) -> int:
    if any(value <= 0 for value in values):
        raise ValueError("values must be positive")
    if len(values) < 2:
        return 0

    maximum = max(values)
    frequency = [0] * (maximum + 1)
    for value in values:
        frequency[value] += 1

    divisible_count = [0] * (maximum + 1)
    for divisor in range(1, maximum + 1):
        for multiple in range(divisor, maximum + 1, divisor):
            divisible_count[divisor] += frequency[multiple]

    exact_pairs = [0] * (maximum + 1)
    for divisor in range(maximum, 0, -1):
        count = divisible_count[divisor]
        pairs = count * (count - 1) // 2
        for multiple in range(2 * divisor, maximum + 1, divisor):
            pairs -= exact_pairs[multiple]
        exact_pairs[divisor] = pairs
    return exact_pairs[1]
```

**Complexity:** `O(A log A + n)` time and `O(A)` space.

## 5. Expert solution: Möbius inversion

A linear sieve computes all Möbius values. Divisor-multiple loops then count
the values divisible by each `d` and apply the signed formula directly.

```python
def counting_coprime_pairs_mobius(values: list[int]) -> int:
    if any(value <= 0 for value in values):
        raise ValueError("values must be positive")
    if len(values) < 2:
        return 0

    maximum = max(values)
    frequency = [0] * (maximum + 1)
    for value in values:
        frequency[value] += 1

    mobius = [0] * (maximum + 1)
    mobius[1] = 1
    primes: list[int] = []
    composite = [False] * (maximum + 1)
    for number in range(2, maximum + 1):
        if not composite[number]:
            primes.append(number)
            mobius[number] = -1
        for prime in primes:
            product = number * prime
            if product > maximum:
                break
            composite[product] = True
            if number % prime == 0:
                mobius[product] = 0
                break
            mobius[product] = -mobius[number]

    answer = 0
    for divisor in range(1, maximum + 1):
        if mobius[divisor] == 0:
            continue
        divisible = 0
        for multiple in range(divisor, maximum + 1, divisor):
            divisible += frequency[multiple]
        answer += mobius[divisor] * divisible * (divisible - 1) // 2
    return answer
```

### Why the expert code is correct

- `choose(divisible, 2)` counts every pair whose gcd is divisible by `d`.
- For any gcd `g`, the sum of `mu[d]` over divisors `d` of `g` is `1` when
  `g = 1` and `0` otherwise.
- Consequently every coprime pair contributes one and every other pair cancels
  to zero.

**Complexity:** `O(A log A + n)` time and `O(A)` space.

## 6. What to remember

```text
count[d] = values divisible by d
pairs divisible by d = choose(count[d], 2)
Mobius-weighted sum keeps exactly gcd-1 pairs
```
