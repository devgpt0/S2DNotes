# Python Dictionary Worksheet Answers

Source Worksheet: `python/assignement/worksheets/collection_framwork/dict.md`

## Level 1 Answers

### Tricky Predict the Output Solutions (50)

1.
```python
student = {"name": "Ad", "age": 22}
print(type(student).__name__)
print(student["name"])
```

Correct Output:
```text
dict
Ad
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

2.
```python
d = dict()
print(d)
```

Correct Output:
```text
{}
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

3.
```python
d = dict(name="Ad", age=22)
print(d)
```

Correct Output:
```text
{'name': 'Ad', 'age': 22}
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

4.
```python
d = dict([("a", 1), ("b", 2)])
print(d["b"])
```

Correct Output:
```text
2
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

5.
```python
sq = {x: x * x for x in range(4)}
print(sq)
```

Correct Output:
```text
{0: 0, 1: 1, 2: 4, 3: 9}
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

6.
```python
d = {"x": 10, "y": 20}
print(d["x"])
```

Correct Output:
```text
10
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

7.
```python
d = {"x": 10}
print(d.get("z"))
print(d.get("z", 0))
```

Correct Output:
```text
None
0
```
Reason: `get` returns a default (or `None`) when the key is missing, so execution continues safely.

8.
```python
d = {"x": 10}
try:
    print(d["z"])
except KeyError:
    print("KeyError")
```

Correct Output:
```text
KeyError
```
Reason: Direct indexing or `pop` without default raises `KeyError` on missing keys.

9.
```python
d = {}
d["name"] = "Ad"
print(d)
```

Correct Output:
```text
{'name': 'Ad'}
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

10.
```python
d = {"name": "Ad"}
d["name"] = "AI Engineer"
print(d)
```

Correct Output:
```text
{'name': 'AI Engineer'}
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

11.
```python
d = {"a": 1}
d.update({"b": 2, "c": 3})
print(d)
```

Correct Output:
```text
{'a': 1, 'b': 2, 'c': 3}
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

12.
```python
d1 = {"a": 1, "x": 10}
d2 = {"b": 2, "x": 99}
print(d1 | d2)
```

Correct Output:
```text
{'a': 1, 'x': 99, 'b': 2}
```
Reason: In dictionary union, duplicate keys are resolved by keeping the right-side value.

13.
```python
d1 = {"a": 1}
d1 |= {"b": 2}
print(d1)
```

Correct Output:
```text
{'a': 1, 'b': 2}
```
Reason: In dictionary union, duplicate keys are resolved by keeping the right-side value.

14.
```python
d = {"a": 1, "b": 2}
print(d.pop("a"))
print(d)
```

Correct Output:
```text
1
{'b': 2}
```
Reason: `pop` removes by key and returns the removed value (or given default).

15.
```python
d = {"a": 1, "b": 2}
print(d.popitem())
print(d)
```

Correct Output:
```text
('b', 2)
{'a': 1}
```
Reason: `popitem()` removes and returns the last inserted key-value pair.

16.
```python
d = {"a": 1, "b": 2}
del d["b"]
print(d)
```

Correct Output:
```text
{'a': 1}
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

17.
```python
d = {"a": 1, "b": 2}
d.clear()
print(d)
```

Correct Output:
```text
{}
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

18.
```python
d = {"a": 1, "b": 2}
print(list(d.keys()))
```

Correct Output:
```text
['a', 'b']
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

19.
```python
d = {"a": 1, "b": 2}
print(list(d.values()))
```

Correct Output:
```text
[1, 2]
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

20.
```python
d = {"a": 1, "b": 2}
print(list(d.items()))
```

Correct Output:
```text
[('a', 1), ('b', 2)]
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

21.
```python
d = {"a": 1}
print(d.setdefault("a", 100))
print(d)
```

Correct Output:
```text
1
{'a': 1}
```
Reason: `setdefault` returns existing value if present, otherwise inserts and returns the default.

22.
```python
d = {"a": 1}
print(d.setdefault("b", 100))
print(d)
```

Correct Output:
```text
100
{'a': 1, 'b': 100}
```
Reason: `setdefault` returns existing value if present, otherwise inserts and returns the default.

23.
```python
keys = ["x", "y", "z"]
d = dict.fromkeys(keys, 0)
print(d)
```

Correct Output:
```text
{'x': 0, 'y': 0, 'z': 0}
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

24.
```python
d = dict.fromkeys(["a", "b"], [])
d["a"].append(1)
print(d)
```

Correct Output:
```text
{'a': [1], 'b': [1]}
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

25.
```python
d = {"a": 1}
print("a" in d, 1 in d)
```

Correct Output:
```text
True False
```
Reason: Membership checks and item views follow dictionary key/value-pair semantics.

26.
```python
d = {"a": 1, "b": 2}
for k in d:
    print(k, end=" ")
print()
```

Correct Output:
```text
a b 
```
Reason: Membership checks and item views follow dictionary key/value-pair semantics.

27.
```python
d = {"a": 1, "b": 2}
for v in d.values():
    print(v, end=" ")
print()
```

Correct Output:
```text
1 2 
```
Reason: Membership checks and item views follow dictionary key/value-pair semantics.

28.
```python
d = {"a": 1, "b": 2}
for k, v in d.items():
    print(k, v)
```

Correct Output:
```text
a 1
b 2
```
Reason: Membership checks and item views follow dictionary key/value-pair semantics.

29.
```python
d = {"a": 1, "b": 2, "c": 3}
for k in reversed(d):
    print(k, end=" ")
print()
```

Correct Output:
```text
c b a 
```
Reason: Reverse iteration over dictionary keys follows reverse insertion order.

