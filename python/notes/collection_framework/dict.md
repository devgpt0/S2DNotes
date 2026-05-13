# Python `dict` - Unified Notes

## 1) What is a dictionary?
A dictionary is a key-value mapping type.

Core properties:
- Mutable: you can add, update, and delete entries.
- Ordered: insertion order is preserved.
- Hash-table based: average-case lookup, insert, and delete are fast.

```python
student = {"name": "Ad", "age": 22}
print(type(student))
print(student)
```

Output:
```text
<class 'dict'>
{'name': 'Ad', 'age': 22}
```

## 2) Creating dictionaries

```python
# Empty
d1 = {}
d2 = dict()

# Literal
student = {
    "name": "Ad",
    "age": 22,
    "skills": ["Python", "ML"],
}

# Constructor
d3 = dict(name="Ad", age=22)

# From tuples
d4 = dict([("a", 1), ("b", 2)])

# Comprehension
squares = {x: x * x for x in range(5)}

print(d1)
print(d2)
print(student)
print(d3)
print(d4)
print(squares)
```

Output:
```text
{}
{}
{'name': 'Ad', 'age': 22, 'skills': ['Python', 'ML']}
{'name': 'Ad', 'age': 22}
{'a': 1, 'b': 2}
{0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
```

## 3) Accessing values

```python
d = {"name": "Ad", "age": 22}

print(d["name"])
print(d.get("age"))
print(d.get("city"))
print(d.get("city", "NA"))
```

Output:
```text
Ad
22
None
NA
```

Missing-key behavior:

```python
d = {"name": "Ad"}

try:
    print(d["city"])
except KeyError:
    print("KeyError")

print(d.get("city"))
```

Output:
```text
KeyError
None
```

## 4) Adding and updating

```python
d = {}
d["name"] = "Ad"
d["name"] = "AI Engineer"
d.update({"age": 22, "city": "Pune"})

print(d)
```

Output:
```text
{'name': 'AI Engineer', 'age': 22, 'city': 'Pune'}
```

Merging:

```python
d1 = {"a": 1, "x": 10}
d2 = {"b": 2, "x": 99}

print(d1 | d2)

d1 |= {"c": 3}
print(d1)
```

Output:
```text
{'a': 1, 'x': 99, 'b': 2}
{'a': 1, 'x': 10, 'c': 3}
```

## 5) Removing elements

```python
d = {"a": 1, "b": 2, "c": 3}

print(d.pop("a"))
print(d)

print(d.popitem())
print(d)

del d["b"]
print(d)

d.clear()
print(d)
```

Output:
```text
1
{'b': 2, 'c': 3}
('c', 3)
{'b': 2}
{}
{}
```

## 6) Common methods demo

```python
d = {"a": 1, "b": 2}

print(list(d.keys()))
print(list(d.values()))
print(list(d.items()))
print(d.get("z", 0))

d.setdefault("c", 3)
print(d)

d2 = d.copy()
print(d2)

print(dict.fromkeys(["x", "y"], 0))
```

Output:
```text
['a', 'b']
[1, 2]
[('a', 1), ('b', 2)]
0
{'a': 1, 'b': 2, 'c': 3}
{'a': 1, 'b': 2, 'c': 3}
{'x': 0, 'y': 0}
```

## 7) Iteration patterns

```python
d = {"a": 1, "b": 2}

for key in d:
    print("K", key)

for value in d.values():
    print("V", value)

for key, value in d.items():
    print("KV", key, value)
```

Output:
```text
K a
K b
V 1
V 2
KV a 1
KV b 2
```

## 8) Dictionary comprehension

```python
sq = {x: x * x for x in range(5)}
even_sq = {x: x * x for x in range(10) if x % 2 == 0}

d = {"a": 1, "b": 2}
rev = {v: k for k, v in d.items()}

print(sq)
print(even_sq)
print(rev)
```

Output:
```text
{0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
{0: 0, 2: 4, 4: 16, 6: 36, 8: 64}
{1: 'a', 2: 'b'}
```

## 9) Nested dictionaries

```python
students = {
    101: {"name": "Ad", "age": 22},
    102: {"name": "John", "age": 23},
}

print(students[101]["name"])
print(students[102]["age"])
```

Output:
```text
Ad
23
```

## 10) Shallow copy vs deep copy

Shallow copy:

```python
d1 = {"a": [1, 2]}
d2 = d1.copy()
d2["a"].append(3)

print(d1)
print(d2)
```

Output:
```text
{'a': [1, 2, 3]}
{'a': [1, 2, 3]}
```

Deep copy:

```python
import copy

d1 = {"a": [1, 2]}
d2 = copy.deepcopy(d1)
d2["a"].append(3)

print(d1)
print(d2)
```

