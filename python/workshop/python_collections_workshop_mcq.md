# Python Collections Workshop: 200 MCQs

Focus topics:
- `list`
- `tuple`
- `dict`
- `set`

## Code-Based MCQs (1-120)

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

## Conceptual MCQs (121-200)

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

### Q51
```python
a = [1, 2, 3]
a[1:3] = [9]
print(a)
```
A. `[1, 9]`  
B. `[1, 9, 3]`  
C. `[1, 2, 9]`  
D. `Error`

### Q52
```python
a = [1, 2, 3]
a[1:2] = [7, 8, 9]
print(a)
```
A. `[1, 7, 8, 9, 3]`  
B. `[1, 7, 8, 9]`  
C. `[1, 2, 3, 7, 8, 9]`  
D. `Error`

### Q53
```python
a = [10, 20, 30]
del a[1]
print(a)
```
A. `[10, 20]`  
B. `[10, 30]`  
C. `[20, 30]`  
D. `Error`

### Q54
```python
a = [0, 1, 2, 3, 4]
del a[1:4]
print(a)
```
A. `[0, 4]`  
B. `[1, 2, 3]`  
C. `[0, 1, 4]`  
D. `Error`

### Q55
```python
x = [1, 2]
print(x * 3)
```
A. `[1, 2, 1, 2, 1, 2]`  
B. `[[1, 2], [1, 2], [1, 2]]`  
C. `[3, 6]`  
D. `Error`

### Q56
```python
x = [1, 2]
y = [3]
print(x + y)
```
A. `[1, 2, 3]`  
B. `[1, 2, [3]]`  
C. `[[1, 2], [3]]`  
D. `Error`

### Q57
```python
x = [1, 2]
print(x + 3)
```
A. `[1, 2, 3]`  
B. `[4, 5]`  
C. `TypeError`  
D. `None`

### Q58
```python
a = [3, 1, 2]
print(sorted(a), a)
```
A. `[1, 2, 3] [3, 1, 2]`  
B. `[3, 1, 2] [1, 2, 3]`  
C. `[1, 2, 3] [1, 2, 3]`  
D. `Error`

### Q59
```python
a = [3, 1, 2]
a.reverse()
print(a)
```
A. `[1, 2, 3]`  
B. `[2, 1, 3]`  
C. `[2, 3, 1]`  
D. `[2, 1, 3]`

### Q60
```python
a = [3, 1, 2]
print(list(reversed(a)), a)
```
A. `[2, 1, 3] [3, 1, 2]`  
B. `[3, 1, 2] [2, 1, 3]`  
C. `[1, 2, 3] [3, 1, 2]`  
D. `Error`

### Q61
```python
a = [1, 2, 2, 3]
print(a.count(2), a.index(2))
```
A. `2 1`  
B. `2 2`  
C. `1 2`  
D. `Error`

### Q62
```python
a = [5, 6, 7, 6]
print(a.index(6, 2))
```
A. `1`  
B. `2`  
C. `3`  
D. `Error`

### Q63
```python
a = [1, 2, 3]
a.clear()
print(a)
```
A. `[1, 2, 3]`  
B. `[]`  
C. `None`  
D. `Error`

### Q64
```python
a = []
a.pop()
```
A. `[]`  
B. `None`  
C. `IndexError`  
D. `ValueError`

### Q65
```python
a = [1, 2, 3]
print(4 in a, 2 not in a)
```
A. `True False`  
B. `False True`  
C. `False False`  
D. `True True`

### Q66
```python
a = [10, 20, 30]
for i, v in enumerate(a):
    if i == 1:
        print(i, v)
```
A. `1 20`  
B. `0 10`  
C. `2 30`  
D. No output

### Q67
```python
m = [[0]] * 3
m[0].append(1)
print(m)
```
A. `[[0, 1], [0], [0]]`  
B. `[[0, 1], [0, 1], [0, 1]]`  
C. `[[1], [1], [1]]`  
D. `Error`

### Q68
```python
m = [[0] for _ in range(3)]
m[0].append(1)
print(m)
```
A. `[[0, 1], [0], [0]]`  
B. `[[0, 1], [0, 1], [0, 1]]`  
C. `[[1], [0], [0]]`  
D. `Error`

