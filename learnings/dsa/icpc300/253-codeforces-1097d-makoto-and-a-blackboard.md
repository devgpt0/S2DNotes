# ICPC300 253: Codeforces 1097D - Makoto and a Blackboard

**Source:** [Codeforces 1097D - Makoto and a Blackboard](https://codeforces.com/problemset/problem/1097/D)  
**Rating:** 2200  
**Pattern:** independent prime-exponent Markov chains  
**Goal:** Starting from `number`, repeat `steps` times: replace the current
number by a uniformly random positive divisor. Return the expected final value
modulo `1_000_000_007`.

## 1. First principles

For a prime power `p^e`, choosing a uniform divisor chooses its new exponent
uniformly from `0..e`. Different prime exponents are chosen independently.

Track the exponent distribution of each prime factor through the same Markov
transition. Its expected contribution is

```text
sum(probability[exponent] * p^exponent)
```

The expected final number is the product of those independent expectations.

## 2. Cases that decide correctness

- With zero steps, the expected value is the original number.
- Prime exponent zero is absorbing.
- A current exponent `e` distributes probability equally to `0..e`.
- Distinct prime factors evolve independently.
- All probabilities use modular inverses.

## 3. Brute force: distribute probability across every divisor

```python
from math import isqrt


MODULO = 1_000_000_007


def expected_random_divisor_brute(number: int, steps: int) -> int:
    if number <= 0 or steps < 0:
        raise ValueError("number and steps must be nonnegative")

    def divisors(value: int) -> list[int]:
        result: list[int] = []
        for divisor in range(1, isqrt(value) + 1):
            if value % divisor == 0:
                result.append(divisor)
                if divisor * divisor != value:
                    result.append(value // divisor)
        return result

    distribution = {number: 1}
    for _ in range(steps):
        next_distribution: dict[int, int] = {}
        for value, probability in distribution.items():
            choices = divisors(value)
            share = probability * pow(len(choices), MODULO - 2, MODULO) % MODULO
            for choice in choices:
                next_distribution[choice] = (
                    next_distribution.get(choice, 0) + share
                ) % MODULO
        distribution = next_distribution
    return (
        sum(value * probability for value, probability in distribution.items()) % MODULO
    )
```

**Complexity:** Up to `O(steps * tau(number) * sqrt(number))` time and
`O(tau(number))` states.

## 4. Better transition: factor the random divisor choice

Uniform divisors correspond bijectively to independent choices of one exponent
per prime. Factoring once replaces a potentially huge divisor state space with
small chains whose lengths are the original prime exponents.

## 5. Expert solution: exponent-distribution DP

```python
MODULO = 1_000_000_007


def expected_random_divisor(number: int, steps: int) -> int:
    if number <= 0 or steps < 0:
        raise ValueError("number and steps must be nonnegative")

    factors: list[tuple[int, int]] = []
    remaining = number
    prime = 2
    while prime * prime <= remaining:
        if remaining % prime == 0:
            exponent = 0
            while remaining % prime == 0:
                remaining //= prime
                exponent += 1
            factors.append((prime, exponent))
        prime += 1
    if remaining > 1:
        factors.append((remaining, 1))

    answer = 1
    for prime, maximum_exponent in factors:
        distribution = [0] * (maximum_exponent + 1)
        distribution[maximum_exponent] = 1
        inverses = [
            pow(value, MODULO - 2, MODULO) for value in range(1, maximum_exponent + 2)
        ]
        for _ in range(steps):
            next_distribution = [0] * (maximum_exponent + 1)
            for exponent, probability in enumerate(distribution):
                share = probability * inverses[exponent] % MODULO
                for next_exponent in range(exponent + 1):
                    next_distribution[next_exponent] = (
                        next_distribution[next_exponent] + share
                    ) % MODULO
            distribution = next_distribution
        expected_power = 0
        power = 1
        for probability in distribution:
            expected_power = (expected_power + probability * power) % MODULO
            power = power * prime % MODULO
        answer = answer * expected_power % MODULO
    return answer
```

### Why the expert code is correct

A divisor of a factored number is uniquely determined by independently choosing
each exponent within its current range. The DP applies exactly that uniform
transition for every prime chain. Linearity computes each expected prime power,
and independence makes the expected product equal the product of expectations.

**Complexity:** `O(sum(steps * exponent^2) + sqrt(number))` time and
`O(max exponent)` DP space.

## 6. What to remember

```text
uniform divisor -> independent uniform exponent choices
one prime factor -> small Markov chain on exponents
independent factors -> multiply expected prime powers
```