Output:
```text
{'a': [1, 2]}
{'a': [1, 2, 3]}
```

## 11) Membership testing

```python
d = {"a": 1}

print("a" in d)
print("b" not in d)
print(1 in d)
```

Output:
```text
True
True
False
```

Note: membership checks keys only.

## 12) Hashing and key rules

Valid hashable keys:

```python
d = {
    1: "int",
    "hello": "str",
    (1, 2): "tuple",
    frozenset([1, 2]): "frozenset",
}

print(d[(1, 2)])
print(d[frozenset([1, 2])])
```

Output:
```text
tuple
frozenset
```

Invalid keys (error demo):

```python
try:
    bad = {[1, 2]: "list"}
except TypeError as e:
    print(e)
```

Output:
```text
unhashable type: 'list'
```

## 13) Time complexity summary

| Operation | Average Complexity |
| --- | --- |
| Access | `O(1)` |
| Insert | `O(1)` |
| Delete | `O(1)` |
| Search by key | `O(1)` |
| Iteration | `O(n)` |

Worst case can degrade when collisions are heavy.

## 14) Dynamic views and reverse iteration

```python
d = {"a": 1}
keys_view = d.keys()

print(keys_view)
d["b"] = 2
print(keys_view)
```

Output:
```text
dict_keys(['a'])
dict_keys(['a', 'b'])
```

Set operation on views:

```python
d1 = {"a": 1, "b": 2}
d2 = {"b": 3, "c": 4}

print(d1.keys() & d2.keys())
```

Output:
```text
{'b'}
```

Reverse iteration:

```python
d = {"a": 1, "b": 2, "c": 3}
for key in reversed(d):
    print(key)
```

Output:
```text
c
b
a
```

## 15) Advanced useful classes

`defaultdict`:

```python
from collections import defaultdict

freq = defaultdict(int)
freq["a"] += 1
freq["a"] += 1
print(dict(freq))

groups = defaultdict(list)
groups["c"].append("cat")
groups["c"].append("car")
print(dict(groups))
```

Output:
```text
{'a': 2}
{'c': ['cat', 'car']}
```

`Counter`:

```python
from collections import Counter

arr = [1, 1, 2, 2, 2, 3]
c = Counter(arr)
print(c)
print(c.most_common(1))
```

Output:
```text
Counter({2: 3, 1: 2, 3: 1})
[(2, 3)]
```

`ChainMap`:

```python
from collections import ChainMap

defaults = {"theme": "dark", "lang": "en"}
user = {"theme": "light"}
config = ChainMap(user, defaults)

print(config["theme"])
print(config["lang"])
```

Output:
```text
light
en
```

`MappingProxyType`:

```python
from types import MappingProxyType

d = {"a": 1}
proxy = MappingProxyType(d)
print(proxy["a"])

d["a"] = 10
print(proxy["a"])
```

Output:
```text
1
10
```

## 16) Practical interview patterns

Frequency counter:

```python
arr = [1, 1, 2, 3, 2, 1]
freq = {}

for x in arr:
    freq[x] = freq.get(x, 0) + 1

print(freq)
```

Output:
```text
{1: 3, 2: 2, 3: 1}
```

Grouping:

```python
words = ["cat", "car", "dog"]
groups = {}

for word in words:
    first = word[0]
    groups.setdefault(first, []).append(word)

print(groups)
```

Output:
```text
{'c': ['cat', 'car'], 'd': ['dog']}
```

Dispatch table:

```python
def add(a, b):
    return a + b

def sub(a, b):
    return a - b

ops = {
    "+": add,
    "-": sub,
}

print(ops["+"](10, 3))
print(ops["-"](10, 3))
```

Output:
```text
13
7
```

Memoization:

```python
memo = {}

def fib(n):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib(n - 1) + fib(n - 2)
    return memo[n]

print(fib(7))
print(memo)
```

Output:
```text
13
{2: 1, 3: 2, 4: 3, 5: 5, 6: 8, 7: 13}
```

Graph adjacency list:

```python
edges = [(1, 2), (1, 3), (2, 4)]
graph = {}

for u, v in edges:
    graph.setdefault(u, []).append(v)

print(graph)
```

Output:
```text
{1: [2, 3], 2: [4]}
```

## 17) Common pitfalls

Mutable default with `fromkeys`:

```python
d = dict.fromkeys(["a", "b"], [])
d["a"].append(1)
print(d)
```

Output:
```text
{'a': [1], 'b': [1]}
```

Modifying size during iteration:

```python
d = {"a": 1, "b": 2}

try:
    for k in d:
        del d[k]
except RuntimeError as e:
    print(e)
```

