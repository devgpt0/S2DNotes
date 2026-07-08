# Python Collections Workshop: 50 MCQs

Focus topics:
- `list`
- `tuple`
- `dict`
- `set`

## Code-Based MCQs (1-30)

### Q1
```python
a = [10, 20]
b = a
b.append(30)
print(a)
```
A. `[10, 20]`  
B. `[10, 20, 30]`  
C. `[30, 20, 10]`  
D. `Error`

### Q2
```python
a = [1, 2, 3]
b = a[:]
b[0] = 99
print(a, b)
```
A. `[99, 2, 3] [99, 2, 3]`  
B. `[1, 2, 3] [99, 2, 3]`  
C. `[1, 2, 3] [1, 2, 3]`  
D. `[99, 2, 3] [1, 2, 3]`

### Q3
```python
x = [1, 2]
x.append([3, 4])
print(x)
```
A. `[1, 2, 3, 4]`  
B. `[1, 2, [3, 4]]`  
C. `[[1, 2], [3, 4]]`  
D. `[3, 4, 1, 2]`

### Q4
```python
x = [1, 2]
x.extend([3, 4])
print(x)
```
A. `[1, 2, [3, 4]]`  
B. `[1, 2, 3, 4]`  
C. `[3, 4, 1, 2]`  
D. `Error`

### Q5
```python
nums = [0, 1, 2, 3, 4, 5]
print(nums[1:5:2])
```
A. `[1, 3]`  
B. `[1, 2, 3, 4]`  
C. `[0, 2, 4]`  
D. `[5, 3, 1]`

### Q6
```python
arr = [3, 1, 2]
res = arr.sort()
print(arr, res)
```
A. `[3, 1, 2] [1, 2, 3]`  
B. `[1, 2, 3] None`  
C. `[1, 2, 3] [1, 2, 3]`  
D. `None [1, 2, 3]`

### Q7
```python
vals = [1, 2, 3, 4]
print(vals[::-1])
```
A. `[1, 2, 3, 4]`  
B. `[4, 3, 2, 1]`  
C. `[2, 4]`  
D. `[3, 2, 1]`

### Q8
```python
t = (1, 2)
u = t + (3,)
print(t, u)
```
A. `(1, 2, 3) (1, 2, 3)`  
B. `(1, 2) (1, 2, 3)`  
C. `(1, 2) (3,)`  
D. `(3,) (1, 2)`

### Q9
```python
a = (5)
b = (5,)
print(type(a).__name__, type(b).__name__)
```
A. `tuple tuple`  
B. `int tuple`  
C. `int int`  
D. `tuple int`

### Q10
```python
t = (10, 20, 30, 40)
a, *mid, b = t
print(a, mid, b)
```
A. `10 [20, 30] 40`  
B. `10 (20, 30) 40`  
C. `10 [20, 30, 40] 40`  
D. `Error`

### Q11
```python
d = {"x": 1, "y": 2, "x": 9}
print(d)
```
A. `{'x': 1, 'y': 2}`  
B. `{'x': 9, 'y': 2}`  
C. `{'x': 1, 'y': 2, 'x': 9}`  
D. `Error`

### Q12
```python
d = {"a": 10}
print(d.get("b", 99), d)
```
A. `99 {'a': 10}`  
B. `None {'a': 10, 'b': 99}`  
C. `99 {'a': 10, 'b': 99}`  
D. `KeyError {'a': 10}`

### Q13
```python
d = {"a": 1}
v1 = d.setdefault("a", 100)
v2 = d.setdefault("b", 200)
print(v1, v2, d)
```
A. `100 200 {'a': 100, 'b': 200}`  
B. `1 200 {'a': 1, 'b': 200}`  
C. `1 200 {'a': 1}`  
D. `1 100 {'a': 1, 'b': 100}`

### Q14
```python
d = {"p": 1, "q": 2}
d.update({"q": 9, "r": 3})
removed = d.pop("p")
print(removed, d)
```
A. `1 {'q': 9, 'r': 3}`  
B. `1 {'p': 1, 'q': 9, 'r': 3}`  
C. `9 {'q': 2, 'r': 3}`  
D. `Error`

### Q15
```python
d = {"a": 1, "b": 2, "c": 3}
print(list(d.keys()))
```
A. `['c', 'b', 'a']`  
B. `['a', 'b', 'c']`  
C. `[1, 2, 3]`  
D. `dict_keys(['a', 'b', 'c'])`

