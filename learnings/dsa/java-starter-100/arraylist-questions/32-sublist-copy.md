# 32. Copy an ArrayList Slice

**What you learn:** Java arraylist questions APIs and problem solving.

## Problem

Return an independent list from index from inclusive to to exclusive.

## Example

~~~text
Input: values = [0, 1, 2, 3], from = 1, to = 3
Output: [1, 2]
~~~

## Simple idea

Wrap subList in a new ArrayList so it is not a live view.

## Java solution

~~~java
static ArrayList<Integer> slice(List<Integer> values, int from, int to) {
    return new ArrayList<>(values.subList(from, to));
}
~~~

## Complexity

- Time: `O(to - from)`
- Extra space: `O(to - from)`

Try to write the solution yourself before reading the code.

