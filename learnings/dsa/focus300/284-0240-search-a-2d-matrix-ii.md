# Focus300 284: LeetCode 240 - Search a 2D Matrix II

**Source:** [LeetCode 240](https://leetcode.com/problems/search-a-2d-matrix-ii/)  
**Difficulty:** Medium  
**Pattern:** binary search over a sorted matrix

## Exact contract

Decide whether the target exists in a matrix whose rows are sorted and whose row boundaries are globally ordered.

## First principles

The matrix can be treated as one flattened sorted array because each row starts after the previous row ends. That lets binary search act on one index space instead of two.


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

- An empty matrix or empty row returns false immediately.
- Targets smaller than the first element or larger than the last element fail fast.
- Row boundaries must be mapped back to row and column indexes correctly.
- A target equal to a row start or row end must still be found.

## Brute force

```python
def search_matrix_brute(matrix, target):
    return any(target == num for row in matrix for num in row)
```

Scan every row and every cell until the target appears.

## Better insight

Binary search the flattened index space or first choose the row, then search within that row.

## Expert solution

```python
def search_matrix(matrix, target):
    if not matrix or not matrix[0]:
        return False
    r, c = 0, len(matrix[0]) - 1
    while r < len(matrix) and c >= 0:
        if matrix[r][c] == target:
            return True
        if matrix[r][c] > target:
            c -= 1
        else:
            r += 1
    return False
```

Use the sorted structure to reduce the candidate range logarithmically until the target is either matched or ruled out.

**Complexity:** O(log(m*n)) time and O(1) space.
