# 11. Reverse a String

**What you learn:** Java string questions APIs and problem solving.

## Problem

Return the characters of a string in reverse order.

## Example

~~~text
Input: text = "hello"
Output: olleh
~~~

## Simple idea

String is immutable, so StringBuilder is the natural mutable helper.

## Java solution

~~~java
static String reverse(String text) {
    return new StringBuilder(text).reverse().toString();
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

