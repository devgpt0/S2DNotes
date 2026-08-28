# 51. Find Next Greater Elements

**What you learn:** Java stack questions APIs and problem solving.

## Problem

For each value, return the first later value that is greater, or -1.

## Example

~~~text
Input: values = [2, 1, 3]
Output: [3, 3, -1]
~~~

## Simple idea

A monotonic stack holds indexes whose answer is not known yet.

## Java solution

~~~java
static int[] nextGreater(int[] values) {
    int[] result = new int[values.length]; Arrays.fill(result, -1);
    Deque<Integer> indexes = new ArrayDeque<>();
    for (int i = 0; i < values.length; i++) {
        while (!indexes.isEmpty() && values[i] > values[indexes.peek()])
            result[indexes.pop()] = values[i];
        indexes.push(i);
    }
    return result;
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