30.
```python
d = {"a": 1}
k = d.keys()
print(k)
d["b"] = 2
print(k)
```

Correct Output:
```text
dict_keys(['a'])
dict_keys(['a', 'b'])
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

31.
```python
d1 = {"a": 1, "b": 2}
d2 = {"b": 3, "c": 4}
print(d1.keys() & d2.keys())
```

Correct Output:
```text
{'b'}
```
Reason: Dictionary key views support set operations such as intersection/union/difference.

32.
```python
even_sq = {x: x * x for x in range(6) if x % 2 == 0}
print(even_sq)
```

Correct Output:
```text
{0: 0, 2: 4, 4: 16}
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

33.
```python
d = {"a": 1, "b": 2}
rev = {v: k for k, v in d.items()}
print(rev)
```

Correct Output:
```text
{1: 'a', 2: 'b'}
```
Reason: Membership checks and item views follow dictionary key/value-pair semantics.

34.
```python
d = {"a": 1, "b": 1}
rev = {v: k for k, v in d.items()}
print(rev)
```

Correct Output:
```text
{1: 'b'}
```
Reason: Membership checks and item views follow dictionary key/value-pair semantics.

35.
```python
students = {101: {"name": "Ad", "age": 22}}
print(students[101]["name"])
```

Correct Output:
```text
Ad
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

36.
```python
students = {101: {"name": "Ad", "age": 22}}
students[101]["age"] = 23
print(students)
```

Correct Output:
```text
{101: {'name': 'Ad', 'age': 23}}
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

37.
```python
d1 = {"a": [1, 2]}
d2 = d1.copy()
d2["a"].append(3)
print(d1)
print(d2)
```

Correct Output:
```text
{'a': [1, 2, 3]}
{'a': [1, 2, 3]}
```
Reason: `copy()` is shallow; nested mutable objects are still shared references.

38.
```python
import copy

d1 = {"a": [1, 2]}
d2 = copy.deepcopy(d1)
d2["a"].append(3)
print(d1)
print(d2)
```

Correct Output:
```text
{'a': [1, 2]}
{'a': [1, 2, 3]}
```
Reason: `deepcopy` clones nested mutable objects, so changes in the copy do not affect the original.

39.
```python
d = {"a": 1}
print(d.pop("x", 999))
print(d)
```

Correct Output:
```text
999
{'a': 1}
```
Reason: `pop` removes by key and returns the removed value (or given default).

40.
```python
d = {"a": 1}
try:
    d.pop("x")
except KeyError:
    print("KeyError")
```

Correct Output:
```text
KeyError
```
Reason: `pop` removes by key and returns the removed value (or given default).

41.
```python
arr = [1, 1, 2, 3, 2, 1]
freq = {}
for x in arr:
    freq[x] = freq.get(x, 0) + 1
print(freq)
```

Correct Output:
```text
{1: 3, 2: 2, 3: 1}
```
Reason: `get` returns a default (or `None`) when the key is missing, so execution continues safely.

42.
```python
words = ["cat", "car", "dog"]
groups = {}
for w in words:
    groups.setdefault(w[0], []).append(w)
print(groups)
```

Correct Output:
```text
{'c': ['cat', 'car'], 'd': ['dog']}
```
Reason: `setdefault` returns existing value if present, otherwise inserts and returns the default.

43.
```python
from collections import defaultdict

d = defaultdict(int)
d["a"] += 1
d["a"] += 1
print(dict(d))
```

Correct Output:
```text
{'a': 2}
```
Reason: `defaultdict` auto-creates missing keys using its factory (`int`, `list`, or `set`).

44.
```python
from collections import defaultdict

d = defaultdict(list)
d["c"].append("cat")
d["c"].append("car")
print(dict(d))
```

Correct Output:
```text
{'c': ['cat', 'car']}
```
Reason: `defaultdict` auto-creates missing keys using its factory (`int`, `list`, or `set`).

45.
```python
from collections import Counter

c = Counter([1, 1, 2, 2, 2, 3])
print(c)
```

Correct Output:
```text
Counter({2: 3, 1: 2, 3: 1})
```
Reason: `Counter` tallies frequencies and exposes them directly in dictionary-like form.

46.
```python
from collections import Counter

c = Counter([1, 1, 2, 2, 2, 3])
print(c.most_common(1))
```

Correct Output:
```text
[(2, 3)]
```
Reason: `Counter` tallies frequencies and exposes them directly in dictionary-like form.

47.
```python
from collections import ChainMap

c = ChainMap({"theme": "light"}, {"theme": "dark", "lang": "en"})
print(c["theme"], c["lang"])
```

Correct Output:
```text
light en
```
Reason: `ChainMap` resolves keys from left to right and writes to the first mapping.

48.
```python
from types import MappingProxyType

d = {"a": 1}
proxy = MappingProxyType(d)
print(proxy["a"])
d["a"] = 10
print(proxy["a"])
```

Correct Output:
```text
1
10
```
Reason: `MappingProxyType` is a read-only view of the same underlying dictionary object.

49.
```python
d = {"a": 1, "b": 2}
for k in list(d.keys()):
    del d[k]
print(d)
```

Correct Output:
```text
{}
```
Reason: Iterating over a copied key list is safe when deleting keys from the dictionary.

50.
```python
d = {"a": 1, "b": 2}
try:
    for k in d:
        del d[k]
except RuntimeError as e:
    print(type(e).__name__)
```

Correct Output:
```text
RuntimeError
```
Reason: Changing dictionary size during direct iteration raises `RuntimeError`.

### MCQ Theory Answer Key (50)

