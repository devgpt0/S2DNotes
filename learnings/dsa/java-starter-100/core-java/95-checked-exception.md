# 95. Handle a Checked Exception

**What you learn:** Java core java APIs and problem solving.

## Problem

Read the first line from a Path, returning empty text when reading fails.

## Example

~~~text
Input: path=missing.txt
Output: ""
~~~

## Simple idea

Files.lines declares IOException; handle it at the boundary.

## Java solution

~~~java
static String firstLine(Path path) {
    try (Stream<String> lines = Files.lines(path)) {
        return lines.findFirst().orElse("");
    } catch (IOException error) {
        return "";
    }
}
~~~

## Complexity

- Time: `O(n) until first line`
- Extra space: `O(1) extra`

Try to write the solution yourself before reading the code.

