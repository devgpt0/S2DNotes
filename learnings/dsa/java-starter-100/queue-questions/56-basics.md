# 56. Use a Queue with ArrayDeque

**What you learn:** Java queue questions APIs and problem solving.

## Problem

Enqueue two values and return the first value removed.

## Example

~~~text
Input: offer(10), offer(20), poll()
Output: 10
~~~

## Simple idea

offer adds at the tail and poll removes from the head.

## Java solution

~~~java
static int firstOut() {
    Queue<Integer> queue = new ArrayDeque<>();
    queue.offer(10); queue.offer(20);
    return queue.poll();
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