1. A dictionary is primarily a:
Answer: **A**
Reason: `key-value mapping` is correct for dictionary behavior and interview-style usage in this worksheet.

2. Dictionary lookup average complexity is:
Answer: **A**
Reason: `O(1)` is correct for dictionary behavior and interview-style usage in this worksheet.

3. Which syntax creates an empty dictionary?
Answer: **A**
Reason: `{}` is correct for dictionary behavior and interview-style usage in this worksheet.

4. `d[key]` on missing key:
Answer: **A**
Reason: `KeyError` is correct for dictionary behavior and interview-style usage in this worksheet.

5. `d.get(key)` on missing key returns:
Answer: **A**
Reason: `None by default` is correct for dictionary behavior and interview-style usage in this worksheet.

6. `d.get(key, default)` is used for:
Answer: **A**
Reason: `safe optional lookup` is correct for dictionary behavior and interview-style usage in this worksheet.

7. Keys in dictionary must be:
Answer: **A**
Reason: `hashable` is correct for dictionary behavior and interview-style usage in this worksheet.

8. Which is a valid key?
Answer: **A**
Reason: `(1, 2)` is correct for dictionary behavior and interview-style usage in this worksheet.

9. Which is invalid as key?
Answer: **A**
Reason: `list` is correct for dictionary behavior and interview-style usage in this worksheet.

10. `update()` does:
Answer: **A**
Reason: `merge/overwrite keys` is correct for dictionary behavior and interview-style usage in this worksheet.

11. In `d1 | d2`, duplicate key value comes from:
Answer: **A**
Reason: `d2` is correct for dictionary behavior and interview-style usage in this worksheet.

12. `pop(k)` returns:
Answer: **A**
Reason: `removed value` is correct for dictionary behavior and interview-style usage in this worksheet.

13. `popitem()` removes:
Answer: **A**
Reason: `last inserted key-value pair` is correct for dictionary behavior and interview-style usage in this worksheet.

14. `clear()` does:
Answer: **A**
Reason: `empties dictionary in-place` is correct for dictionary behavior and interview-style usage in this worksheet.

15. `keys()` returns:
Answer: **A**
Reason: `dynamic view object` is correct for dictionary behavior and interview-style usage in this worksheet.

16. Membership test `x in d` checks:
Answer: **A**
Reason: `keys` is correct for dictionary behavior and interview-style usage in this worksheet.

17. Iterating directly over dict yields:
Answer: **A**
Reason: `keys` is correct for dictionary behavior and interview-style usage in this worksheet.

18. `items()` gives:
Answer: **A**
Reason: `key-value pair view` is correct for dictionary behavior and interview-style usage in this worksheet.

19. `setdefault(k, v)` when key exists:
Answer: **A**
Reason: `keeps existing value` is correct for dictionary behavior and interview-style usage in this worksheet.

20. `setdefault(k, v)` when key missing:
Answer: **A**
Reason: `inserts key with v` is correct for dictionary behavior and interview-style usage in this worksheet.

21. `dict.fromkeys(keys, val)` with mutable `val` can cause:
Answer: **A**
Reason: `shared reference pitfall` is correct for dictionary behavior and interview-style usage in this worksheet.

22. Shallow copy of dict with nested list means:
Answer: **A**
Reason: `nested list reference shared` is correct for dictionary behavior and interview-style usage in this worksheet.

23. Deep copy ensures:
Answer: **A**
Reason: `nested objects independent` is correct for dictionary behavior and interview-style usage in this worksheet.

24. Dictionary comprehension creates:
Answer: **A**
Reason: `new dictionary` is correct for dictionary behavior and interview-style usage in this worksheet.

25. `for k, v in d.items()` iterates over:
Answer: **A**
Reason: `key-value pairs` is correct for dictionary behavior and interview-style usage in this worksheet.

26. Reverse iteration of dict follows:
Answer: **A**
Reason: `reverse insertion order` is correct for dictionary behavior and interview-style usage in this worksheet.

27. Which statement about dict order is correct?
Answer: **A**
Reason: `insertion order is preserved` is correct for dictionary behavior and interview-style usage in this worksheet.

28. Heavy collision cases can degrade lookup to:
Answer: **A**
Reason: `O(n)` is correct for dictionary behavior and interview-style usage in this worksheet.

29. `defaultdict(int)` missing key returns default:
Answer: **A**
Reason: `0` is correct for dictionary behavior and interview-style usage in this worksheet.

30. `defaultdict(list)` missing key returns:
Answer: **A**
Reason: `new empty list` is correct for dictionary behavior and interview-style usage in this worksheet.

31. `Counter` is best suited for:
Answer: **A**
Reason: `frequency counting` is correct for dictionary behavior and interview-style usage in this worksheet.

32. `Counter.most_common(1)` returns:
Answer: **A**
Reason: `top frequency pair list` is correct for dictionary behavior and interview-style usage in this worksheet.

33. `ChainMap` lookup priority is:
Answer: **A**
Reason: `left to right mappings` is correct for dictionary behavior and interview-style usage in this worksheet.

34. `MappingProxyType` provides:
Answer: **A**
Reason: `read-only dictionary view` is correct for dictionary behavior and interview-style usage in this worksheet.

35. Modifying dict size during iteration may raise:
Answer: **A**
Reason: `RuntimeError` is correct for dictionary behavior and interview-style usage in this worksheet.

36. Safe deletion while iterating usually uses:
Answer: **A**
Reason: `list(d.keys())` is correct for dictionary behavior and interview-style usage in this worksheet.

