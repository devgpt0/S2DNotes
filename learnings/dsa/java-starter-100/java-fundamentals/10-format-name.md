# 10. Format a Name

**What you learn:** Java java fundamentals APIs and problem solving.

## Problem

Trim a name and capitalize its first character.

## Example

~~~text
Input: name = "  aLICE "
Output: Alice
~~~

## Simple idea

Normalize case, then combine the first character with the remaining substring.

## Java solution

~~~java
static String formatName(String name) {
    String clean = name.trim().toLowerCase(Locale.ROOT);
    if (clean.isEmpty()) return clean;
    return Character.toUpperCase(clean.charAt(0)) + clean.substring(1);
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

