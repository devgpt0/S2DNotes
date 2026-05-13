# Python Dictionary Worksheet

## Level 1

### Tricky Predict the Output (50)

1.
```python
student = {"name": "Ad", "age": 22}
print(type(student).__name__)
print(student["name"])
```

Answer: _____________

2.
```python
d = dict()
print(d)
```

Answer: _____________

3.
```python
d = dict(name="Ad", age=22)
print(d)
```

Answer: _____________

4.
```python
d = dict([("a", 1), ("b", 2)])
print(d["b"])
```

Answer: _____________

5.
```python
sq = {x: x * x for x in range(4)}
print(sq)
```

Answer: _____________

6.
```python
d = {"x": 10, "y": 20}
print(d["x"])
```

Answer: _____________

7.
```python
d = {"x": 10}
print(d.get("z"))
print(d.get("z", 0))
```

Answer: _____________

8.
```python
d = {"x": 10}
try:
    print(d["z"])
except KeyError:
    print("KeyError")
```

Answer: _____________

9.
```python
d = {}
d["name"] = "Ad"
print(d)
```

Answer: _____________

10.
```python
d = {"name": "Ad"}
d["name"] = "AI Engineer"
print(d)
```

Answer: _____________

11.
```python
d = {"a": 1}
d.update({"b": 2, "c": 3})
print(d)
```

Answer: _____________

12.
```python
d1 = {"a": 1, "x": 10}
d2 = {"b": 2, "x": 99}
print(d1 | d2)
```

Answer: _____________

13.
```python
d1 = {"a": 1}
d1 |= {"b": 2}
print(d1)
```

Answer: _____________

14.
```python
d = {"a": 1, "b": 2}
print(d.pop("a"))
print(d)
```

Answer: _____________

15.
```python
d = {"a": 1, "b": 2}
print(d.popitem())
print(d)
```

Answer: _____________

16.
```python
d = {"a": 1, "b": 2}
del d["b"]
print(d)
```

Answer: _____________

17.
```python
d = {"a": 1, "b": 2}
d.clear()
print(d)
```

Answer: _____________

18.
```python
d = {"a": 1, "b": 2}
print(list(d.keys()))
```

Answer: _____________

19.
```python
d = {"a": 1, "b": 2}
print(list(d.values()))
```

Answer: _____________

20.
```python
d = {"a": 1, "b": 2}
print(list(d.items()))
```

Answer: _____________

21.
```python
d = {"a": 1}
print(d.setdefault("a", 100))
print(d)
```

Answer: _____________

22.
```python
d = {"a": 1}
print(d.setdefault("b", 100))
print(d)
```

Answer: _____________

23.
```python
keys = ["x", "y", "z"]
d = dict.fromkeys(keys, 0)
print(d)
```

Answer: _____________

24.
```python
d = dict.fromkeys(["a", "b"], [])
d["a"].append(1)
print(d)
```

Answer: _____________

25.
```python
d = {"a": 1}
print("a" in d, 1 in d)
```

Answer: _____________

26.
```python
d = {"a": 1, "b": 2}
for k in d:
    print(k, end=" ")
print()
```

Answer: _____________

27.
```python
d = {"a": 1, "b": 2}
for v in d.values():
    print(v, end=" ")
print()
```

Answer: _____________

28.
```python
d = {"a": 1, "b": 2}
for k, v in d.items():
    print(k, v)
```

Answer: _____________

29.
```python
d = {"a": 1, "b": 2, "c": 3}
for k in reversed(d):
    print(k, end=" ")
print()
```

Answer: _____________

30.
```python
d = {"a": 1}
k = d.keys()
print(k)
d["b"] = 2
print(k)
```

Answer: _____________

31.
```python
d1 = {"a": 1, "b": 2}
d2 = {"b": 3, "c": 4}
print(d1.keys() & d2.keys())
```

Answer: _____________

32.
```python
even_sq = {x: x * x for x in range(6) if x % 2 == 0}
print(even_sq)
```

Answer: _____________

33.
```python
d = {"a": 1, "b": 2}
rev = {v: k for k, v in d.items()}
print(rev)
```

Answer: _____________

34.
```python
d = {"a": 1, "b": 1}
rev = {v: k for k, v in d.items()}
print(rev)
```

Answer: _____________

35.
```python
students = {101: {"name": "Ad", "age": 22}}
print(students[101]["name"])
```

