# 88. Use a Static Field

**What you learn:** Java core java APIs and problem solving.

## Problem

Count how many Ticket objects have been created.

## Example

~~~text
Input: new Ticket(), new Ticket()
Output: 2
~~~

## Simple idea

A static field belongs to the class and is shared by instances.

## Java solution

~~~java
static final class Ticket {
    private static int created;
    Ticket() { created++; }
    static int createdCount() { return created; }
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

