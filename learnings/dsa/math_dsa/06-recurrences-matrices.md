# Recurrences, Matrix Exponentiation, and Linear Recurrences

When `n` is enormous but the next state depends linearly on a fixed number of
previous states, raise a small transition matrix to the `n`th power. The
exponentiation costs `O(k^3 log n)` for a `k`-state matrix.

## From recurrence to state

For `F(n) = F(n-1) + F(n-2)`, keep state `[F(n), F(n-1)]`. One step is:

```text
[F(n+1)]   [1 1] [F(n)  ]
[F(n)  ] = [1 0] [F(n-1)]
```

The same construction handles constants by adding a state component that stays
one, such as `[F(n), F(n-1), 1]`.

## Reference implementation

The matrices must be square and the modulus positive. This is a template for
small state sizes; do not use cubic multiplication for a 500-state DP.

```python
def multiply(left: list[list[int]], right: list[list[int]], modulus: int) -> list[list[int]]:
    size = len(left)
    result = [[0] * size for _ in range(size)]
    for row in range(size):
        for middle in range(size):
            if left[row][middle] == 0:
                continue
            for column in range(size):
                result[row][column] = (
                    result[row][column] + left[row][middle] * right[middle][column]
                ) % modulus
    return result


def matrix_power(matrix: list[list[int]], exponent: int, modulus: int) -> list[list[int]]:
    if exponent < 0 or modulus <= 0 or not matrix or any(len(row) != len(matrix) for row in matrix):
        raise ValueError("matrix must be non-empty and square; exponent and modulus must be valid")
    size = len(matrix)
    result = [[int(row == column) for column in range(size)] for row in range(size)]
    base = [[value % modulus for value in row] for row in matrix]
    while exponent:
        if exponent & 1:
            result = multiply(result, base, modulus)
        base = multiply(base, base, modulus)
        exponent >>= 1
    return result


def fibonacci(index: int) -> int:
    if index < 0:
        raise ValueError("index must be non-negative")
    transition = [[1, 1], [1, 0]]
    return matrix_power(transition, index, 1_000_000_007)[0][1]


print(fibonacci(10))
```

Output:

```text
55
```

## Choosing the method

| Shape | Best first method |
| --- | --- |
| one recurrence, `n <= 10^7` | iterative DP |
| fixed-order linear recurrence, huge `n` | matrix exponentiation |
| recurrence order is large | Kitamasa / linear recurrence methods |
| nonlinear state transition | matrix multiplication does not apply directly |

Fast doubling is faster and shorter for Fibonacci specifically; matrix power is
the reusable method for several mutually dependent quantities.

## Checklist

- Write the state meaning before writing the matrix.
- Verify the transition on the first two or three terms.
- Use an identity matrix for exponent zero.
- Keep every entry modulo `m` if the requested answer is modulo `m`.