### Q69
```python
nums = [1, 2, 3, 4]
out = [x * 2 for x in nums if x % 2 == 0]
print(out)
```
A. `[2, 4, 6, 8]`  
B. `[4, 8]`  
C. `[1, 3]`  
D. `Error`

### Q70
```python
pairs = [(1, 10), (2, 20)]
out = [a + b for a, b in pairs]
print(out)
```
A. `[11, 22]`  
B. `[1, 10, 2, 20]`  
C. `[(11), (22)]`  
D. `Error`

### Q71
```python
t = (1, 2, 3)
print(t[0], t[-1])
```
A. `1 3`  
B. `3 1`  
C. `0 2`  
D. `Error`

### Q72
```python
t = (1, 2, 3, 4)
print(t[1:3])
```
A. `(1, 2, 3)`  
B. `(2, 3)`  
C. `[2, 3]`  
D. `Error`

### Q73
```python
t = (1, 2, 3)
print(t[::-1])
```
A. `(3, 2, 1)`  
B. `[3, 2, 1]`  
C. `(1, 2, 3)`  
D. `Error`

### Q74
```python
a = (1, 2)
b = (3, 4)
print(a + b)
```
A. `(1, 2, 3, 4)`  
B. `((1, 2), (3, 4))`  
C. `[1, 2, 3, 4]`  
D. `Error`

### Q75
```python
t = (5,)
print(t * 3)
```
A. `(5, 5, 5)`  
B. `[5, 5, 5]`  
C. `(15,)`  
D. `Error`

### Q76
```python
t = (1, 2, 2, 3)
print(t.count(2), t.index(2))
```
A. `2 1`  
B. `1 2`  
C. `2 2`  
D. `Error`

### Q77
```python
t = (1, [2, 3])
t[1].append(4)
print(t)
```
A. `(1, [2, 3])`  
B. `(1, [2, 3, 4])`  
C. `(1, (2, 3, 4))`  
D. `Error`

### Q78
```python
t = (1, 2, 3)
a, b, c = t
print(a + b + c)
```
A. `6`  
B. `123`  
C. `(1, 2, 3)`  
D. `Error`

### Q79
```python
t = (10, 20, 30, 40)
a, *mid, z = t
print(mid)
```
A. `(20, 30)`  
B. `[20, 30]`  
C. `[10, 20, 30]`  
D. `Error`

### Q80
```python
a = [1, 2]
t = tuple(a)
a.append(3)
print(t, a)
```
A. `(1, 2, 3) [1, 2, 3]`  
B. `(1, 2) [1, 2, 3]`  
C. `(1, 2) [1, 2]`  
D. `Error`

### Q81
```python
d = dict([("a", 1), ("b", 2)])
print(d)
```
A. `{'a': 1, 'b': 2}`  
B. `{('a', 1), ('b', 2)}`  
C. `{'a': ('a', 1), 'b': ('b', 2)}`  
D. `Error`

### Q82
```python
d = dict(a=1, b=2)
print(d)
```
A. `{'a': 1, 'b': 2}`  
B. `{'a=1', 'b=2'}`  
C. `[('a', 1), ('b', 2)]`  
D. `Error`

### Q83
```python
d = {"k": 1}
d["k"] = 9
print(d)
```
A. `{'k': 1, 'k': 9}`  
B. `{'k': 9}`  
C. `{'k': [1, 9]}`  
D. `Error`

### Q84
```python
d = {"a": 1}
print(d["b"])
```
A. `None`  
B. `KeyError`  
C. `0`  
D. `False`

### Q85
```python
d = {"a": 1}
print(d.get("b"), d)
```
A. `None {'a': 1}`  
B. `KeyError {'a': 1}`  
C. `0 {'a': 1}`  
D. `None {'a': 1, 'b': None}`

### Q86
```python
d = {"x": 1}
print(d.setdefault("x", 5), d)
```
A. `5 {'x': 5}`  
B. `1 {'x': 1}`  
C. `1 {'x': 1, 'x': 5}`  
D. `Error`

