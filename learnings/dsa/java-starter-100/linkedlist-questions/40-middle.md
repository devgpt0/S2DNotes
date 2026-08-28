# 40. Find the Middle LinkedList Value

**What you learn:** Java linkedlist questions APIs and problem solving.

## Problem

Return the middle value; for even length return the second middle.

## Example

~~~text
Input: values = [1, 2, 3, 4]
Output: 3
~~~

## Simple idea

A slow iterator moves once while a fast iterator moves twice. Java's LinkedList
already exposes the indexed operation needed for this beginner exercise.

## Java solution

~~~java
static int middle(LinkedList<Integer> values) {
    return values.get(values.size() / 2);
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.
