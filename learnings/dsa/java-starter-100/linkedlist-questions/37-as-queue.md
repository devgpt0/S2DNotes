# 37. Use a LinkedList as a Queue

**What you learn:** Java linkedlist questions APIs and problem solving.

## Problem

Process all values in FIFO order and return their removal order.

## Example

~~~text
Input: values = [10, 20, 30]
Output: [10, 20, 30]
~~~

## Simple idea

Queue.offer adds and poll removes the head.

## Java solution

~~~java
static ArrayList<Integer> drain(LinkedList<Integer> values) {
    Queue<Integer> queue = values;
    ArrayList<Integer> result = new ArrayList<>();
    while (!queue.isEmpty()) result.add(queue.poll());
    return result;
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

