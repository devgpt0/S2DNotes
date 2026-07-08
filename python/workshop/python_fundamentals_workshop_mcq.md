# Python Fundamentals Workshop: 50 MCQs

Based on:
- `python/notes/python_fundamentals/Datatypes.md`
- `python/notes/python_fundamentals/variables model.md`
- `python/notes/python_fundamentals/control_flow.md`

## Code-Based MCQs (1-30)

### Q1
```python
a = [1, 2]
b = a
b.append(3)
print(a)
```
A. `[1, 2]`  
B. `[1, 2, 3]`  
C. `[3, 2, 1]`  
D. `Error`

### Q2
```python
a = [1, 2]
b = a
b = b + [3]
print(a, b)
```
A. `[1, 2, 3] [1, 2, 3]`  
B. `[1, 2] [1, 2]`  
C. `[1, 2] [1, 2, 3]`  
D. `[1, 2, 3] [1, 2]`

### Q3
```python
x = 10
y = x
y += 1
print(x, y)
```
A. `11 11`  
B. `10 10`  
C. `10 11`  
D. `11 10`

### Q4
```python
def modify(lst):
    lst.append(10)

a = [1, 2]
modify(a)
print(a)
```
A. `[1, 2]`  
B. `[1, 2, 10]`  
C. `[10, 1, 2]`  
D. `None`

### Q5
```python
def rebind(lst):
    lst = [999]

a = [1, 2]
rebind(a)
print(a)
```
A. `[999]`  
B. `[1, 2]`  
C. `[]`  
D. `Error`

### Q6
```python
a = [1, 2]
b = a
c = [1, 2]
print(a is b, a == c, a is c)
```
A. `False True True`  
B. `True True False`  
C. `True False False`  
D. `False False True`

### Q7
```python
x = [[1], [2]]
y = x[:]
y[0].append(99)
print(x)
```
A. `[[1], [2]]`  
B. `[[1, 99], [2]]`  
C. `[[99], [2]]`  
D. `[[1], [2, 99]]`

### Q8
```python
import copy
x = [[1], [2]]
y = copy.deepcopy(x)
y[0].append(99)
print(x, y)
```
A. `[[1, 99], [2]] [[1, 99], [2]]`  
B. `[[1], [2]] [[1, 99], [2]]`  
C. `[[1], [2, 99]] [[1], [2]]`  
D. `[[1, 99], [2]] [[1], [2]]`

### Q9
```python
def f(x=[]):
    x.append(1)
    return x

print(f())
print(f())
```
A. `[1]` then `[1]`  
B. `[1]` then `[1, 1]`  
C. `[1, 1]` then `[1]`  
D. `Error on second call`

### Q10
```python
funcs = []
for i in range(3):
    funcs.append(lambda: i)
print([fn() for fn in funcs])
```
A. `[0, 1, 2]`  
B. `[2, 2, 2]`  
C. `[0, 0, 0]`  
D. `[1, 2, 3]`

### Q11
```python
a = 0
result = a != 0 and (10 / a)
print(result)
```
A. `0`  
B. `False`  
C. `ZeroDivisionError`  
D. `None`

### Q12
```python
a, b = False, True
print(a or b and not a)
```
A. `False`  
B. `True`  
C. `0`  
D. `Error`

### Q13
```python
for n in [2, 4, 5, 8]:
    if n % 2 != 0:
        print("odd")
        break
else:
    print("all even")
```
A. `all even`  
B. `odd`  
C. `odd` then `all even`  
D. No output

### Q14
```python
for n in [2, 4, 6]:
    if n == 4:
        continue
else:
    print("done")
```
A. `done`  
B. No output  
C. `4`  
D. `Error`

### Q15
```python
i = 0
while i < 5:
    i += 1
    if i == 3:
        continue
    if i == 4:
        break
print(i)
```
A. `2`  
B. `3`  
C. `4`  
D. `5`

### Q16
```python
for _ in range(2):
    pass
print("end")
```
A. `pass`  
B. `end`  
C. No output  
D. `Error`

### Q17
```python
for i in range(2):
    for j in range(3):
        if j == 1:
            break
        print(i, j)
```
A. `0 0` `0 1` `1 0` `1 1`  
B. `0 0` `1 0`  
C. `0 1` `1 1`  
D. No output

