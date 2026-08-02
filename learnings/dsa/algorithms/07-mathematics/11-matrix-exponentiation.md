# Matrix Exponentiation

## Idea

A linear recurrence can be written as a matrix transformation. Binary
exponentiation then applies that transformation in `O(log exponent)` powers.

## Visual model

For Fibonacci numbers:

```text
[F(n+1)]   [1 1]^n [F(1)]
[F(n)  ] = [1 0]   [F(0)]
```

## Classroom board: transformations compose

```text
one matrix multiplication advances Fibonacci by 1 step
matrix^2 advances 2 steps
square again -> matrix^4 advances 4 steps
combine powers from index bits, just like fast exponentiation
```

## Steps

1. Build a transition matrix.
2. Start the result as the identity matrix.
3. Binary-exponentiate the transition.
4. Read the desired state from the powered matrix.

## First-principles derivation

A linear recurrence advances a fixed-size state by the same linear
transformation each step. Represent that transformation as a matrix.

Applying it `n` times is matrix power `M^n`, which binary exponentiation
computes in `O(log n)` matrix multiplications.

## Classroom board: Fibonacci as a state transition

```text
state k = [F(k+1), F(k)]

[1 1] [F(k+1)] = [F(k+2)]
[1 0] [F(k)  ]   [F(k+1)]

start state 0 = [F(1), F(0)] = [1,0]

one step: [1,1] -> F2=1, F1=1
two steps: [2,1] -> F3=2, F2=1
three steps: [3,2] -> F4=3, F3=2
```

Exponentiating the transition jumps many recurrence steps at once.

## Pattern recognition

Use it for a fixed-size linear recurrence with a huge index, repeated state
transitions, or counting fixed-state walks of exact length.

## Implementation: Fibonacci modulo `modulus`

### C++

```cpp
using Matrix = std::array<std::array<long long, 2>, 2>;

Matrix multiply(const Matrix& first, const Matrix& second, long long modulus) {
    Matrix result{};
    for (int row = 0; row < 2; ++row) for (int middle = 0; middle < 2; ++middle) {
        for (int column = 0; column < 2; ++column) result[row][column] = (result[row][column] + first[row][middle] * second[middle][column]) % modulus;
    }
    return result;
}

long long fibonacci(long long index, long long modulus) {
    Matrix result{{{1, 0}, {0, 1}}};
    Matrix base{{{1, 1}, {1, 0}}};
    while (index > 0) {
        if (index & 1) result = multiply(result, base, modulus);
        base = multiply(base, base, modulus);
        index >>= 1;
    }
    return result[0][1];
}
```

### Python

```python
def multiply(first: list[list[int]], second: list[list[int]], modulus: int) -> list[list[int]]:
    return [[
        sum(first[row][middle] * second[middle][column] for middle in range(2)) % modulus
        for column in range(2)
    ] for row in range(2)]


def fibonacci(index: int, modulus: int) -> int:
    result = [[1, 0], [0, 1]]
    base = [[1, 1], [1, 0]]
    while index:
        if index & 1:
            result = multiply(result, base, modulus)
        base = multiply(base, base, modulus)
        index >>= 1
    return result[0][1]
```

### Java

```java
static long[][] multiply(long[][] first, long[][] second, long modulus) {
    long[][] result = new long[2][2];
    for (int row = 0; row < 2; row++) for (int middle = 0; middle < 2; middle++) {
        for (int column = 0; column < 2; column++) {
            result[row][column] = (result[row][column] + first[row][middle] * second[middle][column]) % modulus;
        }
    }
    return result;
}

static long fibonacci(long index, long modulus) {
    long[][] result = {{1, 0}, {0, 1}};
    long[][] base = {{1, 1}, {1, 0}};
    while (index > 0) {
        if ((index & 1) == 1) result = multiply(result, base, modulus);
        base = multiply(base, base, modulus);
        index >>= 1;
    }
    return result[0][1];
}
```

## Why it works

The transition matrix advances the recurrence by one step. Matrix powers
compose steps, and binary exponentiation selects powers whose exponents sum to
the requested index.

## Complexity

For fixed `2 x 2` matrices, time is `O(log index)` and space is `O(1)`. A
general `k x k` matrix takes `O(k^3 log index)`.

## Common mistakes

- Using a non-identity initial result.
- Reading the wrong output cell.
- Overflowing products before modulo for large moduli.
