# Prime Factorization by Trial Division

## Idea

Repeatedly divide by the smallest possible factor. After testing through the
square root of the remaining number, any remainder greater than `1` is prime.

## Visual model

```text
360 -> 2^3 * 45 -> 2^3 * 3^2 * 5
```

## Classroom board: factor `72`

```text
72 /2 =36, /2=18, /2=9 -> factor 2^3
9 /3=3, /3=1          -> factor 3^2
72 = 2^3 * 3^2
```

## Steps

1. Try divisors from `2` while `divisor * divisor <= remaining`.
2. Count how many times each divisor divides the number.
3. Add any remaining value greater than `1` with exponent `1`.

## First-principles derivation

If `n` is composite, its smallest factor is at most `sqrt(n)`. Repeatedly
remove each small prime factor; after that, any remaining value greater than
one must itself be prime.

The product of all recorded prime powers always equals the original number.

## Classroom board: factor 84

```text
84 / 2 = 42   record 2
42 / 2 = 21   record 2
21 / 3 =  7   record 3
next divisor squared > 7
record remaining 7

84 = 2^2 * 3 * 7
check: 4 * 3 * 7 = 84
```

## Pattern recognition

Use trial division for one or a few values up to about `10^12`. For many small
values, precompute smallest prime factors with a sieve.

## Implementation

### C++

```cpp
std::vector<std::pair<long long, int>> factorize(long long value) {
    std::vector<std::pair<long long, int>> factors;
    for (long long divisor = 2; divisor <= value / divisor; ++divisor) {
        if (value % divisor != 0) continue;
        int exponent = 0;
        while (value % divisor == 0) {
            value /= divisor;
            ++exponent;
        }
        factors.push_back({divisor, exponent});
    }
    if (value > 1) factors.push_back({value, 1});
    return factors;
}
```

### Python

```python
def factorize(value: int) -> list[tuple[int, int]]:
    factors: list[tuple[int, int]] = []
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor:
            divisor += 1
            continue
        exponent = 0
        while value % divisor == 0:
            value //= divisor
            exponent += 1
        factors.append((divisor, exponent))
        divisor += 1
    if value > 1:
        factors.append((value, 1))
    return factors
```

### Java

```java
static List<long[]> factorize(long value) {
    List<long[]> factors = new ArrayList<>();
    for (long divisor = 2; divisor <= value / divisor; divisor++) {
        if (value % divisor != 0) continue;
        int exponent = 0;
        while (value % divisor == 0) {
            value /= divisor;
            exponent++;
        }
        factors.add(new long[] {divisor, exponent});
    }
    if (value > 1) factors.add(new long[] {value, 1});
    return factors;
}
```

## Why it works

After smaller factors are removed, the first divisor found must be prime. If a
composite remainder existed after the loop, it would have a factor within the
tested range.

## Complexity

Worst-case time is `O(sqrt(value))`; output space is `O(log value)`.

## Common mistakes

- Forgetting the final prime remainder.
- Factoring `0` or negative values without a defined contract.
- Using `divisor * divisor` where multiplication can overflow.
