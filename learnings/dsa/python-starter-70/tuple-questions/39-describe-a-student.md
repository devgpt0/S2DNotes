# 39. Describe a Student Record

**What you learn:** Tuple unpacking.

## Problem

A tuple contains `(name, age, city)`. Return a readable sentence.

## Example

```text
Input: student = ("Asha", 20, "Pune")
Output: "Asha is 20 and lives in Pune."
```

## Simple idea

Unpack the three tuple values into clearly named variables.

## Python solution

```python
def describe_student(student: tuple[str, int, str]) -> str:
    name, age, city = student
    return f"{name} is {age} and lives in {city}."
```

## Complexity

- Time: `O(1)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