### Q18
```python
stop = False
for i in range(3):
    for j in range(3):
        if i + j > 2:
            stop = True
            break
    if stop:
        break
print(i, j)
```
A. `0 0`  
B. `1 2`  
C. `2 1`  
D. `2 2`

### Q19
```python
for x in [1, 0, 2]:
    try:
        print(10 // x)
    except ZeroDivisionError:
        print("E")
    finally:
        print("F")
```
A. `10 F E F 5 F`  
B. `10 E 5 F`  
C. `10 F 0 F 5 F`  
D. `10 F E 5 F`

### Q20
```python
count = 0
while count < 3:
    try:
        if count == 1:
            break
        print(count)
    finally:
        count += 1
print("done", count)
```
A. `0` then `done 1`  
B. `0` then `done 2`  
C. `0 1` then `done 2`  
D. `done 3`

### Q21
```python
value = ("point", 2, 3)
match value:
    case ("point", x, y) if x == y:
        print("diag")
    case ("point", x, y):
        print("cart", x + y)
    case _:
        print("other")
```
A. `diag`  
B. `cart 5`  
C. `other`  
D. `Error`

### Q22
```python
nums = [0, 1, 2]
print(any(nums), all(nums))
```
A. `True True`  
B. `False False`  
C. `True False`  
D. `False True`

### Q23
```python
data = [3, 5, 7]
if (n := len(data)) > 2:
    print(n)
```
A. `2`  
B. `3`  
C. `True`  
D. No output

### Q24
```python
arr = [1, 2, 3, 4]
for x in arr:
    if x % 2 == 0:
        arr.remove(x)
print(arr)
```
A. `[1, 3]`  
B. `[2, 4]`  
C. `[1, 2, 3, 4]`  
D. `[1, 2, 4]`

### Q25
```python
a = [1, 2]
b = a
a += [3]
print(a is b, a)
```
A. `False [1, 2, 3]`  
B. `True [1, 2, 3]`  
C. `True [1, 2]`  
D. `False [1, 2]`

### Q26
```python
x = (1, 2)
y = x
x += (3,)
print(x is y, x, y)
```
A. `True (1, 2, 3) (1, 2, 3)`  
B. `False (1, 2, 3) (1, 2)`  
C. `True (1, 2) (1, 2)`  
D. `False (1, 2) (1, 2, 3)`

### Q27
```python
def side():
    print("side")
    return True

print(True or side())
```
A. `side` then `True`  
B. `True` only  
C. `False` only  
D. `side` then `False`

### Q28
```python
def g():
    try:
        return "try"
    finally:
        return "finally"

print(g())
```
A. `try`  
B. `finally`  
C. `None`  
D. `Error`

### Q29
```python
cmd = "stop"
match cmd:
    case "start":
        print(1)
    case "pause":
        print(2)
    case _:
        print(3)
```
A. `1`  
B. `2`  
C. `3`  
D. No output

### Q30
```python
i = 0
while i < 3:
    i += 1
    if i == 2:
        break
else:
    print("loop-else")
print(i)
```
A. `loop-else` then `2`  
B. `2` only  
C. `3` only  
D. `loop-else` then `3`

## Conceptual MCQs (31-50)

### Q31
In Python, a variable is best described as:
A. A fixed-size memory block storing raw bytes directly  
B. A label (name) bound to an object reference  
C. A primitive slot that always stores value-copy only  
D. A pointer syntax requiring explicit address operators

### Q32
What does assignment `b = a` do for objects?
A. Always deep-copies object graph  
B. Always shallow-copies top-level container  
C. Binds `b` to the same object as `a`  
D. Converts mutable objects into immutable snapshots

### Q33
Which set contains only mutable built-in types?
A. `list, dict, set`  
B. `int, str, tuple`  
C. `frozenset, tuple, bytes`  
D. `range, str, bytes`

### Q34
Python argument passing is most accurately called:
A. Pass-by-pointer arithmetic  
B. Pass-by-sharing (object reference is shared)  
C. Pass-by-copy-on-write only  
D. Pass-by-name macro expansion

