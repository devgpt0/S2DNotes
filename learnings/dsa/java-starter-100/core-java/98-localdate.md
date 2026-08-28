# 98. Calculate Days Between Dates

**What you learn:** Java core java APIs and problem solving.

## Problem

Return days between two ISO dates.

## Example

~~~text
Input: start=2026-01-01, end=2026-01-10
Output: 9
~~~

## Simple idea

Use java.time instead of manually counting milliseconds.

## Java solution

~~~java
static long daysBetween(String start, String end) {
    return ChronoUnit.DAYS.between(LocalDate.parse(start), LocalDate.parse(end));
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

