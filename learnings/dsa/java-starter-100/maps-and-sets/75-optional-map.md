# 75. Transform an Optional Value

**What you learn:** Java maps and sets APIs and problem solving.

## Problem

Return an uppercase name or UNKNOWN when absent.

## Example

~~~text
Input: name=Optional[Ada]
Output: ADA
~~~

## Simple idea

Optional.map transforms only a present value.

## Java solution

~~~java
static String display(Optional<String> name) {
    return name.map(String::toUpperCase).orElse("UNKNOWN");
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

