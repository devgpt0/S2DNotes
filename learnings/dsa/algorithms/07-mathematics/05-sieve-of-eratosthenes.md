# Sieve of Eratosthenes

## Idea

The sieve finds every prime up to a limit by marking multiples of each prime as
composite.

## Visual model

```text
2: mark 4,6,8,...
3: mark 9,12,15,...
start at p*p because smaller multiples were marked earlier
```

## Classroom board: primes through 12

```text
start candidates 2..12
prime 2 -> cross 4,6,8,10,12
prime 3 -> cross 9,12
remaining 2,3,5,7,11 are prime
```

## Steps

1. Assume all values from `2` onward are prime.
2. For each still-prime `p` with `p*p <= limit`, mark multiples from `p*p`.
3. Collect values still marked prime.

## First-principles derivation

Every composite number has a prime factor at most its square root. Once a prime
`p` is found, all multiples of `p` are composite.

Start marking at `p*p`; smaller multiples already had a smaller prime factor
and were marked earlier.

## Classroom board: primes through 20

```text
start:  2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20

p=2 mark: 4 6 8 10 12 14 16 18 20
left:   2 3 5 7 9 11 13 15 17 19

p=3 mark from 9: 9 12 15 18
left:   2 3 5 7 11 13 17 19

5*5 > 20, stop
primes = [2,3,5,7,11,13,17,19]
```

## Pattern recognition

Use it for many primality queries or prime preprocessing up to a moderate
maximum. Use segmented sieve when the upper limit is too large to store.

## Implementation

### C++

```cpp
std::vector<int> sieve(int limit) {
    std::vector<bool> isPrime(limit + 1, true);
    if (limit >= 0) isPrime[0] = false;
    if (limit >= 1) isPrime[1] = false;
    for (long long prime = 2; prime * prime <= limit; ++prime) {
        if (!isPrime[prime]) continue;
        for (long long multiple = prime * prime; multiple <= limit; multiple += prime) isPrime[multiple] = false;
    }
    std::vector<int> primes;
    for (int value = 2; value <= limit; ++value) if (isPrime[value]) primes.push_back(value);
    return primes;
}
```

### Python

```python
def sieve(limit: int) -> list[int]:
    is_prime = bytearray(b'\x01') * (limit + 1)
    if limit >= 0:
        is_prime[0] = 0
    if limit >= 1:
        is_prime[1] = 0
    prime = 2
    while prime * prime <= limit:
        if is_prime[prime]:
            start = prime * prime
            is_prime[start : limit + 1 : prime] = b'\x00' * (((limit - start) // prime) + 1)
        prime += 1
    return [value for value in range(2, limit + 1) if is_prime[value]]
```

### Java

```java
static List<Integer> sieve(int limit) {
    boolean[] isPrime = new boolean[limit + 1];
    Arrays.fill(isPrime, true);
    if (limit >= 0) isPrime[0] = false;
    if (limit >= 1) isPrime[1] = false;
    for (long prime = 2; prime * prime <= limit; prime++) {
        if (!isPrime[(int) prime]) continue;
        for (long multiple = prime * prime; multiple <= limit; multiple += prime) isPrime[(int) multiple] = false;
    }
    List<Integer> primes = new ArrayList<>();
    for (int value = 2; value <= limit; value++) if (isPrime[value]) primes.add(value);
    return primes;
}
```

## Why it works

Every composite number has a prime factor no larger than its square root. Its
smallest such factor marks it; prime values are never marked by a smaller prime.

## Complexity

Time is `O(n log log n)` and space is `O(n)`.

## Common mistakes

- Leaving `0` or `1` marked prime.
- Starting at `2*p` and doing unnecessary work.
- Computing `p*p` in a type that overflows.