Answer: _____________

36.
```python
students = {101: {"name": "Ad", "age": 22}}
students[101]["age"] = 23
print(students)
```

Answer: _____________

37.
```python
d1 = {"a": [1, 2]}
d2 = d1.copy()
d2["a"].append(3)
print(d1)
print(d2)
```

Answer: _____________

38.
```python
import copy

d1 = {"a": [1, 2]}
d2 = copy.deepcopy(d1)
d2["a"].append(3)
print(d1)
print(d2)
```

Answer: _____________

39.
```python
d = {"a": 1}
print(d.pop("x", 999))
print(d)
```

Answer: _____________

40.
```python
d = {"a": 1}
try:
    d.pop("x")
except KeyError:
    print("KeyError")
```

Answer: _____________

41.
```python
arr = [1, 1, 2, 3, 2, 1]
freq = {}
for x in arr:
    freq[x] = freq.get(x, 0) + 1
print(freq)
```

Answer: _____________

42.
```python
words = ["cat", "car", "dog"]
groups = {}
for w in words:
    groups.setdefault(w[0], []).append(w)
print(groups)
```

Answer: _____________

43.
```python
from collections import defaultdict

d = defaultdict(int)
d["a"] += 1
d["a"] += 1
print(dict(d))
```

Answer: _____________

44.
```python
from collections import defaultdict

d = defaultdict(list)
d["c"].append("cat")
d["c"].append("car")
print(dict(d))
```

Answer: _____________

45.
```python
from collections import Counter

c = Counter([1, 1, 2, 2, 2, 3])
print(c)
```

Answer: _____________

46.
```python
from collections import Counter

c = Counter([1, 1, 2, 2, 2, 3])
print(c.most_common(1))
```

Answer: _____________

47.
```python
from collections import ChainMap

c = ChainMap({"theme": "light"}, {"theme": "dark", "lang": "en"})
print(c["theme"], c["lang"])
```

Answer: _____________

48.
```python
from types import MappingProxyType

d = {"a": 1}
proxy = MappingProxyType(d)
print(proxy["a"])
d["a"] = 10
print(proxy["a"])
```

Answer: _____________

49.
```python
d = {"a": 1, "b": 2}
for k in list(d.keys()):
    del d[k]
print(d)
```

Answer: _____________

50.
```python
d = {"a": 1, "b": 2}
try:
    for k in d:
        del d[k]
except RuntimeError as e:
    print(type(e).__name__)
```

Answer: _____________

### MCQ Theory (50)

1. A dictionary is primarily a:
```text
A) key-value mapping
B) sequence only
C) stack
D) queue
```

2. Dictionary lookup average complexity is:
```text
A) O(1)
B) O(log n)
C) O(n)
D) O(n log n)
```

3. Which syntax creates an empty dictionary?
```text
A) {}
B) []
C) ()
D) set()
```

4. `d[key]` on missing key:
```text
A) KeyError
B) None
C) -1
D) ValueError
```

5. `d.get(key)` on missing key returns:
```text
A) None by default
B) KeyError
C) empty string
D) False always
```

6. `d.get(key, default)` is used for:
```text
A) safe optional lookup
B) deletion
C) sorting
D) deep copy
```

7. Keys in dictionary must be:
```text
A) hashable
B) mutable only
C) numeric only
D) list only
```

8. Which is a valid key?
```text
A) (1, 2)
B) [1, 2]
C) {1, 2}
D) {"a": 1}
```

9. Which is invalid as key?
```text
A) list
B) string
C) int
D) tuple of ints
```

10. `update()` does:
```text
A) merge/overwrite keys
B) removes all keys
C) sorts keys
D) freezes dict
```

11. In `d1 | d2`, duplicate key value comes from:
```text
A) d2
B) d1
C) both as list
D) random side
```

12. `pop(k)` returns:
```text
A) removed value
B) removed key
C) bool
D) None always
```

13. `popitem()` removes:
```text
A) last inserted key-value pair
B) first inserted pair
C) random pair always
D) all pairs
```

14. `clear()` does:
```text
A) empties dictionary in-place
B) deletes variable name
C) creates new dict
D) sorts dict
```

15. `keys()` returns:
```text
A) dynamic view object
B) list copy always
C) tuple copy
D) set copy always
```

16. Membership test `x in d` checks:
```text
A) keys
B) values
C) items tuples
D) both keys and values
```

