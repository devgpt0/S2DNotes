# 96. Sort Objects with Comparators

**What you learn:** Java core java APIs and problem solving.

## Problem

Sort results by score descending, then name ascending.

## Example

~~~text
Input: [Ada:90, Lin:90, Bo:80]
Output: [Ada:90, Lin:90, Bo:80]
~~~

## Simple idea

Compose comparator rules rather than nesting conditionals.

## Java solution

~~~java
record Result(String name, int score) {}
static void sortResults(List<Result> results) {
    results.sort(Comparator.comparingInt(Result::score).reversed()
        .thenComparing(Result::name));
}
~~~

## Complexity

- Time: `O(n log n)`
- Extra space: `O(log n) typical stack space`

Try to write the solution yourself before reading the code.

