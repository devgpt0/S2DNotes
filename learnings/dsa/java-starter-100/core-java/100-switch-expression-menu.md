# 100. Build a Small Command Menu

**What you learn:** Java core java APIs and problem solving.

## Problem

Return a response for add, list, quit, or unknown commands.

## Example

~~~text
Input: command=list
Output: Showing items
~~~

## Simple idea

A switch expression maps each command directly to one result.

## Java solution

~~~java
static String response(String command) {
    return switch (command) {
        case "add" -> "Added item";
        case "list" -> "Showing items";
        case "quit" -> "Goodbye";
        default -> "Unknown";
    };
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

