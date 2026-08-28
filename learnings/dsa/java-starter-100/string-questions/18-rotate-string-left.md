# 18. Rotate a String Left

**What you learn:** Java string questions APIs and problem solving.

## Problem

Rotate text left by steps, even when steps is larger than its length.

## Example

~~~text
Input: text = "abcdef", steps = 2
Output: cdefab
~~~

## Simple idea

Reduce steps with modulo, then concatenate suffix and prefix.

## Java solution

~~~java
static String rotateLeft(String text, int steps) {
    if (text.isEmpty()) return text;
    int split = Math.floorMod(steps, text.length());
    return text.substring(split) + text.substring(0, split);
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

