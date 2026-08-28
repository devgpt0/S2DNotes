# 79. Group by String Length

**What you learn:** Java stream questions APIs and problem solving.

## Problem

Group words by their length.

## Example

~~~text
Input: words=[a,to,cat]
Output: {1=[a],2=[to],3=[cat]}
~~~

## Simple idea

Use String::length as the grouping classifier.

## Java solution

~~~java
static Map<Integer, List<String>> byLength(List<String> words) {
    return words.stream().collect(Collectors.groupingBy(
        String::length, TreeMap::new, Collectors.toList()));
}
~~~

## Complexity

- Time: `O(n log n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

