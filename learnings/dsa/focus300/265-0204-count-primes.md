# Focus300 265: LeetCode 204 - Count Primes

**Source:** [LeetCode 204](https://leetcode.com/problems/count-primes/)  
**Difficulty:** Medium  
**Pattern:** math / bit manipulation / counting

## Exact contract

Solve the numeric problem 'Count Primes' using the arithmetic or bitwise rule that the statement implies.

## First principles

Numeric problems usually hide a compact invariant: counts, prefix products, bit parity, or divisibility. Once that invariant is written down, the implementation becomes straightforward.

## Cases that decide correctness

- Zero values often need special handling.
- Negative values may change sign behavior but not the invariant itself.
- Repeated values can cancel or reinforce the desired quantity.
- The answer should usually be derived from a stable count or recurrence, not brute force.

## Brute force

```python
def count_primes_brute(n):
    def is_prime(x):
        if x < 2:
            return False
        for d in range(2, int(x ** 0.5) + 1):
            if x % d == 0:
                return False
        return True

    return sum(is_prime(x) for x in range(n))
```

Evaluate the full numeric property directly for each candidate.

## Better insight

Track the needed arithmetic state incrementally so each input element is processed once.

## Expert solution

```python
def count_primes(n):
    if n < 3:
        return 0
    sieve = [True] * n
    sieve[0] = sieve[1] = False
    for p in range(2, int(n ** 0.5) + 1):
        if sieve[p]:
            sieve[p * p : n : p] = [False] * len(sieve[p * p : n : p])
    return sum(sieve)
```

Translate the statement into a counting, prefix, parity, or divisibility invariant and update that invariant as you scan.

**Complexity:** Usually O(n) time and O(1) extra space.
