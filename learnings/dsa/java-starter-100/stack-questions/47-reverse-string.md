# 47. Reverse a String with a Stack

**What you learn:** Java stack questions APIs and problem solving.

## Problem

Reverse a string by pushing characters and popping them.

## Example

~~~text
Input: text = "abc"
Output: cba
~~~

## Simple idea

The last character pushed is the first returned.

## Java solution

~~~java
static String reverse(String text) {
    Deque<Character> stack = new ArrayDeque<>();
    for (char c : text.toCharArray()) stack.push(c);
    StringBuilder result = new StringBuilder();
    while (!stack.isEmpty()) result.append(stack.pop());
    return result.toString();
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

