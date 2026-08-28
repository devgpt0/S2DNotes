# 14. Count Words in a String

**What you learn:** Java string questions APIs and problem solving.

## Problem

Count non-empty whitespace-separated words.

## Example

~~~text
Input: text = " Java   is fun "
Output: 3
~~~

## Simple idea

Trim first; an empty string has zero words.

## Java solution

~~~java
static int wordCount(String text) {
    String clean = text.trim();
    return clean.isEmpty() ? 0 : clean.split("\\s+").length;
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