17. Iterating directly over dict yields:
```text
A) keys
B) values
C) items
D) indices
```

18. `items()` gives:
```text
A) key-value pair view
B) keys only
C) values only
D) list always
```

19. `setdefault(k, v)` when key exists:
```text
A) keeps existing value
B) overwrites with v
C) removes key
D) raises error
```

20. `setdefault(k, v)` when key missing:
```text
A) inserts key with v
B) returns None only
C) raises KeyError
D) deletes key
```

21. `dict.fromkeys(keys, val)` with mutable `val` can cause:
```text
A) shared reference pitfall
B) syntax error
C) TypeError always
D) automatic deep copy
```

22. Shallow copy of dict with nested list means:
```text
A) nested list reference shared
B) full deep clone
C) immutable clone
D) key hashing disabled
```

23. Deep copy ensures:
```text
A) nested objects independent
B) same nested refs
C) no new object
D) key order shuffled
```

24. Dictionary comprehension creates:
```text
A) new dictionary
B) new list
C) new tuple
D) generator only
```

25. `for k, v in d.items()` iterates over:
```text
A) key-value pairs
B) keys only
C) values only
D) indexes
```

26. Reverse iteration of dict follows:
```text
A) reverse insertion order
B) sorted key order
C) random order
D) value order
```

27. Which statement about dict order is correct?
```text
A) insertion order is preserved
B) always random
C) sorted by key automatically
D) sorted by value automatically
```

28. Heavy collision cases can degrade lookup to:
```text
A) O(n)
B) O(log n)
C) O(1/2)
D) O(n log n)
```

29. `defaultdict(int)` missing key returns default:
```text
A) 0
B) 1
C) None
D) ""
```

30. `defaultdict(list)` missing key returns:
```text
A) new empty list
B) shared global list
C) None
D) tuple
```

31. `Counter` is best suited for:
```text
A) frequency counting
B) matrix transpose
C) sorting only
D) key hashing customization
```

32. `Counter.most_common(1)` returns:
```text
A) top frequency pair list
B) top key only
C) count only
D) bool
```

33. `ChainMap` lookup priority is:
```text
A) left to right mappings
B) right to left mappings
C) random
D) by key length
```

34. `MappingProxyType` provides:
```text
A) read-only dictionary view
B) deep copy dict
C) encrypted dict
D) sorted dict
```

35. Modifying dict size during iteration may raise:
```text
A) RuntimeError
B) IndexError
C) AttributeError
D) ImportError
```

36. Safe deletion while iterating usually uses:
```text
A) list(d.keys())
B) d directly
C) d.values() directly
D) d.items() directly without copy
```

37. Best pattern for frequency in loop:
```text
A) d[x] = d.get(x, 0) + 1
B) d[x] += 1 without check always
C) d.append(x)
D) d.extend(x)
```

38. Inverting dict with duplicate values causes:
```text
A) overwrite collisions
B) syntax error
C) automatic list grouping
D) key deep copy
```

39. Complexity of iterating all items is:
```text
A) O(n)
B) O(1)
C) O(log n)
D) O(n^2)
```

40. A dictionary is generally implemented using:
```text
A) hash table concepts
B) linked list only
C) binary tree only
D) stack array only
```

41. `d.copy()` returns:
```text
A) shallow copy
B) deep copy
C) no copy
D) read-only proxy
```

42. `del d[k]` on missing key raises:
```text
A) KeyError
B) ValueError
C) TypeError
D) RuntimeError
```

43. `pop(k, default)` on missing key returns:
```text
A) default
B) KeyError always
C) None always
D) False always
```

44. Which is best for grouping words by first character?
```text
A) setdefault/defaultdict(list)
B) list sort only
C) tuple packing only
D) set membership only
```

45. `keys()` and `values()` views are:
```text
A) dynamic
B) immutable snapshots
C) always lists
D) always tuples
```

46. Which data structure supports sparse key mapping naturally?
```text
A) dict
B) list
C) tuple
D) string
```

47. To avoid accidental mutation sharing in nested structures use:
```text
A) deepcopy when needed
B) aliasing
C) fromkeys with []
D) only update
```

48. `in` on `d.values()` complexity is typically:
```text
A) O(n)
B) O(1)
C) O(log n)
D) O(n log n)
```