37. Best pattern for frequency in loop:
Answer: **A**
Reason: `d[x] = d.get(x, 0) + 1` is correct for dictionary behavior and interview-style usage in this worksheet.

38. Inverting dict with duplicate values causes:
Answer: **A**
Reason: `overwrite collisions` is correct for dictionary behavior and interview-style usage in this worksheet.

39. Complexity of iterating all items is:
Answer: **A**
Reason: `O(n)` is correct for dictionary behavior and interview-style usage in this worksheet.

40. A dictionary is generally implemented using:
Answer: **A**
Reason: `hash table concepts` is correct for dictionary behavior and interview-style usage in this worksheet.

41. `d.copy()` returns:
Answer: **A**
Reason: `shallow copy` is correct for dictionary behavior and interview-style usage in this worksheet.

42. `del d[k]` on missing key raises:
Answer: **A**
Reason: `KeyError` is correct for dictionary behavior and interview-style usage in this worksheet.

43. `pop(k, default)` on missing key returns:
Answer: **A**
Reason: `default` is correct for dictionary behavior and interview-style usage in this worksheet.

44. Which is best for grouping words by first character?
Answer: **A**
Reason: `setdefault/defaultdict(list)` is correct for dictionary behavior and interview-style usage in this worksheet.

45. `keys()` and `values()` views are:
Answer: **A**
Reason: `dynamic` is correct for dictionary behavior and interview-style usage in this worksheet.

46. Which data structure supports sparse key mapping naturally?
Answer: **A**
Reason: `dict` is correct for dictionary behavior and interview-style usage in this worksheet.

47. To avoid accidental mutation sharing in nested structures use:
Answer: **A**
Reason: `deepcopy when needed` is correct for dictionary behavior and interview-style usage in this worksheet.

48. `in` on `d.values()` complexity is typically:
Answer: **A**
Reason: `O(n)` is correct for dictionary behavior and interview-style usage in this worksheet.

49. Which statement is true about `Counter`?
Answer: **A**
Reason: `it is a dict subclass for counts` is correct for dictionary behavior and interview-style usage in this worksheet.

50. Which is interview-friendly dict checklist?
Answer: **A**
Reason: `key existence, edge cases, copy behavior, complexity` is correct for dictionary behavior and interview-style usage in this worksheet.

## Level 2 Answers

### Tricky Predict the Output Solutions (50)

1.
```python
class User:
    def __init__(self, uid):
        self.uid = uid
    def __hash__(self):
        return hash(self.uid)
    def __eq__(self, other):
        return self.uid == other.uid

u1 = User(1)
u2 = User(1)
d = {u1: "Ad"}
print(d[u2])
```

Correct Output:
```text
Ad
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

2.
```python
try:
    d = {(1, [2, 3]): "x"}
except TypeError as e:
    print(type(e).__name__)
```

Correct Output:
```text
TypeError
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

3.
```python
d = {frozenset([1, 2]): "ok"}
print(d[frozenset([2, 1])])
```

Correct Output:
```text
ok
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

4.
```python
d = {x: ("even" if x % 2 == 0 else "odd") for x in range(5)}
print(d)
```

Correct Output:
```text
{0: 'even', 1: 'odd', 2: 'even', 3: 'odd', 4: 'even'}
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

5.
```python
keys = ["a", "b", "c"]
vals = [10, 20, 30]
print(dict(zip(keys, vals)))
```

Correct Output:
```text
{'a': 10, 'b': 20, 'c': 30}
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

6.
```python
d1 = {"a": 1}
d2 = {"b": 2}
d3 = {"a": 9}
print(d1 | d2 | d3)
```

Correct Output:
```text
{'a': 9, 'b': 2}
```
Reason: In dictionary union, duplicate keys are resolved by keeping the right-side value.

7.
```python
d = {"a": 1}
out = d.update({"b": 2})
print(out)
print(d)
```

Correct Output:
```text
None
{'a': 1, 'b': 2}
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

8.
```python
d1 = {"a": [1]}
d2 = d1.copy()
print(d1 is d2)
print(d1["a"] is d2["a"])
```

Correct Output:
```text
False
True
```
Reason: `copy()` is shallow; nested mutable objects are still shared references.

9.
```python
import copy

d1 = {"a": [1]}
d2 = copy.deepcopy(d1)
print(d1 is d2)
print(d1["a"] is d2["a"])
```

Correct Output:
```text
False
False
```
Reason: `deepcopy` clones nested mutable objects, so changes in the copy do not affect the original.

10.
```python
d1 = {"a": 1, "b": 2, "c": 3}
d2 = {"b": 9}
print(d1.keys() - d2.keys())
```

Correct Output:
```text
{'c', 'a'}
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

11.
```python
d1 = {"a": 1, "b": 2}
d2 = {"b": 9, "c": 3}
print(d1.keys() | d2.keys())
```

Correct Output:
```text
{'c', 'b', 'a'}
```
Reason: In dictionary union, duplicate keys are resolved by keeping the right-side value.

12.
```python
d = {"a": 1, "b": 2}
print(("a", 1) in d.items())
print(("a", 2) in d.items())
```

Correct Output:
```text
True
False
```
Reason: Membership checks and item views follow dictionary key/value-pair semantics.

13.
```python
d = {"x": 1, "y": 2}
d["x"] = 100
print(d.popitem())
```

Correct Output:
```text
('y', 2)
```
Reason: `popitem()` removes and returns the last inserted key-value pair.

14.
```python
d = {"a": 1, "b": 2, "c": 3}
del d["b"]
d["b"] = 20
print(list(d.keys()))
```

Correct Output:
```text
['a', 'c', 'b']
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

