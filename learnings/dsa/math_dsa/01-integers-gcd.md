# Integer Arithmetic, Divisibility, GCD, and LCM

Most early Codeforces math is careful integer arithmetic. Translate the words
into a divisibility statement before searching for a formula.

## Integer division and remainders

For positive `b`, `a // b` is the number of full groups and `a % b` is what is
left. `ceil(a / b)` for non-negative `a` is `(a + b - 1) // b`; never use a
float for this.

```python
def groups_needed(items: int, group_size: int) -> int:
    if items < 0 or group_size <= 0:
        raise ValueError("items must be non-negative and group_size positive")
    return (items + group_size - 1) // group_size


print(groups_needed(17, 5))
```

Output:

```text
4
```

For signed ceiling division, use `-((-a) // b)` after proving the sign rules;
do not reuse the non-negative shortcut.

## Divisibility and parity

`d` divides `n` exactly when `n % d == 0`. Track only parity when the result
depends solely on odd versus even: addition is XOR of parities and a product is
odd only when both factors are odd.

| Need | Exact test |
| --- | --- |
| `d` divides `n` | `n % d == 0` |
| same remainder modulo `m` | `(a - b) % m == 0` |
| exactly one is odd | `(a + b) % 2 == 1` |
| count multiples of positive `d` in `[1, n]` | `n // d` |

## GCD and LCM

`gcd(a, b)` is the largest positive common divisor. Euclid's replacement
`(a, b) -> (b, a % b)` preserves all common divisors. For nonzero values,
`lcm(a, b) = abs(a // gcd(a, b) * b)`.

```python
from math import gcd


def lcm(first: int, second: int) -> int:
    if first == 0 or second == 0:
        return 0
    return abs(first // gcd(first, second) * second)


print(gcd(48, 18))
print(lcm(12, 18))
```

Output:

```text
6
36
```

Use GCD for shared step sizes, reducing fractions, and whether `ax + by = c`
can have an integer solution. Use LCM for simultaneous periods. GCD is
`O(log(min(abs(a), abs(b))))`.

## Divisors come in pairs

If `d` divides `n`, then `n // d` also divides `n`; one is at most `sqrt(n)`.
Enumerate `d` only while `d * d <= n`, adding both values except at a square.
This is `O(sqrt(n))`, suitable for one or a few values, not `10^5` queries.

```python
def divisors(value: int) -> list[int]:
    if value <= 0:
        raise ValueError("value must be positive")
    result: list[int] = []
    divisor = 1
    while divisor * divisor <= value:
        if value % divisor == 0:
            result.append(divisor)
            if divisor * divisor != value:
                result.append(value // divisor)
        divisor += 1
    return sorted(result)


print(divisors(36))
```

Output:

```text
[1, 2, 3, 4, 6, 9, 12, 18, 36]
```

## Checklist

- Convert "minimum groups" to ceiling division.
- Convert "same schedule" or "repeats together" to LCM.
- Convert "can be formed from steps" to a GCD divisibility test.
- Check zero, one, negative values, and perfect squares explicitly.
