# ICPC300 101: CSES - Prime Multiples

**Source:** [CSES - Prime Multiples](https://cses.fi/problemset/task/2185/)  
**Pattern:** inclusion-exclusion over prime subsets  
**Goal:** Count positive integers at most `n` that are divisible by at least one
of the given distinct primes.

## 1. Problem in plain words

For `n = 20` and primes `2, 5`, there are ten multiples of `2` and four
multiples of `5`. Two numbers, `10` and `20`, belong to both sets, so the answer
is `10 + 4 - 2 = 12`.

With up to twenty primes, iterating their subsets is practical; iterating all
numbers up to a very large `n` is not.

## 2. First principles

For a nonempty subset of primes whose product is `p`, exactly `floor(n / p)`
positive integers up to `n` are divisible by every prime in that subset.

Inclusion-exclusion adds odd-size subsets and subtracts even-size subsets. A
product larger than `n` contributes zero, and every extension of that subset
also contributes zero, so recursion can prune it safely.

## 3. Cases that decide correctness

| Case | Required behavior |
| --- | --- |
| One prime larger than `n` | It contributes zero. |
| One prime only | Return `floor(n / p)`. |
| Number divisible by several primes | Inclusion-exclusion counts it once. |
| Subset product would exceed `n` | Prune before multiplying. |
| Duplicate prime supplied to the reusable function | Reject it explicitly. |

## 4. Brute force: test every number

```python
def count_prime_multiples_brute_force(limit: int, primes: list[int]) -> int:
    if limit < 1 or any(prime < 2 for prime in primes):
        raise ValueError("limit must be positive and primes at least two")
    if len(set(primes)) != len(primes):
        raise ValueError("primes must be distinct")
    return sum(
        any(value % prime == 0 for prime in primes) for value in range(1, limit + 1)
    )
```

**Complexity:** `O(nk)` time and `O(1)` auxiliary memory.

## 5. Better for moderate limits: build the union of multiples

Generating each prime's multiples avoids testing unrelated numbers, but the
set may still contain `O(n)` values.

```python
def count_prime_multiples_set(limit: int, primes: list[int]) -> int:
    if limit < 1 or any(prime < 2 for prime in primes):
        raise ValueError("limit must be positive and primes at least two")
    if len(set(primes)) != len(primes):
        raise ValueError("primes must be distinct")

    divisible: set[int] = set()
    for prime in primes:
        divisible.update(range(prime, limit + 1, prime))
    return len(divisible)
```

**Complexity:** `O(sum(n / p))` insertions and up to `O(n)` memory.

## 6. Expert solution: pruned inclusion-exclusion

```python
def count_prime_multiples(limit: int, primes: list[int]) -> int:
    if limit < 1 or any(prime < 2 for prime in primes):
        raise ValueError("limit must be positive and primes at least two")
    if len(set(primes)) != len(primes):
        raise ValueError("primes must be distinct")

    answer = 0

    def enumerate_subsets(start: int, product: int, sign: int) -> None:
        nonlocal answer
        for index in range(start, len(primes)):
            prime = primes[index]
            if product > limit // prime:
                continue
            next_product = product * prime
            answer += sign * (limit // next_product)
            enumerate_subsets(index + 1, next_product, -sign)

    enumerate_subsets(0, 1, 1)
    return answer
```

### Why the expert code is correct

- Each nonempty prime subset is generated once in increasing index order.
- Its product divides exactly the numbers belonging to every divisibility set
  in that subset.
- Alternating signs are exactly the inclusion-exclusion formula, so a number
  divisible by any positive number of listed primes has final coefficient one.
- The division check proves a product would exceed `limit` without overflowing;
  such a subset and all its supersets contribute zero.

**Complexity:** `O(2^k)` time in the worst case and `O(k)` recursion space.

## 7. What to remember

When `n` is huge but the number of divisibility conditions is near twenty,
enumerate condition subsets, not candidate integers.