### Q87
```python
d = {"x": 1}
print(d.setdefault("y", 5), d)
```
A. `None {'x': 1}`  
B. `5 {'x': 1, 'y': 5}`  
C. `5 {'x': 1}`  
D. `Error`

### Q88
```python
d = {"a": 1, "b": 2}
print(d.pop("a"), d)
```
A. `1 {'b': 2}`  
B. `2 {'a': 1}`  
C. `1 {'a': 1, 'b': 2}`  
D. `Error`

### Q89
```python
d = {"a": 1}
print(d.pop("b", 99), d)
```
A. `KeyError {'a': 1}`  
B. `99 {'a': 1}`  
C. `None {'a': 1}`  
D. `99 {'a': 1, 'b': 99}`

### Q90
```python
d = {"p": 1, "q": 2}
item = d.popitem()
print(item, d)
```
A. `('p', 1) {'q': 2}`  
B. `('q', 2) {'p': 1}`  
C. `('p', 1) {'p': 1, 'q': 2}`  
D. `Error`

### Q91
```python
d = {"a": 1}
view = d.items()
d["b"] = 2
print(list(view))
```
A. `[("a", 1)]`  
B. `[("a", 1), ("b", 2)]`  
C. `["a", "b"]`  
D. `Error`

### Q92
```python
d = {"a": 1, "b": 2}
print("a" in d, 2 in d)
```
A. `True True`  
B. `True False`  
C. `False True`  
D. `False False`

### Q93
```python
d = {k: k * 10 for k in range(4) if k % 2 == 1}
print(d)
```
A. `{1: 10, 3: 30}`  
B. `{0: 0, 1: 10, 2: 20, 3: 30}`  
C. `{0: 0, 2: 20}`  
D. `Error`

### Q94
```python
d = dict.fromkeys(["x", "y"], [])
d["x"].append(1)
print(d)
```
A. `{'x': [1], 'y': []}`  
B. `{'x': [1], 'y': [1]}`  
C. `{'x': 1, 'y': 1}`  
D. `Error`

### Q95
```python
d = {"a": 1, "b": 2}
for k, v in d.items():
    if k == "b":
        print(v)
```
A. `1`  
B. `2`  
C. `a`  
D. No output

### Q96
```python
s = set([1, 2, 2, 3])
print(s)
```
A. `{1, 2, 3}`  
B. `{1, 2, 2, 3}`  
C. `[1, 2, 3]`  
D. `Error`

### Q97
```python
s = {}
print(type(s).__name__)
```
A. `set`  
B. `dict`  
C. `list`  
D. `tuple`

### Q98
```python
s = set()
s.add(5)
print(s)
```
A. `{5}`  
B. `[5]`  
C. `(5,)`  
D. `Error`

### Q99
```python
s = {1, 2}
s.update([2, 3, 4])
print(sorted(s))
```
A. `[1, 2, 2, 3, 4]`  
B. `[1, 2, 3, 4]`  
C. `[2, 3, 4]`  
D. `Error`

### Q100
```python
s = {1, 2, 3}
s.remove(4)
```
A. `{1, 2, 3}`  
B. `None`  
C. `KeyError`  
D. `ValueError`

### Q101
```python
s = {1, 2, 3}
s.discard(4)
print(s)
```
A. `{1, 2}`  
B. `{1, 2, 3}`  
C. `KeyError`  
D. `None`

### Q102
```python
s = {10, 20}
x = s.pop()
print(x in {10, 20}, len(s))
```
A. `True 1`  
B. `False 1`  
C. `True 2`  
D. `Error`

### Q103
```python
s = {1, 2, 3}
print(2 in s, 5 not in s)
```
A. `True True`  
B. `True False`  
C. `False True`  
D. `False False`

### Q104
```python
a = {1, 2, 3}
b = {3, 4}
print(a | b)
```
A. `{1, 2, 3, 4}`  
B. `{3}`  
C. `{1, 2}`  
D. `Error`

### Q105
```python
a = {1, 2, 3}
b = {3, 4}
print(a & b)
```
A. `{1, 2, 3, 4}`  
B. `{3}`  
C. `{1, 2}`  
D. `Error`

