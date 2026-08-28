# 52. Remove Adjacent Duplicates

**What you learn:** Java stack questions APIs and problem solving.

## Problem

Repeatedly remove equal neighboring characters.

## Example

~~~text
Input: text = "abbaca"
Output: ca
~~~

## Simple idea

The stack stores the result so equal neighbors cancel immediately.

## Java solution

~~~java
static String removeAdjacentDuplicates(String text) {
    Deque<Character> stack = new ArrayDeque<>();
    for (char c : text.toCharArray())
        if (!stack.isEmpty() && stack.peek() == c) stack.pop(); else stack.push(c);
    StringBuilder result = new StringBuilder();
    while (!stack.isEmpty()) result.append(stack.removeLast());
    return result.toString();
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

