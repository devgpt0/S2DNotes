# ICPC300 087: CSES - Fibonacci Numbers

**Source:** [CSES - Fibonacci Numbers](https://cses.fi/problemset/task/1722/)  
**Pattern:** fast doubling  
**Goal:** Compute `F(n)` modulo `1_000_000_007`, where `F(0)=0`, `F(1)=1`.

## 1. First principles

Doubling identities derive `F(2k)` and `F(2k+1)` from the pair
`(F(k), F(k+1))`:

```text
F(2k)   = F(k) * (2F(k+1) - F(k))
F(2k+1) = F(k)^2 + F(k+1)^2
```

Halving `n` each recursion level gives logarithmic time.

## 2. Cases that decide correctness

- `F(0)=0` is the recursion base.
- `F(1)=1` follows from the returned pair.
- Modular subtraction must remain valid when negative before reduction.
- Odd `n` returns `(F(2k+1), F(2k)+F(2k+1))`.
- Huge `n` requires logarithmic, not linear, work.

## 3. Brute force: direct recurrence

```python
def fibonacci_brute(n: int, modulo: int = 1_000_000_007) -> int:
    if n < 0 or modulo <= 0:
        raise ValueError("n must be nonnegative and modulo positive")

    def calculate(index: int) -> int:
        if index < 2:
            return index
        return (calculate(index - 1) + calculate(index - 2)) % modulo

    return calculate(n)
```

**Complexity:** `O(2^n)` time and `O(n)` recursion space.

## 4. Better: iterative dynamic programming

```python
def fibonacci_iterative(n: int, modulo: int = 1_000_000_007) -> int:
    if n < 0 or modulo <= 0:
        raise ValueError("n must be nonnegative and modulo positive")

    previous, current = 0, 1
    for _ in range(n):
        previous, current = current, (previous + current) % modulo
    return previous
```

**Complexity:** `O(n)` time and `O(1)` space.

## 5. Expert solution: fast doubling

```python
def fibonacci_fast_doubling(n: int, modulo: int = 1_000_000_007) -> int:
    if n < 0 or modulo <= 0:
        raise ValueError("n must be nonnegative and modulo positive")

    def pair(index: int) -> tuple[int, int]:
        if index == 0:
            return 0, 1
        first, second = pair(index // 2)
        doubled = first * (2 * second - first) % modulo
        doubled_next = (first * first + second * second) % modulo
        if index % 2 == 0:
            return doubled, doubled_next
        return doubled_next, (doubled + doubled_next) % modulo

    return pair(n)[0]
```

### Why the expert code is correct

The recursive pair is exact at zero. The two identities transform an exact
half-index pair into the exact even-index pair, and the Fibonacci recurrence
then produces the odd pair.

**Complexity:** `O(log n)` time and `O(log n)` recursion space.

## 6. What to remember

```text
return F(n) and F(n+1) together
halve n
rebuild even/odd pair with doubling identities
```
