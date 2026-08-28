# 48. Check Balanced Brackets

**What you learn:** Java stack questions APIs and problem solving.

## Problem

Return whether (), [], and {} are correctly nested.

## Example

~~~text
Input: text = "{[()]}"
Output: true
~~~

## Simple idea

Push openings; each closing bracket must match the latest opening.

## Java solution

~~~java
static boolean balanced(String text) {
    Deque<Character> stack = new ArrayDeque<>();
    Map<Character, Character> pairs = Map.of(')', '(', ']', '[', '}', '{');
    for (char c : text.toCharArray()) {
        if (pairs.containsValue(c)) stack.push(c);
        else if (pairs.containsKey(c) && (stack.isEmpty() || stack.pop() != pairs.get(c)))
            return false;
    }
    return stack.isEmpty();
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

