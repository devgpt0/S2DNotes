# 19. Find the Longest Word

**What you learn:** Java string questions APIs and problem solving.

## Problem

Return the longest whitespace-separated word; keep the first on ties.

## Example

~~~text
Input: text = "write clean Java code"
Output: clean
~~~

## Simple idea

Replace the best only when a strictly longer word appears.

## Java solution

~~~java
static String longestWord(String text) {
    String best = "";
    for (String word : text.trim().split("\\s+"))
        if (word.length() > best.length()) best = word;
    return best;
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