### Q106
```python
a = {1, 2, 3}
b = {3, 4}
print(a - b)
```
A. `{3}`  
B. `{1, 2}`  
C. `{4}`  
D. `Error`

### Q107
```python
a = {1, 2, 3}
b = {3, 4}
print(a ^ b)
```
A. `{1, 2, 4}`  
B. `{3}`  
C. `{1, 2, 3, 4}`  
D. `Error`

### Q108
```python
a = {1, 2}
b = {1, 2, 3}
print(a.issubset(b), b.issuperset(a))
```
A. `True True`  
B. `True False`  
C. `False True`  
D. `False False`

### Q109
```python
a = {1, 2}
b = {3, 4}
print(a.isdisjoint(b))
```
A. `False`  
B. `True`  
C. `None`  
D. `Error`

### Q110
```python
s = frozenset([1, 2, 2])
print(s)
```
A. `frozenset({1, 2})`  
B. `{1, 2}`  
C. `[1, 2]`  
D. `Error`

### Q111
```python
d = {frozenset({"a", "b"}): 10}
print(d[frozenset({"b", "a"})])
```
A. `KeyError`  
B. `10`  
C. `None`  
D. `{'a', 'b'}`

### Q112
```python
s = {1, 2, 3}
t = s.copy()
t.add(4)
print(s, t)
```
A. `{1, 2, 3, 4} {1, 2, 3, 4}`  
B. `{1, 2, 3} {1, 2, 3, 4}`  
C. `{1, 2, 3, 4} {1, 2, 3}`  
D. `Error`

### Q113
```python
nums = [1, 2, 2, 3, 1]
print(list(dict.fromkeys(nums)))
```
A. `[1, 2, 3]`  
B. `[1, 2, 2, 3, 1]`  
C. `[3, 2, 1]`  
D. `Error`

### Q114
```python
a = [3, 1, 2, 1]
print(sorted(set(a)))
```
A. `[1, 1, 2, 3]`  
B. `[1, 2, 3]`  
C. `{1, 2, 3}`  
D. `Error`

### Q115
```python
names = ["Ada", "bob", "CHARLIE"]
names.sort(key=str.lower)
print(names)
```
A. `['CHARLIE', 'Ada', 'bob']`  
B. `['Ada', 'bob', 'CHARLIE']`  
C. `['bob', 'Ada', 'CHARLIE']`  
D. `Error`

### Q116
```python
words = ["aa", "b", "cccc"]
out = sorted(words, key=len, reverse=True)
print(out)
```
A. `['b', 'aa', 'cccc']`  
B. `['cccc', 'aa', 'b']`  
C. `['aa', 'b', 'cccc']`  
D. `Error`

### Q117
```python
nums = [1, -3, 2, -10]
nums.sort(key=abs)
print(nums)
```
A. `[1, 2, -3, -10]`  
B. `[-10, -3, 2, 1]`  
C. `[1, -3, 2, -10]`  
D. `Error`

### Q118
```python
a = [1, 2, 3]
print(min(a), max(a), sum(a), len(a))
```
A. `1 3 6 3`  
B. `0 3 6 4`  
C. `1 2 6 3`  
D. `Error`

### Q119
```python
names = ["Alice", "Bob", "Charlie"]
print(max(names))
```
A. `Alice`  
B. `Bob`  
C. `Charlie`  
D. `Error`

### Q120
```python
a = [10, 20, 30]
print(a[10:20])
```
A. `IndexError`  
B. `[]`  
C. `[30]`  
D. `None`

### Q121
```python
a = [10, 20, 30]
print(a[5])
```
A. `None`  
B. `[]`  
C. `IndexError`  
D. `0`

### Q122
```python
d = {"a": 1, "b": 2}
print(list(d.values()))
```
A. `['a', 'b']`  
B. `[1, 2]`  
C. `[('a', 1), ('b', 2)]`  
D. `Error`

### Q123
```python
d = {"a": 1, "b": 2}
print(list(d.items()))
```
A. `['a', 'b']`  
B. `[1, 2]`  
C. `[('a', 1), ('b', 2)]`  
D. `Error`

