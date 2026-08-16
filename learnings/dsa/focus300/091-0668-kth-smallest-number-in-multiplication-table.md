# Focus300 091: LeetCode 668 - Kth Smallest Number in Multiplication Table

**Source:** [LeetCode 668](https://leetcode.com/problems/kth-smallest-number-in-multiplication-table/)  
**Difficulty:** Hard  
**Pattern:** binary search on an implicit sorted multiset

## Exact contract

The cell in one-indexed row `i` and column `j` contains `i*j`. Given
`1 <= rows, columns <= 30_000` and `1 <= position <= rows*columns`, return the
`position`th value in sorted order. Equal products occupy separate positions.

## First principles

Materializing the table is unnecessary. For a candidate value `x`, row `i`
contains `min(columns, x // i)` values at most `x`. Their sum is monotone in
`x`, so the first value whose count reaches `position` is exactly the answer.


## Classroom board: discard half the search space

```text
binary search keeps the side that can still contain the answer and throws
away the side that cannot.
```



## Step-by-step transformation

1. Compare the middle position with the target rule or boundary condition.
2. Discard the half that cannot still contain a valid answer.
3. Repeat until the remaining interval is exactly the split or value the problem asks for.
4. Convert the final boundary positions into the required output.

Binary-search style notes transform the input by shrinking the search space until only one valid boundary or value remains.


## Diagram: discard half the search space

```text

            sorted input
                |
                v
            check middle
                |
                v
            keep the half that can still work
                |
                v
            final boundary / value
```

Binary search keeps shrinking the input until only the valid boundary or value is left.

## Cases that decide correctness

- Products are a multiset: `6` can occur in several cells.
- The first position is `1`; the last is `rows*columns`.
- Rectangular tables use the same counting formula as square tables.
- Binary search must find the first feasible value, not merely any feasible one.
- Iterating over the smaller dimension reduces every count evaluation.

## Brute force: generate the complete table

```python
def kth_multiplication_value_brute(
    rows: int,
    columns: int,
    position: int,
) -> int:
    if type(rows) is not int or type(columns) is not int:
        raise TypeError("rows and columns must be integers")
    if not 1 <= rows <= 30_000 or not 1 <= columns <= 30_000:
        raise ValueError("rows and columns must be between 1 and 30,000")
    if type(position) is not int:
        raise TypeError("position must be an integer")
    if not 1 <= position <= rows * columns:
        raise ValueError("position is outside the table")

    products = [
        row * column for row in range(1, rows + 1) for column in range(1, columns + 1)
    ]
    products.sort()
    return products[position - 1]
```

This costs `O(rows*columns log(rows*columns))` time and
`O(rows*columns)` space.

## Better insight: count values instead of constructing them

The answer lies in `[1, rows*columns]`. Counting products at most `x` takes one
division per row and preserves duplicate occurrences automatically.

## Expert solution: lower-bound binary search on the value

```python
def kth_multiplication_value(rows: int, columns: int, position: int) -> int:
    if type(rows) is not int or type(columns) is not int:
        raise TypeError("rows and columns must be integers")
    if not 1 <= rows <= 30_000 or not 1 <= columns <= 30_000:
        raise ValueError("rows and columns must be between 1 and 30,000")
    if type(position) is not int:
        raise TypeError("position must be an integer")
    if not 1 <= position <= rows * columns:
        raise ValueError("position is outside the table")

    if rows > columns:
        rows, columns = columns, rows

    low = 1
    high = rows * columns
    while low < high:
        middle = (low + high) // 2
        count = sum(min(columns, middle // row) for row in range(1, rows + 1))
        if count >= position:
            high = middle
        else:
            low = middle + 1
    return low
```

The count predicate is false below the answer and true from the answer onward,
so lower-bound search returns the required multiset value.

**Complexity:** `O(min(rows, columns) * log(rows*columns))` time and `O(1)`
extra space.
