# 20. Find a Common Prefix

**What you learn:** Java string questions APIs and problem solving.

## Problem

Return the longest prefix shared by every string.

## Example

~~~text
Input: words = ["interview", "internet", "internal"]
Output: inte
~~~

## Simple idea

Shorten the first word until every other word starts with it.

## Java solution

~~~java
static String commonPrefix(String[] words) {
    if (words.length == 0) return "";
    String prefix = words[0];
    for (int i = 1; i < words.length; i++) {
        while (!words[i].startsWith(prefix)) {
            prefix = prefix.substring(0, prefix.length() - 1);
            if (prefix.isEmpty()) return "";
        }
    }
    return prefix;
}
~~~

## Complexity

- Time: `O(n * p)`
- Extra space: `O(p)`

Try to write the solution yourself before reading the code.