### Q124
```python
x = [1, 2, 3]
y = x.copy()
y.append(4)
print(x, y)
```
A. `[1, 2, 3, 4] [1, 2, 3, 4]`  
B. `[1, 2, 3] [1, 2, 3, 4]`  
C. `[1, 2, 3, 4] [1, 2, 3]`  
D. `Error`

### Q125
```python
x = [[1], [2]]
y = x.copy()
y[0].append(9)
print(x)
```
A. `[[1], [2]]`  
B. `[[1, 9], [2]]`  
C. `[[9], [2]]`  
D. `Error`

### Q126
```python
import copy
x = [[1], [2]]
y = copy.deepcopy(x)
y[0].append(9)
print(x, y)
```
A. `[[1, 9], [2]] [[1, 9], [2]]`  
B. `[[1], [2]] [[1, 9], [2]]`  
C. `[[1], [2]] [[1], [2]]`  
D. `Error`

### Q127
```python
a = set("banana")
print(a)
```
A. `{'b', 'a', 'n'}`  
B. `{'banana'}`  
C. `['b', 'a', 'n']`  
D. `Error`

### Q128
```python
s = {1, 2}
s.clear()
print(s)
```
A. `{}`  
B. `set()`  
C. `None`  
D. `Error`

### Q129
```python
a = {1, 2, 3}
a &= {2, 3, 4}
print(a)
```
A. `{1, 2, 3, 4}`  
B. `{2, 3}`  
C. `{1}`  
D. `Error`

### Q130
```python
a = {1, 2}
a |= {2, 3}
print(a)
```
A. `{1, 2, 3}`  
B. `{2, 3}`  
C. `{1, 2}`  
D. `Error`

### Q131
```python
a = {1, 2, 3}
a -= {2}
print(a)
```
A. `{1, 3}`  
B. `{2}`  
C. `{1, 2, 3}`  
D. `Error`

### Q132
```python
a = {1, 2, 3}
a ^= {3, 4}
print(a)
```
A. `{3}`  
B. `{1, 2, 4}`  
C. `{1, 2, 3, 4}`  
D. `Error`

### Q133
```python
s = {1, 2, 3}
print(sorted(s, reverse=True))
```
A. `[1, 2, 3]`  
B. `[3, 2, 1]`  
C. `{3, 2, 1}`  
D. `Error`

### Q134
```python
a = [1, 2, 3]
print(tuple(reversed(a)))
```
A. `(3, 2, 1)`  
B. `[3, 2, 1]`  
C. `(1, 2, 3)`  
D. `Error`

### Q135
```python
d = {"a": 1}
d.update({"b": 2}, c=3)
print(d)
```
A. `{'a': 1, 'b': 2, 'c': 3}`  
B. `{'a': 1, 'b': 2}`  
C. `{'a': 1, 'c': 3}`  
D. `Error`

### Q136
```python
keys = ["x", "y"]
print(dict.fromkeys(keys, 0))
```
A. `{'x': 0, 'y': 0}`  
B. `{'x': None, 'y': None}`  
C. `{0: 'x', 0: 'y'}`  
D. `Error`

### Q137
```python
d = {"a": 1, "b": 2}
for k in d:
    if k == "a":
        print(k)
```
A. `1`  
B. `a`  
C. `('a', 1)`  
D. No output

### Q138
```python
s = {1, 2, 3}
print(any(x > 2 for x in s), all(x > 0 for x in s))
```
A. `True True`  
B. `True False`  
C. `False True`  
D. `False False`

### Q139
```python
a = ["ab", "cd"]
print("".join(a))
```
A. `ab cd`  
B. `['ab', 'cd']`  
C. `abcd`  
D. `Error`

### Q140
```python
a = [1, 2, 3, 4]
print(a[3:0:-1])
```
A. `[4, 3, 2]`  
B. `[4, 3, 2, 1]`  
C. `[3, 2, 1]`  
D. `[]`

### Q141
Which statement about list slicing is correct?
A. End index is included in slice results  
B. Out-of-range slicing always raises IndexError  
C. Slice assignment can change list length  
D. Negative step is not allowed

