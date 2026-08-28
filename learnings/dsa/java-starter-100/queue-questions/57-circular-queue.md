# 57. Build a Circular Queue

**What you learn:** Java queue questions APIs and problem solving.

## Problem

Implement a fixed-capacity integer queue with offer and poll.

## Example

~~~text
Input: capacity=2; offer(1), offer(2), poll()
Output: 1
~~~

## Simple idea

Use modular positions and track the element count.

## Java solution

~~~java
static final class CircularQueue {
    private final int[] data; private int head, size;
    CircularQueue(int capacity) { data = new int[capacity]; }
    boolean offer(int value) {
        if (size == data.length) return false;
        data[(head + size) % data.length] = value; size++; return true;
    }
    int poll() {
        if (size == 0) throw new NoSuchElementException();
        int value = data[head]; head = (head + 1) % data.length; size--; return value;
    }
}
~~~

## Complexity

- Time: `O(1) per operation`
- Extra space: `O(capacity)`

Try to write the solution yourself before reading the code.

