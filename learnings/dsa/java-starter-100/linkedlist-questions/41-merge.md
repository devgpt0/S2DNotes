# 41. Merge Sorted LinkedLists

**What you learn:** Java linkedlist questions APIs and problem solving.

## Problem

Merge two ascending LinkedLists into a new list.

## Example

~~~text
Input: left = [1, 4], right = [2, 3]
Output: [1, 2, 3, 4]
~~~

## Simple idea

Remove the smaller head and append it to the result.

## Java solution

~~~java
static LinkedList<Integer> merge(LinkedList<Integer> left, LinkedList<Integer> right) {
    LinkedList<Integer> result = new LinkedList<>();
    while (!left.isEmpty() && !right.isEmpty())
        result.add(left.peek() <= right.peek() ? left.poll() : right.poll());
    result.addAll(left); result.addAll(right);
    return result;
}
~~~

## Complexity

- Time: `O(n + m)`
- Extra space: `O(n + m)`

Try to write the solution yourself before reading the code.