### Q35
Choose the correct statement about `is` vs `==`.
A. `is` compares values, `==` compares identities  
B. Both always check memory identity  
C. `is` checks identity, `==` checks value equality  
D. Both are interchangeable for containers

### Q36
`arr2 = arr1[:]` on a list creates:
A. No copy, exact same list object  
B. A shallow copy (new outer list, shared inner references)  
C. A deep recursive copy of all levels  
D. An immutable view object

### Q37
Which statement about `copy.deepcopy` is true?
A. It duplicates only top-level references  
B. It shares all nested mutable children  
C. It recursively copies nested objects  
D. It works only for dictionaries

### Q38
What is the safest interview-level rule for interning/caching?
A. Assume all equal integers are same object everywhere  
B. Rely on string interning for business logic correctness  
C. Treat interning as optimization, not correctness rule  
D. Use `is` for numeric equality checks

### Q39
Why is `def f(x=[]):` often dangerous?
A. Default list is recreated on every function call  
B. Mutable default is evaluated once and reused  
C. Lists cannot be used as defaults in Python  
D. It forces parameter `x` to be tuple

### Q40
Late binding in closures means:
A. Captured variables are frozen at function definition value  
B. Captured names are resolved when inner function executes  
C. Closures store only primitive values  
D. Closure variables bypass LEGB rules

### Q41
For frequent membership testing (`item in ?`) at scale, best default choice is:
A. `list` with append-only usage  
B. `set` for near O(1) membership checks  
C. `tuple` for mutability speed  
D. `str` for hash table lookups

### Q42
Which structure is primarily optimized for key lookup by mapping?
A. `dict`  
B. `set`  
C. `list`  
D. `tuple`

### Q43
When is `tuple` commonly preferred over `list`?
A. When frequent in-place mutation is needed  
B. When immutable, fixed records are required  
C. When random deletion speed is critical  
D. When key-value mapping is required

### Q44
Which pattern avoids hidden O(n²) behavior while building a list?
A. Repeated `arr = arr + [i]` in loop  
B. Repeated `arr.append(i)` in loop  
C. Repeated `arr = sorted(arr)` in loop  
D. Repeated `arr = arr[::-1]` in loop

### Q45
Which copy-cost statement is correct?
A. Shallow copy of size `n` container is typically O(1)  
B. Shallow copy is typically O(n), deep copy is O(total nested elements)  
C. Deep copy is always O(1) with references  
D. Copy complexity is always identical regardless of depth

### Q46
Boolean operator precedence in Python is:
A. `or > and > not`  
B. `and > or > not`  
C. `not > and > or`  
D. `not > or > and`

### Q47
Which statement is correct?
A. `break` exits nearest loop; `continue` skips to next iteration; `pass` does nothing  
B. `pass` exits loop immediately; `break` skips one iteration  
C. `continue` terminates all nested loops automatically  
D. `break` and `pass` are synonyms

### Q48
A loop `else` block executes when:
A. Loop completes normally without `break`  
B. Loop hits `continue` at least once  
C. Loop raises any exception  
D. Loop body never runs due to false condition only

### Q49
Which statement about `try/except/finally` is correct?
A. `finally` runs only when exception occurs  
B. `finally` is skipped on `break` and `continue`  
C. `finally` runs before leaving `try` block path  
D. `except` always runs even when no exception occurs

### Q50
In `match/case`, selection behavior is:
A. All matching cases execute in sequence  
B. Cases are checked bottom-up for specificity  
C. Cases are checked top-to-bottom; first match wins  
D. Guard conditions are ignored after pattern match

---

## Answer Key
1. B  
2. C  
3. C  
4. B  
5. B  
6. B  
7. B  
8. B  
9. B  
10. B  
11. B  
12. B  
13. B  
14. A  
15. C  
16. B  
17. B  
18. B  
19. A  
20. B  
21. B  
22. C  
23. B  
24. A  
25. B  
26. B  
27. B  
28. B  
29. C  
30. B  
31. B  
32. C  
33. A  
34. B  
35. C  
36. B  
37. C  
38. C  
39. B  
40. B  
41. B  
42. A  
43. B  
44. B  
45. B  
46. C  
47. A  
48. A  
49. C  
50. C