### Q142
What is the best description of `append` on a list?
A. Adds all elements from iterable one by one  
B. Adds one object as a single element at end  
C. Returns a new list with item added  
D. Works only for numeric values

### Q143
Which method adds each element from an iterable into a list?
A. `insert`  
B. `append`  
C. `extend`  
D. `count`

### Q144
What does `remove(x)` do on a list?
A. Removes all matching occurrences of `x`  
B. Removes first matching occurrence of `x`  
C. Removes by index position `x`  
D. Removes last element and returns it

### Q145
Which operation on an empty list raises `IndexError`?
A. `clear()`  
B. `count(1)`  
C. `pop()`  
D. `append(1)`

### Q146
What is true about `list.copy()`?
A. It creates a deep copy of all nested objects  
B. It creates an alias to same list object  
C. It creates a shallow copy  
D. It sorts the list before copying

### Q147
Which is true for `a = b` with lists?
A. Creates independent copy of list  
B. Creates alias to same object  
C. Converts to tuple automatically  
D. Raises TypeError

### Q148
Which statement about list membership (`x in a_list`) is correct?
A. Average complexity is O(1) due to hashing  
B. It performs linear search in typical list  
C. It requires sorted input list  
D. It checks indices, not values

### Q149
Which construct is most suitable for map+filter in one expression for lists?
A. Generator stop statement  
B. List comprehension with condition  
C. Exception handling block  
D. `del` expression

### Q150
Which list method returns the first index of a value?
A. `find`  
B. `locate`  
C. `index`  
D. `position`

### Q151
What is the key immutability rule for tuples?
A. Tuple length can be changed, values cannot  
B. Tuple items can be reassigned by index  
C. Tuple object structure cannot be modified  
D. Tuple can store only numbers

### Q152
Which syntax is required for a one-element tuple?
A. `(5)`  
B. `[5]`  
C. `(5,)`  
D. `{5}`

### Q153
Which statement about tuple unpacking is correct?
A. Number of targets must match values unless starred target used  
B. Unpacking works only for lists  
C. Starred target must be at end only  
D. Unpacking always returns tuple values as strings

### Q154
What does `tuple(iterable)` do?
A. Mutates iterable into tuple in place  
B. Creates a new tuple from iterable items  
C. Returns same iterable object always  
D. Requires iterable to be list only

### Q155
Why can a tuple containing a list still appear to �change�?
A. Tuple auto-converts nested lists to tuples  
B. Nested mutable object can mutate independently  
C. Python silently rebuilds tuple object  
D. Tuples are mutable after Python 3.10

### Q156
Which tuple operation is valid?
A. `t[0] = 9`  
B. `t.append(9)`  
C. `t + (9,)`  
D. `t.remove(1)`

### Q157
What is true about dictionary keys?
A. Keys must be hashable  
B. Keys must always be strings  
C. Keys may be mutable lists  
D. Duplicate keys are stored separately

### Q158
How does `d.get(key, default)` behave when key is missing?
A. Inserts key with default into dict  
B. Returns default without modifying dict  
C. Raises KeyError  
D. Returns tuple of key and default

### Q159
What does `setdefault` do when key is absent?
A. Deletes key if default is None  
B. Returns None and does nothing  
C. Inserts key with default and returns value  
D. Raises ValueError

### Q160
Which statement about dict insertion order (Python 3.7+) is correct?
A. Dict is always sorted by keys  
B. Insertion order is preserved by language spec  
C. Order is random every access  
D. Only OrderedDict preserves insertion order

### Q161
What does `popitem()` remove in modern Python dictionaries?
A. Random key-value pair  
B. First inserted key-value pair only  
C. Last inserted key-value pair  
D. Pair with minimum key

### Q162
Which statement about dictionary views is true?
A. `keys()` returns static snapshot list  
B. `items()` never reflects later updates  
C. Views are dynamic and reflect changes  
D. Views support item assignment by index

### Q163
In `key in d` for a dict, membership checks:
A. values only  
B. keys only  
C. key-value tuples only  
D. values and keys simultaneously

### Q164
Why is `dict.fromkeys(keys, [])` a common pitfall?
A. It deep-copies list per key  
B. It refuses mutable defaults  
C. All keys share one list object  
D. It stores keys as tuples

