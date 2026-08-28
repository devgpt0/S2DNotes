# 07. Calculate Matrix Row Sums

**What you learn:** Java java fundamentals APIs and problem solving.

## Problem

Return the sum of every row in a rectangular int[][].

## Example

~~~text
Input: matrix = [[1, 2], [3, 4, 5]]
Output: [3, 12]
~~~

## Simple idea

Create one result entry per row and traverse its values.

## Java solution

~~~java
static int[] rowSums(int[][] matrix) {
    int[] result = new int[matrix.length];
    for (int row = 0; row < matrix.length; row++)
        for (int value : matrix[row]) result[row] += value;
    return result;
}
~~~

## Complexity

- Time: `O(rows * columns)`
- Extra space: `O(rows)`

Try to write the solution yourself before reading the code.

