# 53. Convert Decimal to Binary

**What you learn:** Java stack questions APIs and problem solving.

## Problem

Return the binary representation of a non-negative integer.

## Example

~~~text
Input: number = 13
Output: 1101
~~~

## Simple idea

Push least-significant remainders, then pop them in reverse order.

## Java solution

~~~java
static String toBinary(int number) {
    if (number == 0) return "0";
    Deque<Integer> stack = new ArrayDeque<>();
    while (number > 0) { stack.push(number % 2); number /= 2; }
    StringBuilder result = new StringBuilder();
    while (!stack.isEmpty()) result.append(stack.pop());
    return result.toString();
}
~~~

## Complexity

- Time: `O(log n)`
- Extra space: `O(log n)`

Try to write the solution yourself before reading the code.

