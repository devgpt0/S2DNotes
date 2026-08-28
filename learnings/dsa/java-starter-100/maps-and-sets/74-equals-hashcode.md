# 74. Make a Value Object

**What you learn:** Java maps and sets APIs and problem solving.

## Problem

Make equal IDs compare equal when placed in a HashSet.

## Example

~~~text
Input: students=[id 7,id 7]
Output: set size = 1
~~~

## Simple idea

Hash collections require equal objects to have equal hash codes.

## Java solution

~~~java
record Student(int id, String name) {}
static int distinctStudents(Student first, Student second) {
    Set<Student> students = new HashSet<>();
    students.add(first); students.add(second);
    return students.size();
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

