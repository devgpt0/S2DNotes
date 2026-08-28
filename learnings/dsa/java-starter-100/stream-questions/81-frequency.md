# 81. Count Frequencies with Streams

**What you learn:** Java stream questions APIs and problem solving.

## Problem

Return a map of each word and its frequency.

## Example

~~~text
Input: words=[java,code,java]
Output: {java=2,code=1}
~~~

## Simple idea

Use groupingBy with the counting downstream collector.

## Java solution

~~~java
static Map<String, Long> frequencies(List<String> words) {
    return words.stream().collect(Collectors.groupingBy(
        Function.identity(), Collectors.counting()));
}
~~~

## Complexity

- Time: `O(n) average`
- Extra space: `O(k)`

Try to write the solution yourself before reading the code.

