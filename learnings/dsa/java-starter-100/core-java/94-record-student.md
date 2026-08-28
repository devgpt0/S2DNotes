# 94. Model Data with a Record

**What you learn:** Java core java APIs and problem solving.

## Problem

Create an immutable student value with id and name.

## Example

~~~text
Input: new Student(7, Ada)
Output: Student[id=7, name=Ada]
~~~

## Simple idea

A record supplies accessors, equality, hashCode, and toString.

## Java solution

~~~java
record Student(int id, String name) {}
static String describe(Student student) { return student.toString(); }
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

