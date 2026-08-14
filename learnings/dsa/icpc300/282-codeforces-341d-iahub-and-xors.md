# ICPC300 282: Codeforces 341D - Iahub and Xors

**Source:** [Codeforces 341D - Iahub and Xors](https://codeforces.com/problemset/problem/341/D)  
**Rating:** 2400  
**Pattern:** two-dimensional XOR difference grid and parity Fenwick trees  
**Goal:** On an initially zero square matrix, XOR a value into every cell of a
rectangle and answer rectangle-XOR queries.

Operations use one-based inclusive coordinates: update tuples are
`(1, x1, y1, x2, y2, value)` and query tuples are `(2, x1, y1, x2, y2)`.

## 1. First principles

A rectangle update becomes four point toggles in the two-dimensional
difference grid. A difference point `(x,y)` appears in a prefix XOR ending at
`(r,c)` only when both `r-x+1` and `c-y+1` are odd. Equivalently, its row and
column parities must match those of the prefix corner.

## 2. Cases that decide correctness

- Rectangle coordinates are inclusive and ordered.
- A corner at `size + 1` is outside the stored grid and is ignored.
- XORing the same value twice cancels it.
- Prefixes with row or column zero have XOR zero.
- Four parity combinations need independent Fenwick trees.

## 3. Brute force: update and scan cells

```python
def process_xor_matrix_brute(size: int, operations: list[tuple[int, ...]]) -> list[int]:
    if size <= 0:
        raise ValueError("size must be positive")
    matrix = [[0] * size for _ in range(size)]
    answers: list[int] = []
    for operation in operations:
        if operation[0] == 1 and len(operation) == 6:
            _, x1, y1, x2, y2, value = operation
            if not (1 <= x1 <= x2 <= size and 1 <= y1 <= y2 <= size and value >= 0):
                raise ValueError("invalid update")
            for row in range(x1 - 1, x2):
                for column in range(y1 - 1, y2):
                    matrix[row][column] ^= value
        elif operation[0] == 2 and len(operation) == 5:
            _, x1, y1, x2, y2 = operation
            if not (1 <= x1 <= x2 <= size and 1 <= y1 <= y2 <= size):
                raise ValueError("invalid query")
            answer = 0
            for row in range(x1 - 1, x2):
                for column in range(y1 - 1, y2):
                    answer ^= matrix[row][column]
            answers.append(answer)
        else:
            raise ValueError("unknown operation")
    return answers
```

**Complexity:** `O(size^2)` per operation in the worst case.

## 4. Better transition: query the XOR difference grid by parity

Each rectangle update toggles four difference points. Store a point in the
Fenwick tree selected by its row and column parity. A matrix-prefix XOR then
queries only the tree matching the prefix corner's parities.

## 5. Expert solution: four 2D Fenwick trees

```python
from array import array


def process_xor_matrix(size: int, operations: list[tuple[int, ...]]) -> list[int]:
    if size <= 0:
        raise ValueError("size must be positive")

    trees = [[array("I", [0]) * (size + 1) for _ in range(size + 1)] for _ in range(4)]

    def toggle(row: int, column: int, value: int) -> None:
        if row > size or column > size:
            return
        tree = trees[(row & 1) * 2 + (column & 1)]
        x = row
        while x <= size:
            y = column
            while y <= size:
                tree[x][y] ^= value
                y += y & -y
            x += x & -x

    def prefix(row: int, column: int) -> int:
        tree = trees[(row & 1) * 2 + (column & 1)]
        answer = 0
        x = row
        while x > 0:
            y = column
            while y > 0:
                answer ^= tree[x][y]
                y -= y & -y
            x -= x & -x
        return answer

    answers: list[int] = []
    for operation in operations:
        if operation[0] == 1 and len(operation) == 6:
            _, x1, y1, x2, y2, value = operation
            if not (
                1 <= x1 <= x2 <= size
                and 1 <= y1 <= y2 <= size
                and 0 <= value <= 0xFFFFFFFF
            ):
                raise ValueError("invalid update")
            toggle(x1, y1, value)
            toggle(x1, y2 + 1, value)
            toggle(x2 + 1, y1, value)
            toggle(x2 + 1, y2 + 1, value)
        elif operation[0] == 2 and len(operation) == 5:
            _, x1, y1, x2, y2 = operation
            if not (1 <= x1 <= x2 <= size and 1 <= y1 <= y2 <= size):
                raise ValueError("invalid query")
            answers.append(
                prefix(x2, y2)
                ^ prefix(x1 - 1, y2)
                ^ prefix(x2, y1 - 1)
                ^ prefix(x1 - 1, y1 - 1)
            )
        else:
            raise ValueError("unknown operation")
    return answers
```

### Why the expert code is correct

The four corner toggles are exactly the XOR difference representation of an
inclusive rectangle update. Expanding a matrix-prefix XOR shows that a
difference point survives precisely when both coordinate parities match the
prefix corner, which `prefix` enforces by choosing one tree. Ordinary
four-prefix inclusion-exclusion is XOR, so it returns the requested rectangle.

**Complexity:** `O(log^2 size)` time per operation and `O(size^2)` space.

## 6. What to remember

```text
rectangle XOR update -> four difference corners
prefix of reconstructed grid -> parity decides cancellation
rectangle query -> XOR four prefixes
```
