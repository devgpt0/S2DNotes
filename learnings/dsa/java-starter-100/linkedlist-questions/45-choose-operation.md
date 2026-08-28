# 45. Choose the Right List Operation

**What you learn:** Java linkedlist questions APIs and problem solving.

## Problem

Implement repeated end insertion using LinkedList's Deque view.

## Example

~~~text
Input: values = [1, 2], value = 3
Output: [1, 2, 3]
~~~

## Simple idea

LinkedList is useful at ends; ArrayList is usually better for indexed access.

## Java solution

~~~java
static void append(LinkedList<Integer> values, int value) {
    Deque<Integer> deque = values;
    deque.addLast(value);
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