15.
```python
d = {"a": 3, "b": 1, "c": 2}
out = dict(sorted(d.items(), key=lambda x: x[1]))
print(out)
```

Correct Output:
```text
{'b': 1, 'c': 2, 'a': 3}
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

16.
```python
d = {"a": 3, "b": 1, "c": 2}
out = dict(sorted(d.items(), key=lambda x: x[0], reverse=True))
print(out)
```

Correct Output:
```text
{'c': 2, 'b': 1, 'a': 3}
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

17.
```python
def add(a, b):
    return a + b

def sub(a, b):
    return a - b

ops = {"+": add, "-": sub}
print(ops["+"](10, 3), ops["-"](10, 3))
```

Correct Output:
```text
13 7
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

18.
```python
memo = {}

def fib(n):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib(n - 1) + fib(n - 2)
    return memo[n]

print(fib(6))
print(sorted(memo.items()))
```

Correct Output:
```text
8
[(2, 1), (3, 2), (4, 3), (5, 5), (6, 8)]
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

19.
```python
edges = [(1, 2), (1, 3), (2, 4)]
graph = {}
for u, v in edges:
    graph.setdefault(u, []).append(v)
print(graph)
```

Correct Output:
```text
{1: [2, 3], 2: [4]}
```
Reason: `setdefault` returns existing value if present, otherwise inserts and returns the default.

20.
```python
arr = ["a", "b", "a", "c", "b", "a"]
freq = {}
for x in arr:
    freq[x] = freq.get(x, 0) + 1
print(freq)
```

Correct Output:
```text
{'a': 3, 'b': 2, 'c': 1}
```
Reason: `get` returns a default (or `None`) when the key is missing, so execution continues safely.

21.
```python
from collections import Counter

arr = ["a", "b", "a", "c", "b", "a"]
print(Counter(arr) == {"a": 3, "b": 2, "c": 1})
```

Correct Output:
```text
True
```
Reason: `Counter` tallies frequencies and exposes them directly in dictionary-like form.

22.
```python
from collections import ChainMap

defaults = {"theme": "dark", "lang": "en"}
user = {"theme": "light"}
c = ChainMap(user, defaults)
print(c["theme"], c["lang"])
```

Correct Output:
```text
light en
```
Reason: `ChainMap` resolves keys from left to right and writes to the first mapping.

23.
```python
from collections import ChainMap

a = {"x": 1}
b = {"x": 2}
c = ChainMap(a, b)
c["y"] = 9
print(a)
print(b)
```

Correct Output:
```text
{'x': 1, 'y': 9}
{'x': 2}
```
Reason: `ChainMap` resolves keys from left to right and writes to the first mapping.

24.
```python
from types import MappingProxyType

d = {"a": 1}
proxy = MappingProxyType(d)
try:
    proxy["b"] = 2
except TypeError as e:
    print(type(e).__name__)
```

Correct Output:
```text
TypeError
```
Reason: `MappingProxyType` is a read-only view of the same underlying dictionary object.

25.
```python
class ZeroDict(dict):
    def __missing__(self, key):
        return 0

d = ZeroDict()
print(d["x"])
print(d.get("y"))
```

Correct Output:
```text
0
None
```
Reason: `get` returns a default (or `None`) when the key is missing, so execution continues safely.

26.
```python
d = {"a": 1}
v = d.values()
print(v)
d["b"] = 2
print(v)
```

Correct Output:
```text
dict_values([1])
dict_values([1, 2])
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

27.
```python
d = {"a": 1, "b": 2, "c": 3}
print({"a", "b"}.issubset(d.keys()))
```

Correct Output:
```text
True
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

28.
```python
d1 = {"a": 1, "b": 2}
d2 = {"b": 9, "c": 3}
print({**d1, **d2})
```

Correct Output:
```text
{'a': 1, 'b': 9, 'c': 3}
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

29.
```python
matrix = {}
matrix[(1, 2)] = 10
matrix[(2, 1)] = 20
print(matrix[(1, 2)], matrix[(2, 1)])
```

Correct Output:
```text
10 20
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

30.
```python
d = dict.fromkeys(["p", "q"])
print(d)
```

Correct Output:
```text
{'p': None, 'q': None}
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

31.
```python
d = {"a": 1}
print(d.get("a", 100))
print(d.get("b", 100))
```

Correct Output:
```text
1
100
```
Reason: `get` returns a default (or `None`) when the key is missing, so execution continues safely.

32.
```python
d = {"a": 1, "b": 2, "c": 3}
print({k: v for k, v in d.items() if v % 2 == 1})
```

Correct Output:
```text
{'a': 1, 'c': 3}
```
Reason: Membership checks and item views follow dictionary key/value-pair semantics.

33.
```python
d = {"a": 10, "b": 20}
print(sum(d.values()))
```

Correct Output:
```text
30
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

34.
```python
d = {"a": 1}
print(bool(d))
d.clear()
print(bool(d))
```

Correct Output:
```text
True
False
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

35.
```python
d = {"a": 1, "b": 2}
print(min(d), max(d))
```

Correct Output:
```text
a b
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

36.
```python
d = {"a": 1, "b": 2}
print(sorted(d))
```

Correct Output:
```text
['a', 'b']
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

37.
```python
d = {"x": 1, "y": 2}
print(list(d.items())[0])
```

Correct Output:
```text
('x', 1)
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

38.
```python
d = {"x": 1, "y": 2, "z": 3}
print(next(iter(d)))
```

Correct Output:
```text
x
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

39.
```python
from collections import defaultdict

d = defaultdict(set)
for ch in "banana":
    d[ch].add(ch.upper())