### Q165
Which statement about sets is correct?
A. Sets preserve insertion index access like lists  
B. Sets allow duplicates by default  
C. Sets store unique hashable elements  
D. Sets are key-value mappings

### Q166
How do you create an empty set?
A. `{}`  
B. `set()`  
C. `[]`  
D. `()`

### Q167
Which set method does NOT raise error if element is missing?
A. `remove`  
B. `discard`  
C. `pop`  
D. `clear`

### Q168
What does `a | b` represent for sets?
A. Intersection  
B. Difference  
C. Union  
D. Symmetric difference

### Q169
What does `a & b` represent for sets?
A. Elements in both sets  
B. Elements only in `a`  
C. Elements only in `b`  
D. Elements in either but not both

### Q170
What does `a ^ b` represent for sets?
A. Union of all elements  
B. Common elements only  
C. Elements in exactly one set  
D. Empty set always

### Q171
Which statement about set order is safest for production logic?
A. Set order is stable and indexable  
B. Set order should not be relied on  
C. Set order is always sorted ascending  
D. Set order equals insertion order contract

### Q172
What is true about `frozenset`?
A. Mutable and unhashable  
B. Immutable and hashable  
C. Ordered and indexable  
D. Same as list with unique values

### Q173
Which container is most suitable for frequent membership checks with uniqueness?
A. `set`  
B. `list`  
C. `tuple`  
D. `str`

### Q174
Which expression preserves order while removing duplicates from a list?
A. `list(set(seq))`  
B. `sorted(set(seq))`  
C. `list(dict.fromkeys(seq))`  
D. `tuple(set(seq))`

### Q175
Which statement about direct indexing is correct?
A. Bad index on list returns None  
B. Bad index on tuple returns empty tuple  
C. Bad index access raises IndexError  
D. Bad index auto-expands sequence

### Q176
What does `sorted(iterable)` return?
A. Sorts in place and returns None  
B. Returns new sorted list  
C. Returns tuple of sorted values  
D. Works only on lists

### Q177
What does `list.sort()` return?
A. New sorted list  
B. Original unsorted list  
C. `None` after in-place sort  
D. Tuple of sorted elements

### Q178
Why use `enumerate(seq)` in loops?
A. It mutates sequence while iterating  
B. It yields `(index, element)` pairs  
C. It sorts sequence automatically  
D. It removes duplicates

### Q179
Which is true about `reversed(seq)`?
A. It mutates sequence immediately  
B. It returns reverse iterator  
C. It works only for tuples  
D. It returns set

### Q180
Which operation is invalid for sets?
A. `s.add(1)`  
B. `s.update([2, 3])`  
C. `s[0]`  
D. `s.copy()`

### Q181
Which is a correct dict comprehension form?
A. `{k: v for (k, v) in pairs}`  
B. `[k: v for (k, v) in pairs]`  
C. `(k: v for (k, v) in pairs)`  
D. `{k, v for (k, v) in pairs}`

### Q182
Which set comprehension syntax is valid?
A. `{x for x in data if x > 0}`  
B. `[x for x in data if x > 0]`  
C. `(x for x in data if x > 0)`  
D. `{x: x for x in data}`

### Q183
What happens with duplicate keys in dict literal?
A. SyntaxError  
B. First value wins  
C. Last value overwrites earlier value  
D. Values merge into list

### Q184
Which statement about hashability is correct?
A. Lists are hashable by default  
B. Dicts are hashable by default  
C. Tuples are hashable if elements are hashable  
D. Sets are hashable

### Q185
Which is safest when key may be absent but no insertion desired?
A. `d[key]`  
B. `d.get(key)`  
C. `d.setdefault(key)`  
D. `d.pop(key)`

### Q186
Which method removes all items from a dict?
A. `erase()`  
B. `remove_all()`  
C. `clear()`  
D. `flush()`

### Q187
Which operation can shrink or grow a list in one statement?
A. Integer addition  
B. Slice assignment  
C. Membership check  
D. `len()`

