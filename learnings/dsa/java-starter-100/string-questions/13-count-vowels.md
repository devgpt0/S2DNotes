# 13. Count Vowels in a String

**What you learn:** Java string questions APIs and problem solving.

## Problem

Count a, e, i, o, and u, ignoring case.

## Example

~~~text
Input: text = "Education"
Output: 5
~~~

## Simple idea

Lowercase each character and count the five vowel cases.

## Java solution

~~~java
static int countVowels(String text) {
    int count = 0;
    for (char c : text.toLowerCase(Locale.ROOT).toCharArray())
        if ("aeiou".indexOf(c) >= 0) count++;
    return count;
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