49. Which statement is true about `Counter`?
```text
A) it is a dict subclass for counts
B) it stores only unique keys without counts
C) it cannot handle strings
D) it cannot be updated
```

50. Which is interview-friendly dict checklist?
```text
A) key existence, edge cases, copy behavior, complexity
B) memorize only syntax
C) avoid testing
D) ignore missing keys
```

## Level 2

### Tricky Predict the Output (50)

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

Answer: _____________

2.
```python
try:
    d = {(1, [2, 3]): "x"}
except TypeError as e:
    print(type(e).__name__)
```

Answer: _____________

3.
```python
d = {frozenset([1, 2]): "ok"}
print(d[frozenset([2, 1])])
```

Answer: _____________

4.
```python
d = {x: ("even" if x % 2 == 0 else "odd") for x in range(5)}
print(d)
```

Answer: _____________

5.
```python
keys = ["a", "b", "c"]
vals = [10, 20, 30]
print(dict(zip(keys, vals)))
```

Answer: _____________

6.
```python
d1 = {"a": 1}
d2 = {"b": 2}
d3 = {"a": 9}
print(d1 | d2 | d3)
```

Answer: _____________

7.
```python
d = {"a": 1}
out = d.update({"b": 2})
print(out)
print(d)
```

Answer: _____________

8.
```python
d1 = {"a": [1]}
d2 = d1.copy()
print(d1 is d2)
print(d1["a"] is d2["a"])
```

Answer: _____________

9.
```python
import copy

d1 = {"a": [1]}
d2 = copy.deepcopy(d1)
print(d1 is d2)
print(d1["a"] is d2["a"])
```

Answer: _____________

10.
```python
d1 = {"a": 1, "b": 2, "c": 3}
d2 = {"b": 9}
print(d1.keys() - d2.keys())
```

Answer: _____________

11.
```python
d1 = {"a": 1, "b": 2}
d2 = {"b": 9, "c": 3}
print(d1.keys() | d2.keys())
```

Answer: _____________

12.
```python
d = {"a": 1, "b": 2}
print(("a", 1) in d.items())
print(("a", 2) in d.items())
```

Answer: _____________

13.
```python
d = {"x": 1, "y": 2}
d["x"] = 100
print(d.popitem())
```

Answer: _____________

14.
```python
d = {"a": 1, "b": 2, "c": 3}
del d["b"]
d["b"] = 20
print(list(d.keys()))
```

Answer: _____________

15.
```python
d = {"a": 3, "b": 1, "c": 2}
out = dict(sorted(d.items(), key=lambda x: x[1]))
print(out)
```

Answer: _____________

16.
```python
d = {"a": 3, "b": 1, "c": 2}
out = dict(sorted(d.items(), key=lambda x: x[0], reverse=True))
print(out)
```

Answer: _____________

17.
```python
def add(a, b):
    return a + b

def sub(a, b):
    return a - b

ops = {"+": add, "-": sub}
print(ops["+"](10, 3), ops["-"](10, 3))
```

Answer: _____________

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

Answer: _____________

19.
```python
edges = [(1, 2), (1, 3), (2, 4)]
graph = {}
for u, v in edges:
    graph.setdefault(u, []).append(v)
print(graph)
```

Answer: _____________

20.
```python
arr = ["a", "b", "a", "c", "b", "a"]
freq = {}
for x in arr:
    freq[x] = freq.get(x, 0) + 1
print(freq)
```

Answer: _____________

21.
```python
from collections import Counter

arr = ["a", "b", "a", "c", "b", "a"]
print(Counter(arr) == {"a": 3, "b": 2, "c": 1})
```

Answer: _____________

22.
```python
from collections import ChainMap

defaults = {"theme": "dark", "lang": "en"}
user = {"theme": "light"}
c = ChainMap(user, defaults)
print(c["theme"], c["lang"])
```

Answer: _____________

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

Answer: _____________

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

Answer: _____________

25.
```python
class ZeroDict(dict):
    def __missing__(self, key):
        return 0

d = ZeroDict()
print(d["x"])
print(d.get("y"))
```

Answer: _____________

26.
```python
d = {"a": 1}
v = d.values()
print(v)
d["b"] = 2
print(v)
```

Answer: _____________

27.
```python
d = {"a": 1, "b": 2, "c": 3}
print({"a", "b"}.issubset(d.keys()))
```

Answer: _____________