### Q16
```python
d = {k: k * k for k in range(5) if k % 2 == 0}
print(d)
```
A. `{0: 0, 2: 4, 4: 16}`  
B. `{1: 1, 3: 9}`  
C. `{0: 0, 1: 1, 2: 4, 3: 9, 4: 16}`  
D. `{0, 2, 4}`

### Q17
```python
s = {1, 2, 2, 3}
print(len(s), sorted(s))
```
A. `4 [1, 2, 2, 3]`  
B. `3 [1, 2, 3]`  
C. `3 [3, 2, 1]`  
D. `2 [1, 3]`

### Q18
```python
a = {1, 2, 3}
b = {3, 4}
print(sorted(a | b), sorted(a & b), sorted(a - b))
```
A. `[1, 2, 3, 4] [3] [1, 2]`  
B. `[1, 2, 3] [3, 4] [4]`  
C. `[1, 2, 3, 4] [1, 2, 3] [4]`  
D. `[3, 4] [1, 2] [3]`

### Q19
```python
s = {1}
s.update([2, 3])
print(sorted(s))
```
A. `[1, [2, 3]]`  
B. `[1, 2, 3]`  
C. `[2, 3]`  
D. `Error`

### Q20
```python
a = [3, 1, 2, 1, 3]
print(sorted(set(a)))
```
A. `[3, 1, 2, 1, 3]`  
B. `[1, 2, 3]`  
C. `{1, 2, 3}`  
D. `[1, 1, 2, 3, 3]`

### Q21
```python
t = ([1, 2], "x")
t[0].append(3)
print(t)
```
A. `([1, 2], 'x')`  
B. `([1, 2, 3], 'x')`  
C. `([3], 'x')`  
D. `Error`

### Q22
```python
try:
    t = (1, 2, 3)
    t[0] = 9
except TypeError:
    print("immutable")
```
A. `TypeError` traceback  
B. `immutable`  
C. `None`  
D. No output

### Q23
```python
d = {"a": 1}
kv = d.keys()
d["b"] = 2
print(list(kv))
```
A. `['a']`  
B. `['a', 'b']`  
C. `['b']`  
D. `Error`

### Q24
```python
x = [[1], [2]]
y = list(x)
y[1].append(99)
print(x)
```
A. `[[1], [2]]`  
B. `[[1], [2, 99]]`  
C. `[[1, 99], [2]]`  
D. `[[1, 99], [2, 99]]`

### Q25
```python
s = {1, 2}
s.discard(9)
try:
    s.remove(9)
except KeyError:
    print("K")
print(len(s))
```
A. `2` only  
B. `K` then `2`  
C. `K` then `3`  
D. `KeyError` and stop

### Q26
```python
d = dict.fromkeys(["a", "b"], [])
d["a"].append(1)
print(d)
```
A. `{'a': [1], 'b': []}`  
B. `{'a': [1], 'b': [1]}`  
C. `{'a': 1, 'b': 1}`  
D. `Error`

### Q27
```python
m = [[0]] * 3
m[0].append(1)
print(m)
```
A. `[[0, 1], [0], [0]]`  
B. `[[0, 1], [0, 1], [0, 1]]`  
C. `[[1], [1], [1]]`  
D. `[[0], [0], [0, 1]]`

### Q28
```python
pairs = [("a", 1), ("b", 2)]
d = {k: v for k, v in pairs}
print(d)
```
A. `{'a': 1, 'b': 2}`  
B. `{'a': ('a', 1), 'b': ('b', 2)}`  
C. `{('a', 1), ('b', 2)}`  
D. `Error`

### Q29
```python
keys = ["x", "y", "z"]
vals = [10, 20]
print(dict(zip(keys, vals)))
```
A. `{'x': 10, 'y': 20, 'z': None}`  
B. `{'x': 10, 'y': 20}`  
C. `{'x': 10, 'y': 20, 'z': 20}`  
D. `Error`

### Q30
```python
words = ["pear", "a", "banana", "kiwi"]
print(sorted(words, key=len))
```
A. `['banana', 'pear', 'kiwi', 'a']`  
B. `['a', 'pear', 'kiwi', 'banana']`  
C. `['a', 'kiwi', 'pear', 'banana']`  
D. `['pear', 'a', 'banana', 'kiwi']`

## Conceptual MCQs (31-50)

### Q31
Which statement about Python lists is correct?
A. Lists are immutable sequences  
B. Lists preserve insertion order and are mutable  
C. Lists require all elements to be same type  
D. Lists do not support slicing

