# 49. Build a Minimum Stack

**What you learn:** Java stack questions APIs and problem solving.

## Problem

Support push, pop, and min in constant time.

## Example

~~~text
Input: push(3), push(1), min()
Output: 1
~~~

## Simple idea

Store the current minimum beside every pushed value.

## Java solution

~~~java
static final class MinStack {
    private final Deque<Integer> values = new ArrayDeque<>();
    private final Deque<Integer> minimums = new ArrayDeque<>();
    void push(int value) {
        values.push(value);
        minimums.push(minimums.isEmpty() ? value : Math.min(value, minimums.peek()));
    }
    int pop() { minimums.pop(); return values.pop(); }
    int min() { return minimums.peek(); }
}
~~~

## Complexity

- Time: `O(1) per operation`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

