# Control Flow Worksheet Answers

## Level 1

1.
```text
B
```

2.
```text
0 1 2 4
```
`continue` skips the print when `i` is `3`.

3.
```text
0
1
2
```
The loop breaks after incrementing `i` to `3`.

4.
```text
Done
```
`pass` does nothing.

5.
```text
Yes
```
`and` has higher precedence than `or`, so the condition is `True or (False and False)`.

6.
```text
0 even
1 odd
2 even
3 odd
4 even
5 odd
6 even
7 odd
8 even
9 odd
```

7.
```text
2
4
8
10
```
`continue` skips the print when `x` is `6`.

8.
```text
10
```
The assignment expression assigns `10`, a truthy value, to `num`.

9.
```text
0 0
1 1
2 2
```
Each inner loop breaks when `i == j`.

10.
```text
10
```
For each `i`, the inner loop counts values before `j == i`: `0 + 1 + 2 + 3 + 4`.

## Level 2

1.
```text
[1, 2, 3, 10, 20, 30, 100]
```
The loop sees appended items; it stops when the list length exceeds six. Mutating an iterated list is poor practice.

2.
```text
4 3 1 0 Loop ended normally
```
The `continue` skips `2`, and `while ... else` runs because there is no `break`.

3. The result depends on the entered integer. For `11`:
```text
11 is greater than 10
```
For `10`:
```text
10 is not greater than 10
```

4.
```text
1 9
2 8
3 7
4 6
5 5
```
The loop ends when both values become `5`.

5.
```text
True
```
The condition is `(x > 3 and y < 15) or x == 0`.

6.
```text
1
2
Fizz
4
Buzz
Fizz
7
8
Fizz
```

7.
```text
0
1
2
```
The loop breaks at `3`, so its `else` clause does not run.

8.
```text
B
```
The first condition is false; `x and not y` is true.

9.
```text
[3, 4, 9, 8, 15]
```
Odd values are tripled and even values are doubled.

10.
```text
1
3
```
Even values are skipped, and the loop breaks before printing `5`.

## Level 3

1.
```text
0
Finally 0
Finally 1
ValueError
```
The `finally` block runs before the uncaught `ValueError` propagates.

2.
```text
0
1
2
3
4
```
At `5`, the exception is caught and breaks the loop; `finally` still increments `x`.

3.
```text
0 0 | 0 1 | 0 2 | 0 3 | 1 0 | 1 1 | 1 2 | 1 3 | 2 0 | 2 1 | 2 2 | 2 3 | 3 0 | 3 1 | 3 2 |
```
The inner `break` for `i == 3, j == 3` prevents its `else`, then the outer `break` ends the loop.

4.
```text
1
2
3
4
5
```
The final assignment to `n` is `6`, which ends the condition without printing it.

5.
```text
30
```

6.
```text
Server Error
```
The guarded wildcard case matches codes of at least `500`.

7.
```text
0
2
4
```
The loop breaks when the generator produces `6`.

8.
```text
1
2
4
5
While loop completed
```
The loop completes normally, so its `else` clause runs.

9.
```text
Outer 1
  Inner 1
  Inner 2
  Inner 4
  Inner 5
Outer 2
  Inner 1
  Inner 2
  Inner 4
  Inner 5
Outer 3
  Inner 1
  Inner 2
Outer 4
  Inner 1
  Inner 2
Outer 5
  Inner 1
  Inner 2
```
`j == 3` is skipped; `break` exits only the inner loop when the product exceeds `10`.

10.
```text
B
```
At least one value is truthy, but not all values are truthy.

## Code Quality

1. The loop is a counted loop, so use `range`:
```python
for i in range(101):
    print(i)
```

2. The original grade ladder is already clear. Keep it as a single `if`/`elif`/`else` chain and assign directly:
```python
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"
```

3. Use an early guard to avoid nesting and prevent division by zero:
```python
if x == 0:
    raise ValueError("x cannot be zero")
if y / x > 10:
    print("High")
```

4. There is no need to test every pair. Derive `j` from `i`:
```python
for i in range(8):
    print(i, 7 - i)
```

5. Prefer `for` when the iteration source or count is known, such as `for item in items`. Prefer `while` when progress depends on a changing condition, such as reading input until an empty line is received.
