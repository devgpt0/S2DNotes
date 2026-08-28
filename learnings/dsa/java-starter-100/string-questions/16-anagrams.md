# 16. Check Anagrams

**What you learn:** Java string questions APIs and problem solving.

## Problem

Return whether two strings contain the same letters, ignoring case and spaces.

## Example

~~~text
Input: first = "listen", second = "silent"
Output: true
~~~

## Simple idea

Normalize both strings and compare their character-frequency maps.

## Java solution

~~~java
static boolean anagrams(String first, String second) {
    return counts(first).equals(counts(second));
}
static Map<Character, Integer> counts(String text) {
    Map<Character, Integer> result = new HashMap<>();
    for (char c : text.toLowerCase(Locale.ROOT).toCharArray())
        if (!Character.isWhitespace(c)) result.merge(c, 1, Integer::sum);
    return result;
}
~~~

## Complexity

- Time: `O(n + m)`
- Extra space: `O(k)`

Try to write the solution yourself before reading the code.

