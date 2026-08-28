# 36. Add Values at LinkedList Ends

**What you learn:** Java linkedlist questions APIs and problem solving.

## Problem

Add first and last to the corresponding ends of a LinkedList.

## Example

~~~text
Input: values = [2, 3], first = 1, last = 4
Output: [1, 2, 3, 4]
~~~

## Simple idea

LinkedList provides constant-time end operations through its deque API.

## Java solution

~~~java
static void addEnds(LinkedList<Integer> values, int first, int last) {
    values.addFirst(first); values.addLast(last);
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