print({k: sorted(v) for k, v in d.items()})
```

Correct Output:
```text
{'b': ['B'], 'a': ['A'], 'n': ['N']}
```
Reason: `defaultdict` auto-creates missing keys using its factory (`int`, `list`, or `set`).

40.
```python
from collections import Counter

c = Counter("aabccc")
c.update("cc")
print(c)
```

Correct Output:
```text
Counter({'c': 5, 'a': 2, 'b': 1})
```
Reason: `Counter` tallies frequencies and exposes them directly in dictionary-like form.

41.
```python
from collections import Counter

c = Counter([1, 1, 2, 3])
c.subtract([1, 3])
print(c)
```

Correct Output:
```text
Counter({1: 1, 2: 1, 3: 0})
```
Reason: `Counter` tallies frequencies and exposes them directly in dictionary-like form.

42.
```python
d = {"a": 1, "b": 2}
d["c"] = 3
d.pop("b")
d["b"] = 20
print(list(d.keys()))
```

Correct Output:
```text
['a', 'c', 'b']
```
Reason: `pop` removes by key and returns the removed value (or given default).

43.
```python
d = {"a": 1}
d.clear()
d["x"] = 9
print(d)
```

Correct Output:
```text
{'x': 9}
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

44.
```python
d1 = {"a": 1}
d2 = d1.copy()
d2["b"] = 2
print(d1)
print(d2)
```

Correct Output:
```text
{'a': 1}
{'a': 1, 'b': 2}
```
Reason: `copy()` is shallow; nested mutable objects are still shared references.

45.
```python
d1 = {"a": [1]}
d2 = d1.copy()
d2["a"][0] = 99
print(d1)
```

Correct Output:
```text
{'a': [99]}
```
Reason: `copy()` is shallow; nested mutable objects are still shared references.

46.
```python
d = {"a": None}
print(d.get("a", 100))
print(d.get("b", 100))
```

Correct Output:
```text
None
100
```
Reason: `get` returns a default (or `None`) when the key is missing, so execution continues safely.

47.
```python
d = {"a": 1, "b": 2}
k = d.keys()
print("a" in k)
d.pop("a")
print("a" in k)
```

Correct Output:
```text
True
False
```
Reason: `pop` removes by key and returns the removed value (or given default).

48.
```python
d = {"a": 3, "b": 1, "c": 2}
print(sorted(d.items(), key=lambda kv: kv[1], reverse=True))
```

Correct Output:
```text
[('a', 3), ('c', 2), ('b', 1)]
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

49.
```python
d = {}
d[1] = "int"
d[True] = "bool"
print(d)
print(len(d))
```

Correct Output:
```text
{1: 'bool'}
1
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

50.
```python
d = {}
d[1] = "int"
d[1.0] = "float"
print(d)
print(len(d))
```

Correct Output:
```text
{1: 'float'}
1
```
Reason: Python evaluates statements in order; the output reflects dictionary lookup, mutation, and iteration rules in this snippet.

### MCQ Theory Answer Key (50)

1. In interview coding, the most common dict use-case is:
Answer: **A**
Reason: `frequency counting/grouping` is correct for advanced dictionary concepts and coding-test expectations.

2. Why is dict lookup called amortized O(1)?
Answer: **A**
Reason: `occasional costly resize but average constant-time operations` is correct for advanced dictionary concepts and coding-test expectations.

3. High collision scenarios may cause:
Answer: **A**
Reason: `performance degradation` is correct for advanced dictionary concepts and coding-test expectations.

4. Best key choice for stable behavior is usually:
Answer: **A**
Reason: `immutable and simple types` is correct for advanced dictionary concepts and coding-test expectations.

5. Which statement about `dict.get()` is correct?
Answer: **A**
Reason: `does not raise KeyError for missing key` is correct for advanced dictionary concepts and coding-test expectations.

6. Which method can raise KeyError if key missing (without default)?
Answer: **A**
Reason: `pop` is correct for advanced dictionary concepts and coding-test expectations.

7. `setdefault` is commonly preferred for:
Answer: **A**
Reason: `grouping/appending patterns` is correct for advanced dictionary concepts and coding-test expectations.

8. `defaultdict(list)` is useful because:
Answer: **A**
Reason: `missing keys auto-create empty lists` is correct for advanced dictionary concepts and coding-test expectations.

9. `defaultdict(int)` count pattern avoids:
Answer: **A**
Reason: `explicit missing-key checks` is correct for advanced dictionary concepts and coding-test expectations.

10. `Counter` differs from plain dict mainly by:
Answer: **A**
Reason: `built-in counting helpers (`most_common`, updates)` is correct for advanced dictionary concepts and coding-test expectations.

11. `Counter.subtract()` can produce:
Answer: **A**
Reason: `zero/negative counts` is correct for advanced dictionary concepts and coding-test expectations.

12. `ChainMap` write operations affect:
Answer: **A**
Reason: `first mapping only` is correct for advanced dictionary concepts and coding-test expectations.

13. `MappingProxyType` is mainly used to:
Answer: **A**
Reason: `expose read-only views safely` is correct for advanced dictionary concepts and coding-test expectations.

14. `__missing__` hook is triggered by:
Answer: **A**
Reason: `direct indexing on missing key` is correct for advanced dictionary concepts and coding-test expectations.

15. Which operation is unsafe during direct dict iteration?
Answer: **A**
Reason: `changing dictionary size` is correct for advanced dictionary concepts and coding-test expectations.

16. Safe mutation while iterating typically uses:
Answer: **A**
Reason: `iteration over copied key list` is correct for advanced dictionary concepts and coding-test expectations.

