# 38. Reverse a LinkedList

**What you learn:** Java linkedlist questions APIs and problem solving.

## Problem

Reverse a LinkedList<Integer> in place.

## Example

~~~text
Input: values = [1, 2, 3]
Output: [3, 2, 1]
~~~

## Simple idea

Collections.reverse swaps through a list iterator.

## Java solution

~~~java
static void reverse(LinkedList<Integer> values) {
    Collections.reverse(values);
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(1) extra`

Try to write the solution yourself before reading the code.

