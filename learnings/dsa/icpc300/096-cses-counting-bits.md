# ICPC300 096: CSES - Counting Bits

**Source:** [CSES - Counting Bits](https://cses.fi/problemset/task/1146/)  
**Pattern:** binary place-value cycle counting

## Exact contract

Input is an integer `n` (`1 <= n <= 10^15`). Output the total number of `1`
bits in the binary representations of all integers from `1` through `n`.

## First principles

At bit value `half = 2^b`, bits repeat in cycles of `2*half`: `half` zeroes,
then `half` ones. Among `n+1` values from `0` through `n`, full cycles
contribute `full_cycles * half`; the partial cycle contributes every position
beyond its first `half` entries.

## Cases that decide correctness

- Including zero simplifies cycle lengths and adds no set bit.
- At `n = 2^k - 1`, each of `k` bits is set exactly `2^(k-1)` times.
- The last partial cycle contribution is clamped below by zero.
- The answer is much larger than `n` and requires wide integers.

## Brute force: count bits of every number

```python
def count_bits_brute(limit: int) -> int:
    return sum(value.bit_count() for value in range(1, limit + 1))
```

**Complexity:** `O(n log n)` bit work.

## Better: remove the highest set bit recursively

```python
def count_bits_recursive(limit: int) -> int:
    if limit == 0:
        return 0
    highest_bit = limit.bit_length() - 1
    highest_power = 1 << highest_bit
    bits_below_power = highest_bit * (highest_power >> 1)
    highest_bit_uses = limit - highest_power + 1
    return (
        bits_below_power
        + highest_bit_uses
        + count_bits_recursive(limit - highest_power)
    )
```

Each call removes one set bit, giving `O(log n)` time and recursion space.

## Expert solution: count every bit's cycles directly

```python
import sys


def solve() -> None:
    limit = int(sys.stdin.readline())
    value_count = limit + 1
    answer = 0
    half_cycle = 1

    while half_cycle <= limit:
        full_cycle = half_cycle << 1
        answer += value_count // full_cycle * half_cycle
        answer += max(0, value_count % full_cycle - half_cycle)
        half_cycle <<= 1
    print(answer)


if __name__ == "__main__":
    solve()
```

Every set bit belongs to exactly one bit position, and the cycle formula counts
that position over the entire closed range. Summing positions is therefore the
required total.

**Complexity:** `O(log n)` time and `O(1)` space.