28.
```python
d1 = {"a": 1, "b": 2}
d2 = {"b": 9, "c": 3}
print({**d1, **d2})
```

Answer: _____________

29.
```python
matrix = {}
matrix[(1, 2)] = 10
matrix[(2, 1)] = 20
print(matrix[(1, 2)], matrix[(2, 1)])
```

Answer: _____________

30.
```python
d = dict.fromkeys(["p", "q"])
print(d)
```

Answer: _____________

31.
```python
d = {"a": 1}
print(d.get("a", 100))
print(d.get("b", 100))
```

Answer: _____________

32.
```python
d = {"a": 1, "b": 2, "c": 3}
print({k: v for k, v in d.items() if v % 2 == 1})
```

Answer: _____________

33.
```python
d = {"a": 10, "b": 20}
print(sum(d.values()))
```

Answer: _____________

34.
```python
d = {"a": 1}
print(bool(d))
d.clear()
print(bool(d))
```

Answer: _____________

35.
```python
d = {"a": 1, "b": 2}
print(min(d), max(d))
```

Answer: _____________

36.
```python
d = {"a": 1, "b": 2}
print(sorted(d))
```

Answer: _____________

37.
```python
d = {"x": 1, "y": 2}
print(list(d.items())[0])
```

Answer: _____________

38.
```python
d = {"x": 1, "y": 2, "z": 3}
print(next(iter(d)))
```

Answer: _____________

39.
```python
from collections import defaultdict

d = defaultdict(set)
for ch in "banana":
    d[ch].add(ch.upper())
print({k: sorted(v) for k, v in d.items()})
```

Answer: _____________

40.
```python
from collections import Counter

c = Counter("aabccc")
c.update("cc")
print(c)
```

Answer: _____________

41.
```python
from collections import Counter

c = Counter([1, 1, 2, 3])
c.subtract([1, 3])
print(c)
```

Answer: _____________

42.
```python
d = {"a": 1, "b": 2}
d["c"] = 3
d.pop("b")
d["b"] = 20
print(list(d.keys()))
```

Answer: _____________

43.
```python
d = {"a": 1}
d.clear()
d["x"] = 9
print(d)
```

Answer: _____________

44.
```python
d1 = {"a": 1}
d2 = d1.copy()
d2["b"] = 2
print(d1)
print(d2)
```

Answer: _____________

45.
```python
d1 = {"a": [1]}
d2 = d1.copy()
d2["a"][0] = 99
print(d1)
```

Answer: _____________

46.
```python
d = {"a": None}
print(d.get("a", 100))
print(d.get("b", 100))
```

Answer: _____________

47.
```python
d = {"a": 1, "b": 2}
k = d.keys()
print("a" in k)
d.pop("a")
print("a" in k)
```

Answer: _____________

48.
```python
d = {"a": 3, "b": 1, "c": 2}
print(sorted(d.items(), key=lambda kv: kv[1], reverse=True))
```

Answer: _____________

49.
```python
d = {}
d[1] = "int"
d[True] = "bool"
print(d)
print(len(d))
```

Answer: _____________

50.
```python
d = {}
d[1] = "int"
d[1.0] = "float"
print(d)
print(len(d))
```

Answer: _____________

### MCQ Theory (50)

1. In interview coding, the most common dict use-case is:
```text
A) frequency counting/grouping
B) image rendering
C) thread scheduling
D) socket binding
```

2. Why is dict lookup called amortized O(1)?
```text
A) occasional costly resize but average constant-time operations
B) always exactly one CPU instruction
C) never resizes
D) tree balancing cost
```

3. High collision scenarios may cause:
```text
A) performance degradation
B) automatic syntax failure
C) key type conversion
D) key sorting
```

4. Best key choice for stable behavior is usually:
```text
A) immutable and simple types
B) mutable list
C) mutable set
D) nested dict
```

5. Which statement about `dict.get()` is correct?
```text
A) does not raise KeyError for missing key
B) always inserts missing key
C) deletes missing key
D) sorts by key before returning
```

6. Which method can raise KeyError if key missing (without default)?
```text
A) pop
B) get
C) values
D) keys
```

7. `setdefault` is commonly preferred for:
```text
A) grouping/appending patterns
B) sorting
C) deleting duplicates
D) reversing dict
```

8. `defaultdict(list)` is useful because:
```text
A) missing keys auto-create empty lists
B) it is immutable
C) it sorts keys automatically
D) it avoids hashing
```