Output:
```text
dictionary changed size during iteration
```

Safe deletion:

```python
d = {"a": 1, "b": 2}
for k in list(d.keys()):
    del d[k]

print(d)
```

Output:
```text
{}
```

Invert collision issue:

```python
d = {"a": 1, "b": 1}
inv = {v: k for k, v in d.items()}
print(inv)
```

Output:
```text
{1: 'b'}
```

## 18) Internal behavior (conceptual)
- Dictionaries use hashing plus probing for fast average lookup.
- Heavy collision patterns can reduce performance.
- Resizing is automatic when load increases.
- Deletions can leave internal markers until rebuild/resize.

## 19) Best practices
- Use `get()` when keys may be missing.
- Use `defaultdict` for grouping/counting-heavy logic.
- Use immutable keys.
- Avoid changing dictionary size while iterating directly.
- Use deep copy only when nested independence is required.

## 20) Self-check questions (with verification output)

1. **Question:** `in` operator checks keys or values?

```python
d = {"a": 10}
print("a" in d)
print(10 in d)
```

Output:
```text
True
False
```

**Answer:** It checks keys.

**Reason:** Dictionary membership is defined on keys.

2. **Question:** What happens on missing key with indexing?

```python
d = {"x": 1}
try:
    print(d["y"])
except KeyError:
    print("KeyError")
```

Output:
```text
KeyError
```

**Answer:** It raises `KeyError`.

**Reason:** Indexing requires key presence.

3. **Question:** Why prefer `get()` in optional lookups?

```python
d = {"x": 1}
print(d.get("y"))
print(d.get("y", 0))
```

Output:
```text
None
0
```

**Answer:** It avoids exceptions for missing keys.

**Reason:** `get()` returns fallback values safely.

4. **Question:** Why can shallow copy affect original nested data?

```python
d1 = {"a": [1]}
d2 = d1.copy()
d2["a"].append(2)
print(d1)
```

Output:
```text
{'a': [1, 2]}
```

**Answer:** Inner mutable objects are shared.

**Reason:** Shallow copy duplicates only outer container.

5. **Question:** Why does deep copy prevent shared nested changes?

```python
import copy

d1 = {"a": [1]}
d2 = copy.deepcopy(d1)
d2["a"].append(2)
print(d1)
```

Output:
```text
{'a': [1]}
```

**Answer:** Deep copy duplicates nested objects recursively.

**Reason:** Changes in copy do not affect original nested references.

6. **Question:** Why is `fromkeys(..., [])` risky?

```python
d = dict.fromkeys(["a", "b"], [])
d["a"].append(99)
print(d)
```

Output:
```text
{'a': [99], 'b': [99]}
```

**Answer:** Both keys reference the same list object.

**Reason:** One default object is reused for all keys.

7. **Question:** Which side wins in dictionary merge on same key?

```python
left = {"x": 1}
right = {"x": 2}
print(left | right)
```

Output:
```text
{'x': 2}
```

**Answer:** Right side wins.

**Reason:** Merge applies right mapping last.

8. **Question:** Why do duplicate values lose data when inverting dict?

```python
d = {"a": 1, "b": 1}
inv = {v: k for k, v in d.items()}
print(inv)
```

Output:
```text
{1: 'b'}
```

**Answer:** Later key overwrites earlier one.

**Reason:** Dictionary keys must be unique.

9. **Question:** Why is dictionary useful for frequency counting?

```python
arr = [2, 2, 3]
freq = {}
for x in arr:
    freq[x] = freq.get(x, 0) + 1
print(freq)
```

Output:
```text
{2: 2, 3: 1}
```

**Answer:** It tracks counts by key efficiently.

**Reason:** Each update is fast average-case lookup + write.

10. **Question:** Why avoid changing size during iteration?

```python
d = {"a": 1, "b": 2}
try:
    for k in d:
        d["z"] = 0
except RuntimeError as e:
    print(e)
```

Output:
```text
dictionary changed size during iteration
```

**Answer:** It breaks iterator consistency.

**Reason:** Iterator expects stable container size while traversing.

11. **Question:** Do views update when dictionary changes?

```python
d = {"a": 1}
v = d.keys()
print(v)
d["b"] = 2
print(v)
```

Output:
```text
dict_keys(['a'])
dict_keys(['a', 'b'])
```

**Answer:** Yes, views are dynamic.

**Reason:** They reflect the live dictionary state.

12. **Question:** Why use dictionary dispatch pattern?

```python
def hi():
    return "hello"

actions = {"greet": hi}
print(actions["greet"]())
```

Output:
```text
hello
```

**Answer:** It replaces long condition chains cleanly.

**Reason:** Behavior is selected by key lookup, making code extensible.