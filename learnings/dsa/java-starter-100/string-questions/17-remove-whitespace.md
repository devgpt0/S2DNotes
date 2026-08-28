# 17. Remove Whitespace

**What you learn:** Java string questions APIs and problem solving.

## Problem

Return a string with every whitespace character removed.

## Example

~~~text
Input: text = " a b\tc "
Output: abc
~~~

## Simple idea

The regular expression \s+ matches each whitespace run.

## Java solution

~~~java
static String withoutWhitespace(String text) {
    return text.replaceAll("\\s+", "");
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