### Q188
What is true about sequence slicing with out-of-range bounds?
A. Always raises IndexError  
B. Returns valid truncated result without error  
C. Returns None  
D. Converts to set

### Q189
Which operation is appropriate to remove one arbitrary element from a set and get it?
A. `discard()`  
B. `remove()`  
C. `pop()`  
D. `delete()`

### Q190
Which is true for `a.copy()` on built-in list/dict/set?
A. Deep copies nested mutables  
B. Creates shallow copy  
C. Returns alias  
D. Unsupported on these types

### Q191
Which type is best for fixed, read-only coordinate-like data?
A. `tuple`  
B. `dict`  
C. `set`  
D. `list`

### Q192
Which container best models key-value configuration settings?
A. `list`  
B. `tuple`  
C. `dict`  
D. `set`

### Q193
Which container best models unique tags with fast lookup?
A. `list`  
B. `set`  
C. `tuple`  
D. `str`

### Q194
Which statement about `values()` view is true?
A. It is always hashable  
B. It supports numeric indexing directly  
C. It reflects dictionary mutations dynamically  
D. It is immutable snapshot tuple

### Q195
When should you prefer `discard` over `remove` on sets?
A. When missing element should raise error  
B. When missing element should be ignored  
C. When adding new elements  
D. When sorting set elements

### Q196
Which built-in converts an iterable of pairs to dict?
A. `set()`  
B. `dict()`  
C. `tuple()`  
D. `list()`

### Q197
What is true about `list(set(seq))` for de-duplication?
A. Preserves original order always  
B. Removes duplicates but order may change  
C. Keeps duplicates and sorts  
D. Raises TypeError for strings

### Q198
Which operation is best to reverse a list in place?
A. `reversed(lst)`  
B. `lst[::-1]`  
C. `lst.reverse()`  
D. `sorted(lst, reverse=True)`

### Q199
Which expression checks whether `a` and `b` sets share no common elements?
A. `a.issubset(b)`  
B. `a.isdisjoint(b)`  
C. `a.issuperset(b)`  
D. `a.symmetric_difference(b)`

### Q200
Which statement about `{}` in Python is correct?
A. It creates empty set  
B. It creates empty tuple  
C. It creates empty dict  
D. It is invalid syntax

---

## Extended Answer Key (1-200)

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
51. A  
52. A  
53. B  
54. A  
55. A  
56. A  
57. C  
58. A  
59. C  
60. A  
61. A  
62. C  
63. B  
64. C  
65. B  
66. A  
67. B  
68. A  
69. B  
70. A  
71. A  
72. B  
73. A  
74. A  
75. A  
76. A  
77. B  
78. A  
79. B  
80. B  
81. A  
82. A  
83. B  
84. B  
85. A  
86. B  
87. B  
88. A  
89. B  
90. B  
91. B  
92. B  
93. A  
94. B  
95. B  
96. A  
97. B  
98. A  
99. B  
100. C  
101. B  
102. A  
103. A  
104. A  
105. B  
106. B  
107. A  
108. A  
109. B  
110. A  
111. B  
112. B  
113. A  
114. B  
115. B  
116. B  
117. A  
118. A  
119. C  
120. B  
121. C  
122. B  
123. C  
124. B  
125. B  
126. B  
127. A  
128. B  
129. B  
130. A  
131. A  
132. B  
133. B  
134. A  
135. A  
136. A  
137. B  
138. A  
139. C  
140. A  
141. C  
142. B  
143. C  
144. B  
145. C  
146. C  
147. B  
148. B  
149. B  
150. C  
151. C  
152. C  
153. A  
154. B  
155. B  
156. C  
157. A  
158. B  
159. C  
160. B  
161. C  
162. C  
163. B  
164. C  
165. C  
166. B  
167. B  
168. C  
169. A  
170. C  
171. B  
172. B  
173. A  
174. C  
175. C  
176. B  
177. C  
178. B  
179. B  
180. C  
181. A  
182. A  
183. C  
184. C  
185. B  
186. C  
187. B  
188. B  
189. C  
190. B  
191. A  
192. C  
193. B  
194. C  
195. B  
196. B  
197. B  
198. C  
199. B  
200. C