9. `defaultdict(int)` count pattern avoids:
```text
A) explicit missing-key checks
B) iteration
C) hashing
D) memory allocation
```

10. `Counter` differs from plain dict mainly by:
```text
A) built-in counting helpers (`most_common`, updates)
B) immutable keys only
C) sorted output always
D) no dict behavior
```

11. `Counter.subtract()` can produce:
```text
A) zero/negative counts
B) KeyError always
C) only positive counts
D) list output
```

12. `ChainMap` write operations affect:
```text
A) first mapping only
B) all mappings
C) last mapping only
D) none
```

13. `MappingProxyType` is mainly used to:
```text
A) expose read-only views safely
B) deep clone dict
C) speed hashing only
D) auto-persist changes to disk
```

14. `__missing__` hook is triggered by:
```text
A) direct indexing on missing key
B) `get()` always
C) `in` operator
D) `.keys()`
```

15. Which operation is unsafe during direct dict iteration?
```text
A) changing dictionary size
B) reading values
C) printing keys
D) checking membership
```

16. Safe mutation while iterating typically uses:
```text
A) iteration over copied key list
B) direct dict iteration
C) recursion only
D) sorted views only
```

17. In `{**d1, **d2}`, duplicate keys resolve by:
```text
A) right-most mapping wins
B) left-most mapping wins
C) both stored as tuple
D) runtime error
```

18. Invert dict with duplicate values usually needs:
```text
A) value-to-list grouping logic
B) direct one-line invert only
C) no hashing
D) tuple sorting
```

19. Which is true for dictionary views?
```text
A) they are dynamic/live
B) they are frozen snapshots
C) they are always lists
D) they cannot do set operations
```

20. Which view supports set-like intersections naturally?
```text
A) keys view
B) values view only
C) string representation
D) repr output
```

21. Best way to test key presence before heavy processing:
```text
A) `if key in d:`
B) `if key in d.values():`
C) `if key in d.items():`
D) `if d[key]:`
```

22. Why can `1` and `True` collide as keys?
```text
A) they compare equal and share hash behavior
B) dictionaries sort bool first
C) bool cannot be dict key
D) int cannot be dict key
```

23. Why can `1` and `1.0` collapse into one key?
```text
A) equal numeric keys hash/compare equal
B) float keys are converted to strings
C) int keys are deleted
D) dictionary forbids mixed numeric types
```

24. Recommended strategy for nested independent copy:
```text
A) `copy.deepcopy`
B) `d.copy()`
C) `dict(d)`
D) alias assignment
```

25. For sparse matrices/graphs, dict is useful due to:
```text
A) flexible non-contiguous keys
B) index-only contiguous storage
C) immutable values requirement
D) automatic sorting by edge weight
```

26. Dictionary dispatch pattern maps:
```text
A) operation tokens to callables
B) values to indices only
C) exceptions to files
D) loops to recursion
```

27. Memoization with dict improves recursion by:
```text
A) caching repeated subproblem results
B) reducing function parameters
C) avoiding base cases
D) sorting calls
```

28. Which statement about `update()` return value is true?
```text
A) returns None (in-place mutation)
B) returns new dict
C) returns bool
D) returns updated key count
```

29. Best interview explanation for dict speed should include:
```text
A) hashing + average probe behavior
B) linked-list traversal only
C) binary search tree depth
D) constant memory guarantee
```

30. Frequency count one-liner inside loop:
```text
A) `freq[x] = freq.get(x, 0) + 1`
B) `freq += 1`
C) `freq.append(x)`
D) `freq[x].add(1)`
```

31. Which operation is O(n) typically?
```text
A) full dict iteration
B) single key lookup
C) single key insert average-case
D) single key delete average-case
```

32. Which check scans values linearly?
```text
A) `target in d.values()`
B) `target in d`
C) `d.get(target)`
D) `d[target]` (when present)
```

33. For grouping words by first letter, best pair is:
```text
A) `defaultdict(list)` + append
B) list sorting only
C) tuple indexing only
D) set subtraction
```

34. For immutable public config exposure, choose:
```text
A) `MappingProxyType`
B) plain dict alias
C) list of tuples only
D) mutable global dict directly
```

35. Which statement is true for dict membership complexity?
```text
A) key membership is average O(1)
B) key membership is always O(n)
C) value membership is O(1)
D) membership unsupported
```

