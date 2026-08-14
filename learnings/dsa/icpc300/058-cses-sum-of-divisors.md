# ICPC300 058: CSES - Sum of Divisors

**Source:** [CSES - Sum of Divisors](https://cses.fi/problemset/task/1082/)  
**Pattern:** floor-quotient grouping  
**Goal:** Compute `sigma(1) + sigma(2) + ... + sigma(n)` modulo
`1_000_000_007`, where `sigma(x)` is the sum of positive divisors of `x`.

## 1. First principles

Reverse which quantity is counted. Divisor `d` contributes once to every
multiple `d, 2d, ...` up to `n`, so it contributes `d * floor(n / d)` in
total:

```text
sum from x=1 to n of sigma(x)
    = sum from d=1 to n of d * floor(n / d)
```

The quotient `floor(n / d)` changes only `O(sqrt(n))` times. If it equals `q`
at `left`, it remains `q` through `right = floor(n / q)`. Sum that whole
arithmetic interval at once.

## 2. Cases that decide correctness

| Case | Required behavior |
| --- | --- |
| `n = 1` | Return `1`. |
| Perfect-square divisor enumeration | Count the square root once. |
| Final quotient group | Stop exactly at `n`. |
| Large intermediate products | Reduce modulo after multiplication. |
| Group sum | Use the inclusive arithmetic-series formula. |

## 3. Brute force: factor every number

```python
from math import isqrt


def sum_of_divisors_brute(n: int, modulo: int = 1_000_000_007) -> int:
    if n <= 0 or modulo <= 0:
        raise ValueError("n and modulo must be positive")

    answer = 0
    for number in range(1, n + 1):
        divisor_sum = 0
        for divisor in range(1, isqrt(number) + 1):
            if number % divisor != 0:
                continue
            divisor_sum += divisor
            paired_divisor = number // divisor
            if paired_divisor != divisor:
                divisor_sum += paired_divisor
        answer = (answer + divisor_sum) % modulo
    return answer
```

**Complexity:** `O(n sqrt(n))` time and `O(1)` extra space.

## 4. Better: sum each divisor's contribution

Instead of factoring each number, iterate possible divisors once.

```python
def sum_of_divisors_by_contribution(n: int, modulo: int = 1_000_000_007) -> int:
    if n <= 0 or modulo <= 0:
        raise ValueError("n and modulo must be positive")

    answer = 0
    for divisor in range(1, n + 1):
        answer += divisor * (n // divisor)
        answer %= modulo
    return answer
```

**Complexity:** `O(n)` time and `O(1)` space.

## 5. Expert solution: group equal floor quotients

All divisors from `left` through `n // (n // left)` share the same quotient.
Their contribution is that quotient times their arithmetic-series sum.

```python
def sum_of_divisors_quotient_groups(n: int, modulo: int = 1_000_000_007) -> int:
    if n <= 0 or modulo <= 0:
        raise ValueError("n and modulo must be positive")

    answer = 0
    left = 1
    while left <= n:
        quotient = n // left
        right = n // quotient
        interval_sum = (left + right) * (right - left + 1) // 2
        answer += (quotient % modulo) * (interval_sum % modulo)
        answer %= modulo
        left = right + 1
    return answer
```

### Why the expert code is correct

- Each divisor's total contribution is exactly `d * floor(n / d)`.
- `right = floor(n / quotient)` is the final divisor with the current quotient,
  so groups are disjoint and cover `1..n`.
- The arithmetic-series formula sums every divisor in a group exactly once.

**Complexity:** `O(sqrt(n))` time and `O(1)` space.

## 6. What to remember

```text
swap sums: divisor d appears in floor(n / d) numbers
equal floor quotients form O(sqrt(n)) intervals
right endpoint for left = n // (n // left)
```
