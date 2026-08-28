# 09. Parse an Integer Safely

**What you learn:** Java java fundamentals APIs and problem solving.

## Problem

Return an OptionalInt for valid whole-number text, or empty for invalid text.

## Example

~~~text
Input: text = "2048"
Output: OptionalInt[2048]
~~~

## Simple idea

Use Integer.parseInt and catch NumberFormatException.

## Java solution

~~~java
static OptionalInt parseInteger(String text) {
    try {
        return OptionalInt.of(Integer.parseInt(text.trim()));
    } catch (NumberFormatException error) {
        return OptionalInt.empty();
    }
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