17. In `{**d1, **d2}`, duplicate keys resolve by:
Answer: **A**
Reason: `right-most mapping wins` is correct for advanced dictionary concepts and coding-test expectations.

18. Invert dict with duplicate values usually needs:
Answer: **A**
Reason: `value-to-list grouping logic` is correct for advanced dictionary concepts and coding-test expectations.

19. Which is true for dictionary views?
Answer: **A**
Reason: `they are dynamic/live` is correct for advanced dictionary concepts and coding-test expectations.

20. Which view supports set-like intersections naturally?
Answer: **A**
Reason: `keys view` is correct for advanced dictionary concepts and coding-test expectations.

21. Best way to test key presence before heavy processing:
Answer: **A**
Reason: ``if key in d:`` is correct for advanced dictionary concepts and coding-test expectations.

22. Why can `1` and `True` collide as keys?
Answer: **A**
Reason: `they compare equal and share hash behavior` is correct for advanced dictionary concepts and coding-test expectations.

23. Why can `1` and `1.0` collapse into one key?
Answer: **A**
Reason: `equal numeric keys hash/compare equal` is correct for advanced dictionary concepts and coding-test expectations.

24. Recommended strategy for nested independent copy:
Answer: **A**
Reason: ``copy.deepcopy`` is correct for advanced dictionary concepts and coding-test expectations.

25. For sparse matrices/graphs, dict is useful due to:
Answer: **A**
Reason: `flexible non-contiguous keys` is correct for advanced dictionary concepts and coding-test expectations.

26. Dictionary dispatch pattern maps:
Answer: **A**
Reason: `operation tokens to callables` is correct for advanced dictionary concepts and coding-test expectations.

27. Memoization with dict improves recursion by:
Answer: **A**
Reason: `caching repeated subproblem results` is correct for advanced dictionary concepts and coding-test expectations.

28. Which statement about `update()` return value is true?
Answer: **A**
Reason: `returns None (in-place mutation)` is correct for advanced dictionary concepts and coding-test expectations.

29. Best interview explanation for dict speed should include:
Answer: **A**
Reason: `hashing + average probe behavior` is correct for advanced dictionary concepts and coding-test expectations.

30. Frequency count one-liner inside loop:
Answer: **A**
Reason: ``freq[x] = freq.get(x, 0) + 1`` is correct for advanced dictionary concepts and coding-test expectations.

31. Which operation is O(n) typically?
Answer: **A**
Reason: `full dict iteration` is correct for advanced dictionary concepts and coding-test expectations.

32. Which check scans values linearly?
Answer: **A**
Reason: ``target in d.values()`` is correct for advanced dictionary concepts and coding-test expectations.

33. For grouping words by first letter, best pair is:
Answer: **A**
Reason: ``defaultdict(list)` + append` is correct for advanced dictionary concepts and coding-test expectations.

34. For immutable public config exposure, choose:
Answer: **A**
Reason: ``MappingProxyType`` is correct for advanced dictionary concepts and coding-test expectations.

35. Which statement is true for dict membership complexity?
Answer: **A**
Reason: `key membership is average O(1)` is correct for advanced dictionary concepts and coding-test expectations.

36. If two mappings are chained via `ChainMap(a, b)`, lookup order is:
Answer: **A**
Reason: ``a` then `b`` is correct for advanced dictionary concepts and coding-test expectations.

37. Which is a clean approach for top-k frequent elements?
Answer: **A**
Reason: ``Counter(...).most_common(k)`` is correct for advanced dictionary concepts and coding-test expectations.

38. Why avoid `dict.fromkeys(keys, [])` in production code?
Answer: **A**
Reason: `shared mutable default causes bugs` is correct for advanced dictionary concepts and coding-test expectations.

39. Which method gives pair tuples view?
Answer: **A**
Reason: ``items()`` is correct for advanced dictionary concepts and coding-test expectations.

40. Which is true about dictionary ordering behavior?
Answer: **A**
Reason: `it reflects insertion sequence` is correct for advanced dictionary concepts and coding-test expectations.

41. In interview constraints, when dict memory is high, common alternatives include:
Answer: **A**
Reason: `arrays/tuples/specialized structures where possible` is correct for advanced dictionary concepts and coding-test expectations.

42. Why is `get()` often more readable in counting code?
Answer: **A**
Reason: `combines missing-key default with retrieval` is correct for advanced dictionary concepts and coding-test expectations.

43. Which method is best to remove and return an arbitrary-like latest pair quickly?
Answer: **A**
Reason: ``popitem()`` is correct for advanced dictionary concepts and coding-test expectations.

44. Which code can preserve key order while deduping stream with last value wins?
Answer: **A**
Reason: `plain dict assignment by key` is correct for advanced dictionary concepts and coding-test expectations.

45. `dict` as adjacency list usually maps:
Answer: **A**
Reason: `node -> list of neighbors` is correct for advanced dictionary concepts and coding-test expectations.

46. Why should explanation include worst-case O(n) even if average is O(1)?
Answer: **A**
Reason: `interviewers expect collision/pathological case awareness` is correct for advanced dictionary concepts and coding-test expectations.

47. Which is true about shallow copy + nested mutable values?
Answer: **A**
Reason: `inner mutations reflect in both dictionaries` is correct for advanced dictionary concepts and coding-test expectations.

48. For a read-mostly layered config, good pattern is:
Answer: **A**
Reason: ``ChainMap(user, defaults)`` is correct for advanced dictionary concepts and coding-test expectations.

49. In coding tests, safest missing-key strategy for optional read is:
Answer: **A**
Reason: ``get` with explicit default` is correct for advanced dictionary concepts and coding-test expectations.

