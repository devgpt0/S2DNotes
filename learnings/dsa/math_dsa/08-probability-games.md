# Probability, Expected Value, and Impartial Games

Probability problems are usually state DP with fractions or modular values;
game problems are usually state DP with winning conditions. Define the state
before writing a recurrence.

## Expected value and linearity

Expectation is a weighted average: `E[X] = sum(value * probability)`. Linearity
always holds: `E[X + Y] = E[X] + E[Y]`, even when `X` and `Y` are dependent.
This lets you count expected contributions one item at a time.

For a geometric process that succeeds each independent trial with probability
`p`, expected trials is `1 / p`. Do not use it when success probability changes
with state; write an expectation recurrence instead.

## Exact versus modular probability

Use rational arithmetic or floating point only when the output permits it.
When the answer is requested modulo a prime `M`, represent `a / b` as
`a * inverse(b) mod M`, after verifying `b % M != 0`.

```python
MODULUS = 1_000_000_007
probability = 3 * pow(4, MODULUS - 2, MODULUS) % MODULUS
print(probability * 4 % MODULUS)
```

Output:

```text
3
```

This output verifies the modular representation; it is not the decimal value
`0.75`.

## Nim and Grundy values

In normal Nim, a position is losing exactly when XOR of heap sizes is zero.
For a general impartial game, assign each state its Grundy value: the minimum
non-negative integer missing from its next states' Grundy values. XOR Grundy
values of independent subgames.

```python
def nim_winner(heaps: list[int]) -> str:
    if any(heap < 0 for heap in heaps):
        raise ValueError("heap sizes must be non-negative")
    xor_sum = 0
    for heap in heaps:
        xor_sum ^= heap
    return "First" if xor_sum else "Second"


print(nim_winner([1, 4, 5]))
```

Output:

```text
Second
```

Misere Nim changes the all-heaps-size-one case; do not reuse the normal rule
without checking the winning condition.

## Checklist

- Specify the random variable before taking its expectation.
- Use linearity to avoid tracking dependent events together.
- Use modular inverses only for denominators nonzero modulo the prime.
- For games, define whether the player with no move wins or loses.

For routine sample-space, conditional, distribution, and expectation questions,
continue with [probability patterns](12-probability-patterns.md).
