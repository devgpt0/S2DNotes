# 92. Use an Enum in a Switch

**What you learn:** Java core java APIs and problem solving.

## Problem

Return the days in a month for a non-leap year.

## Example

~~~text
Input: month=APRIL
Output: 30
~~~

## Simple idea

A switch expression returns a value and makes enum cases explicit.

## Java solution

~~~java
enum Month { JANUARY, FEBRUARY, MARCH, APRIL, MAY, JUNE,
    JULY, AUGUST, SEPTEMBER, OCTOBER, NOVEMBER, DECEMBER }
static int days(Month month) {
    return switch (month) {
        case APRIL, JUNE, SEPTEMBER, NOVEMBER -> 30;
        case FEBRUARY -> 28;
        default -> 31;
    };
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