36. If two mappings are chained via `ChainMap(a, b)`, lookup order is:
```text
A) `a` then `b`
B) `b` then `a`
C) random
D) sorted by key
```

37. Which is a clean approach for top-k frequent elements?
```text
A) `Counter(...).most_common(k)`
B) `set(...).pop()` repeated
C) random shuffle
D) nested loops only
```

38. Why avoid `dict.fromkeys(keys, [])` in production code?
```text
A) shared mutable default causes bugs
B) syntax invalid
C) too slow to build
D) cannot store lists
```

39. Which method gives pair tuples view?
```text
A) `items()`
B) `values()`
C) `keys()`
D) `get()`
```

40. Which is true about dictionary ordering behavior?
```text
A) it reflects insertion sequence
B) always sorted alphabetically
C) random each run
D) reverse insertion always
```

41. In interview constraints, when dict memory is high, common alternatives include:
```text
A) arrays/tuples/specialized structures where possible
B) using deeper nesting always
C) converting everything to strings
D) disabling hashing
```

42. Why is `get()` often more readable in counting code?
```text
A) combines missing-key default with retrieval
B) performs deep copy
C) skips hashing
D) orders keys
```

43. Which method is best to remove and return an arbitrary-like latest pair quickly?
```text
A) `popitem()`
B) `remove()`
C) `discard()`
D) `extract()`
```

44. Which code can preserve key order while deduping stream with last value wins?
```text
A) plain dict assignment by key
B) set conversion only
C) tuple conversion only
D) list slicing only
```

45. `dict` as adjacency list usually maps:
```text
A) node -> list of neighbors
B) edge -> fixed tuple only
C) index -> boolean only
D) path -> sorted set always
```

46. Why should explanation include worst-case O(n) even if average is O(1)?
```text
A) interviewers expect collision/pathological case awareness
B) average case is invalid
C) dict never hashes
D) complexity not relevant
```

47. Which is true about shallow copy + nested mutable values?
```text
A) inner mutations reflect in both dictionaries
B) both dictionaries fully isolated
C) shallow copy forbids mutation
D) all keys become immutable
```

48. For a read-mostly layered config, good pattern is:
```text
A) `ChainMap(user, defaults)`
B) deleting defaults each read
C) converting to list each access
D) global try/except blocks only
```

49. In coding tests, safest missing-key strategy for optional read is:
```text
A) `get` with explicit default
B) direct indexing always
C) `del` then read
D) `popitem`
```

50. Best final check before submitting dict-based solution:
```text
A) verify collisions in logic, missing keys, mutable defaults, complexity claims
B) remove all edge-case tests
C) replace dict with list blindly
D) ignore order assumptions
```

## Interview Theory (Top 25)

1. Explain why dictionary keys must be immutable and hashable.
2. Compare `d[key]` vs `d.get(key, default)` with failure behavior.
3. Why is dictionary lookup average O(1)? Why not guaranteed O(1)?
4. Explain collision handling conceptually in hash-table-backed mappings.
5. Difference between shallow copy and deep copy in nested dictionaries.
6. Why does `dict.fromkeys(keys, [])` cause shared-state bugs?
7. Explain insertion order behavior and how delete+reinsert affects order.
8. Compare merge styles: `update`, `|`, and `{**d1, **d2}`.
9. What are dictionary view objects? Why are they called dynamic?
10. How do you safely delete keys while iterating?
11. When should you use `setdefault` vs `defaultdict`?
12. When is `Counter` better than manual frequency dictionaries?
13. How does `ChainMap` work, and where is it useful?
14. What does `MappingProxyType` solve in API/config design?
15. Why can duplicate values break one-line dictionary inversion?
16. Explain dictionary dispatch pattern and a real use-case.
17. Explain memoization with dictionary using Fibonacci-like recurrence.
18. Why are dictionaries common in graph adjacency lists and sparse matrices?
19. Discuss complexity of key membership vs value membership.
20. Explain key equality edge cases (`1`, `True`, `1.0`) and impact.
21. What are common runtime errors with dictionaries and how to prevent them?
22. How would you justify dictionary choice vs list/tuple/set in a problem?
23. What memory trade-offs exist for large dictionaries?
24. What interview pitfalls appear in nested dictionaries and mutable defaults?
25. Give an interview-ready checklist for dict-heavy solutions (correctness + complexity + edge cases).