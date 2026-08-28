# 44. Rotate a LinkedList

**What you learn:** Java linkedlist questions APIs and problem solving.

## Problem

Rotate a list right by steps.

## Example

~~~text
Input: values = [1, 2, 3, 4], steps = 2
Output: [3, 4, 1, 2]
~~~

## Simple idea

Move the last value to the front after normalizing steps.

## Java solution

~~~java
static void rotateRight(LinkedList<Integer> values, int steps) {
    if (values.isEmpty()) return;
    int moves = Math.floorMod(steps, values.size());
    while (moves-- > 0) values.addFirst(values.removeLast());
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

