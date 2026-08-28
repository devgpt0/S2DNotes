# 33. Build an ArrayList Matrix

**What you learn:** Java arraylist questions APIs and problem solving.

## Problem

Create an n by n matrix with 1 on the diagonal and 0 elsewhere.

## Example

~~~text
Input: n = 3
Output: [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
~~~

## Simple idea

Create a fresh inner list for every row.

## Java solution

~~~java
static ArrayList<ArrayList<Integer>> identity(int n) {
    ArrayList<ArrayList<Integer>> matrix = new ArrayList<>();
    for (int r = 0; r < n; r++) {
        ArrayList<Integer> row = new ArrayList<>();
        for (int c = 0; c < n; c++) row.add(r == c ? 1 : 0);
        matrix.add(row);
    }
    return matrix;
}
~~~

## Complexity

- Time: `O(n²)`
- Extra space: `O(n²)`

Try to write the solution yourself before reading the code.

