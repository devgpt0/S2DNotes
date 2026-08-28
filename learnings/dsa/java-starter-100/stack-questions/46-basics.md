# 46. Use a Stack with Deque

**What you learn:** Java stack questions APIs and problem solving.

## Problem

Push 10 and 20, then return the top without removing it.

## Example

~~~text
Input: push(10), push(20), peek()
Output: 20
~~~

## Simple idea

Prefer Deque with ArrayDeque over legacy Stack for ordinary DSA.

## Java solution

~~~java
static int topAfterPushes() {
    Deque<Integer> stack = new ArrayDeque<>();
    stack.push(10); stack.push(20);
    return stack.peek();
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

