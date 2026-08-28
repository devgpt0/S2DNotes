# 54. Implement One Text Undo

**What you learn:** Java stack questions APIs and problem solving.

## Problem

Support an append followed by undo.

## Example

~~~text
Input: append("a"), append("b"), undo()
Output: a
~~~

## Simple idea

Store the previous text snapshot on a history stack.

## Java solution

~~~java
static String undoOnce(String original, String addition) {
    Deque<String> history = new ArrayDeque<>();
    history.push(original);
    String current = original + addition;
    return history.pop();
}
~~~

## Complexity

- Time: `O(1) for this snapshot`
- Extra space: `O(n) snapshot space`

Try to write the solution yourself before reading the code.

