# 12. Check a String Palindrome

**What you learn:** Java string questions APIs and problem solving.

## Problem

Return whether text reads the same from both ends, ignoring case.

## Example

~~~text
Input: text = "Level"
Output: true
~~~

## Simple idea

Compare symmetric characters after converting to one case.

## Java solution

~~~java
static boolean isPalindrome(String text) {
    String clean = text.toLowerCase(Locale.ROOT);
    for (int left = 0, right = clean.length() - 1; left < right; left++, right--)
        if (clean.charAt(left) != clean.charAt(right)) return false;
    return true;
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