50. Best final check before submitting dict-based solution:
Answer: **A**
Reason: `verify collisions in logic, missing keys, mutable defaults, complexity claims` is correct for advanced dictionary concepts and coding-test expectations.

## Interview Theory Answers (Top 25)

1. Explain why dictionary keys must be immutable and hashable.
Answer: Keys must be immutable/hashable so hash stays stable after insertion.
Reason: If hash/equality changed, the key could no longer be found in the hash table.

2. Compare `d[key]` vs `d.get(key, default)` with failure behavior.
Answer: `d[key]` raises `KeyError` when missing; `d.get(key, default)` returns a fallback.
Reason: `get` is designed for optional reads without exceptions.

3. Why is dictionary lookup average O(1)? Why not guaranteed O(1)?
Answer: Average lookup is O(1) due to hashing and direct slot probing; worst-case is O(n).
Reason: Heavy collisions/pathological cases increase probe length.

4. Explain collision handling conceptually in hash-table-backed mappings.
Answer: Collisions are resolved by probing strategy in the hash table.
Reason: Multiple keys may map to related slots, so Python searches alternative positions.

5. Difference between shallow copy and deep copy in nested dictionaries.
Answer: Shallow copy duplicates outer dict only; deep copy recursively clones nested objects.
Reason: Shared nested references in shallow copy cause cross-mutation effects.

6. Why does `dict.fromkeys(keys, [])` cause shared-state bugs?
Answer: `fromkeys(keys, [])` reuses one shared list for all keys.
Reason: Mutable default object is not copied per key.

7. Explain insertion order behavior and how delete+reinsert affects order.
Answer: Insertion order is preserved; deleting then reinserting moves key to the end.
Reason: Reinsertion is a new insertion event in order tracking.

8. Compare merge styles: `update`, `|`, and `{**d1, **d2}`.
Answer: `update`, `|`, and `{**d1, **d2}` all let right-side duplicates win.
Reason: Later mapping assignments overwrite existing key values.

9. What are dictionary view objects? Why are they called dynamic?
Answer: `keys()`, `values()`, `items()` are live view objects.
Reason: They reflect current dictionary state, not a frozen snapshot.

10. How do you safely delete keys while iterating?
Answer: Iterate over `list(d.keys())` (or collected keys) before deleting.
Reason: Direct size mutation during dict iteration raises `RuntimeError`.

11. When should you use `setdefault` vs `defaultdict`?
Answer: Use `setdefault` for quick inline grouping; use `defaultdict` for heavy repeated missing-key flows.
Reason: `defaultdict` reduces boilerplate and often improves clarity in loops.

12. When is `Counter` better than manual frequency dictionaries?
Answer: Use `Counter` when task is counting/top-k frequency.
Reason: It provides optimized counting APIs like `most_common`.

13. How does `ChainMap` work, and where is it useful?
Answer: `ChainMap` provides layered lookup across mappings (first map has priority).
Reason: Useful for defaults-overrides configuration patterns.

14. What does `MappingProxyType` solve in API/config design?
Answer: `MappingProxyType` gives a read-only view of a mutable source dict.
Reason: Safe exposure of config/state without allowing writes.

15. Why can duplicate values break one-line dictionary inversion?
Answer: Duplicate original values collide when inverted into keys.
Reason: Dict keys must be unique, so later assignments overwrite earlier ones.

16. Explain dictionary dispatch pattern and a real use-case.
Answer: Dispatch maps operation tokens to callables (e.g., `{: add}`).
Reason: It replaces long `if/elif` chains with O(1)-style key lookup.

17. Explain memoization with dictionary using Fibonacci-like recurrence.
Answer: Memoization stores computed results in dict and reuses them.
Reason: Repeated subproblems become constant-time lookups.

18. Why are dictionaries common in graph adjacency lists and sparse matrices?
Answer: Dicts handle sparse/non-contiguous keys naturally for adjacency/sparse matrices.
Reason: You store only present entries instead of dense contiguous arrays.

19. Discuss complexity of key membership vs value membership.
Answer: `key in d` is average O(1), while `value in d.values()` is O(n).
Reason: Keys are hashed; value membership scans values.

20. Explain key equality edge cases (`1`, `True`, `1.0`) and impact.
Answer: `1`, `True`, and `1.0` compare equal and hash compatibly, so they share one key slot.
Reason: Later assignment overwrites earlier value for that equivalent key.

21. What are common runtime errors with dictionaries and how to prevent them?
Answer: Common errors are `KeyError`, `RuntimeError` (size change during iteration), and `TypeError` (unhashable key).
Reason: Use `get/pop default`, safe iteration patterns, and hashable keys to prevent them.

22. How would you justify dictionary choice vs list/tuple/set in a problem?
Answer: Choose dict when you need fast key-based retrieval, grouping, counting, sparse mapping.
Reason: Lists/tuples are index-based; sets store keys only (no values).

23. What memory trade-offs exist for large dictionaries?
Answer: Dicts trade memory for speed due to hashing tables and object overhead.
Reason: Large mappings can be RAM-heavy compared with compact arrays/tuples.

24. What interview pitfalls appear in nested dictionaries and mutable defaults?
Answer: Major pitfalls: shared mutable defaults, shallow-copy surprises, inversion overwrite, unsafe mutation in iteration.
Reason: These cause subtle bugs that pass simple happy-path tests.

25. Give an interview-ready checklist for dict-heavy solutions (correctness + complexity + edge cases).
Answer: Checklist: handle missing keys, edge cases, copy semantics, ordering assumptions, and complexity claims.
Reason: Interview evaluation rewards both correctness and reasoning quality.