### Q32
Primary use case of `tuple` over `list` is:
A. Frequent element updates in place  
B. Fixed-size immutable records  
C. Faster key-value mapping than dict  
D. Automatic duplicate removal

### Q33
Which object is hashable by default (usable as dict key if contents hashable)?
A. `list`  
B. `set`  
C. `tuple`  
D. `dict`

### Q34
Which statement about dictionaries is true in modern Python (3.7+ language spec)?
A. Keys are always sorted alphabetically  
B. Insertion order of keys is preserved  
C. Duplicate keys are stored as separate entries  
D. Only string keys are allowed

### Q35
What happens when the same key appears multiple times in a dict literal?
A. First value wins permanently  
B. Last value for that key overwrites earlier value  
C. Python raises `ValueError`  
D. Key becomes a list of all values

### Q36
Best description of a set:
A. Ordered collection with index-based access  
B. Mapping of key-value pairs  
C. Unordered collection of unique elements  
D. Immutable sequence of values

### Q37
Time-complexity intuition for average membership checks (`in`) is best for:
A. `list`  
B. `tuple`  
C. `set`  
D. All identical in practice

### Q38
Which expression creates a shallow copy of list `a`?
A. `b = a`  
B. `b = a[:]`  
C. `b = tuple(a)`  
D. `b = set(a)`

### Q39
Why is `dict.fromkeys(keys, [])` often risky?
A. It deep-copies the empty list for each key  
B. All keys share the same mutable list object  
C. It cannot accept iterable keys  
D. It creates tuple keys unexpectedly

### Q40
What does `setdefault` do?
A. Removes key if missing  
B. Returns key name when present  
C. Gets value; inserts default only if key absent  
D. Sorts dictionary by key

### Q41
Which statement is correct about tuple immutability?
A. Tuple and all nested objects are always immutable  
B. Tuple items can be reassigned by index  
C. Tuple is immutable, but nested mutable elements may still mutate  
D. Tuple can never contain mutable objects

### Q42
Difference between `append` and `extend` on lists:
A. Both always flatten nested iterables  
B. `append` adds one object; `extend` adds elements from iterable  
C. `extend` works only with lists, not tuples  
D. `append` returns new list, `extend` mutates old list

### Q43
`popitem()` on dict in modern Python removes:
A. Random item always  
B. Smallest key item  
C. Last inserted key-value pair (LIFO behavior)  
D. First inserted item always in all Python versions

### Q44
Which operation is valid for sets?
A. Indexing like `s[0]`  
B. Slicing like `s[1:3]`  
C. Intersection using `&`  
D. Duplicate-preserving concatenation

### Q45
When converting list to set and back to list, what is true?
A. Original order is guaranteed preserved  
B. Duplicates are removed, order may change  
C. Only numeric elements are kept  
D. Conversion fails for strings

### Q46
Which statement about dictionary views (`keys()`, `values()`, `items()`) is correct?
A. They are static snapshots disconnected from dict changes  
B. They are dynamic views reflecting dict updates  
C. They are writable sequences  
D. They are always lists internally

### Q47
Best way to safely read possibly missing key without exception:
A. `d[key]` always  
B. `d.get(key, default)`  
C. `d.remove(key)`  
D. `d.append(key)`

### Q48
Why is `[[0]] * 3` a common pitfall?
A. It creates three independent inner lists  
B. It creates three aliases to the same inner list  
C. It is slower but always safe  
D. It automatically deep-copies nested values

### Q49
Which collection type is designed for key-value association?
A. `dict`  
B. `tuple`  
C. `set`  
D. `list`

### Q50
If you need uniqueness + fast membership + set algebra, choose:
A. `tuple`  
B. `dict`  
C. `set`  
D. `list`

---

## Answer Key
1. B  
2. B  
3. B  
4. B  
5. A  
6. B  
7. B  
8. B  
9. B  
10. A  
11. B  
12. A  
13. B  
14. A  
15. B  
16. A  
17. B  
18. A  
19. B  
20. B  
21. B  
22. B  
23. B  
24. B  
25. B  
26. B  
27. B  
28. A  
29. B  
30. B  
31. B  
32. B  
33. C  
34. B  
35. B  
36. C  
37. C  
38. B  
39. B  
40. C  
41. C  
42. B  
43. C  
44. C  
45. B  
46. B  
47. B  
48. B  
49. A  
50. C
