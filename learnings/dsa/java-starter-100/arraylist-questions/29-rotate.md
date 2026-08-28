# 29. Rotate an ArrayList Right

**What you learn:** Java arraylist questions APIs and problem solving.

## Problem

Rotate a mutable list right by steps.

## Example

~~~text
Input: values = [1, 2, 3, 4], steps = 1
Output: [4, 1, 2, 3]
~~~

## Simple idea

Collections.rotate handles negative and oversized distances.

## Java solution

~~~java
static void rotateRight(ArrayList<Integer> values, int steps) {
    Collections.rotate(values, steps);
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(1) extra`

Try to write the solution yourself before reading the code.

