# Python List Worksheet

Source: python/notes/collection_framework/list.md

## Level 1

### Tricky Predict the Output (50)

1.
```python
a = [10, 20, 30, 40, 50]
print(a[0], a[-1])
```

Answer: _____________

2.
```python
a = [10, 20, 30, 40, 50]
print(a[1:4])
```

Answer: _____________

3.
```python
a = [10, 20, 30, 40, 50]
print(a[:3])
```

Answer: _____________

4.
```python
a = [10, 20, 30, 40, 50]
print(a[2:])
```

Answer: _____________

5.
```python
a = [10, 20, 30, 40, 50]
print(a[::-1])
```

Answer: _____________

6.
```python
a = [10, 20, 30, 40, 50]
print(a[::2])
```

Answer: _____________

7.
```python
a = [10, 20, 30, 40, 50]
print(a[1::2])
```

Answer: _____________

8.
```python
a = [10, 20, 30, 40, 50]
print(a[-3:])
```

Answer: _____________

9.
```python
a = [10, 20, 30, 40, 50]
print(a[3:100])
```

Answer: _____________

10.
```python
a = ['a', 'b', 'c', 'd']
print(a[-4], a[-2])
```

Answer: _____________

11.
```python
a = [1, 2, 3, 4, 5, 6]
print(a[5:1:-2])
```

Answer: _____________

12.
```python
a = [1, 2, 3, 4, 5, 6]
print(a[-2::-2])
```

Answer: _____________

13.
```python
a = [1, 2, 3, 4, 5]
print(a[:])
```

Answer: _____________

14.
```python
a = [1, 2, 3, 4, 5]
print(a[:: -2])
```

Answer: _____________

15.
```python
a = [1, 2, 3, 4, 5]
print(a[1:1])
```

Answer: _____________

16.
```python
a = ['apple', 'banana', 'cherry']
a[1] = 'blueberry'
print(a)
```

Answer: _____________

17.
```python
a = ['apple', 'banana', 'cherry']
a[1:3] = ['pear', 'kiwi']
print(a)
```

Answer: _____________

18.
```python
a = [1, 2, 3]
a.append(4)
print(a)
```

Answer: _____________

19.
```python
a = [1, 2]
a.append([3, 4])
print(a)
```

Answer: _____________

20.
```python
a = [1, 2]
a.extend([3, 4])
print(a)
```

Answer: _____________

21.
```python
a = [1, 2, 3]
a.insert(1, 99)
print(a)
```

Answer: _____________

22.
```python
a = ['x', 'y', 'z']
a.remove('y')
print(a)
```

Answer: _____________

23.
```python
a = ['x', 'y', 'z']
print(a.pop())
print(a)
```

Answer: _____________

24.
```python
a = ['x', 'y', 'z']
print(a.pop(0))
print(a)
```

Answer: _____________

25.
```python
a = [1, 2, 3, 4]
del a[1]
print(a)
```

Answer: _____________

26.
```python
a = [1, 2, 3, 4, 5]
del a[1:4]
print(a)
```

Answer: _____________

27.
```python
a = [1, 2, 3]
a.clear()
print(a)
```

Answer: _____________

28.
```python
a = [1, 2, 3]
print(a.count(2), a.index(3))
```

Answer: _____________

29.
```python
a = ['apple', 'banana', 'apple', 'orange']
print(a.index('apple', 1))
```

Answer: _____________

30.
```python
a = [1, 2, 3]
print(2 in a, 9 not in a)
```

Answer: _____________

31.
```python
a = [1, 2, 3]
b = a
b.append(4)
print(a, b)
```

Answer: _____________

32.
```python
a = [1, 2, 3]
b = a[:]
b[0] = 99
print(a, b)
```

Answer: _____________

33.
```python
a = [[1, 2], [3, 4]]
b = a[:]
b[0][0] = 99
print(a)
```

Answer: _____________

34.
```python
import copy
a = [[1, 2], [3, 4]]
b = copy.deepcopy(a)
b[0][0] = 99
print(a)
print(b)
```

Answer: _____________

35.
```python
a = [1, 2, 3]
b = [4, 5]
print(a + b)
```

Answer: _____________

36.
```python
a = [1, 2, 3]
print(a * 2)
```

Answer: _____________

37.
```python
a = [1, 2]
b = [3]
a += b
print(a)
```

Answer: _____________

38.
```python
a = [1, 2]
b = [3]
a = a + b
print(a)
```

Answer: _____________

39.
```python
a = [1, 2, 3]
print(len(a), min(a), max(a), sum(a))
```

Answer: _____________

40.
```python
names = ['Alice', 'Bob', 'Charlie']
print(min(names), max(names))
```

Answer: _____________

41.
```python
a = [3, 1, 2]
a.sort()
print(a)
```

Answer: _____________

42.
```python
a = [3, 1, 2]
print(sorted(a))
print(a)
```

Answer: _____________

43.
```python
a = [-10, 5, -3, 2, -1]
a.sort(key=abs)
print(a)
```

Answer: _____________

44.
```python
a = [-10, 5, -3, 2, -1]
a.sort(key=abs, reverse=True)
print(a)
```

Answer: _____________

45.
```python
a = [1, 2, 3]
a.reverse()
print(a)
```

Answer: _____________

46.
```python
a = [1, 2, 3]
print(list(reversed(a)))
print(a)
```

Answer: _____________

47.
```python
a = ['Alice', 'ALice', 'Charlie']
a.sort(key=str.lower, reverse=True)
print(a)
```

Answer: _____________

48.
```python
a = [10, 20, 30]
for x in a:
    print(x, end=' ')
print()
```

Answer: _____________

49.
```python
a = ['x', 'y', 'z']
for i in range(len(a)):
    print(i, a[i])
```

Answer: _____________

50.
```python
a = ['x', 'y', 'z']
for i, v in enumerate(a):
    print(i, v)
```

Answer: _____________

### MCQ Theory (50)

1. Lists in Python are:
```text
A) Ordered and mutable
B) Unordered and immutable
C) Only numeric
D) Key-value only
```

2. Best empty list syntax:
```text
A) []
B) {}
C) ()
D) set()
```

3. `list("Ada")` produces:
```text
A) ['A','d','a']
B) ['Ada']
C) (A,d,a)
D) TypeError
```

4. `list(range(4))` gives:
```text
A) [0,1,2,3]
B) [1,2,3,4]
C) range(4)
D) (0,1,2,3)
```

5. Index `-1` means:
```text
A) last element
B) first element
C) middle element
D) invalid index
```

6. Slicing upper bound in `a[1:4]` is:
```text
A) exclusive
B) inclusive
C) random
D) depends on type
```

7. Out-of-range slicing typically:
```text
A) returns available slice
B) raises IndexError always
C) returns None
D) returns -1
```

8. Out-of-range direct indexing raises:
```text
A) IndexError
B) KeyError
C) ValueError
D) TypeError
```

9. `append(x)` does:
```text
A) adds one item at end
B) adds many items unpacked
C) inserts at start
D) sorts list
```

10. `extend(iterable)` does:
```text
A) adds each iterable item
B) adds iterable as one item
C) removes iterable
D) reverses list
```

11. `insert(i,x)` does:
```text
A) places x before index i
B) replaces index i only
C) appends always
D) removes at i
```

12. `remove(x)` removes:
```text
A) first matching value
B) all matches
C) by index
D) last item
```

13. `pop()` returns and removes:
```text
A) last element by default
B) first element always
C) all elements
D) none
```

14. `del a[i]` is:
```text
A) statement-based deletion
B) list method
C) copy operation
D) sort operation
```

15. `clear()` on list:
```text
A) empties it in-place
B) deletes variable name
C) returns new list
D) makes tuple
```

16. Aliasing `b=a` means:
```text
A) same object reference
B) deep copy
C) shallow copy values only
D) immutable copy
```

17. `a[:]` is commonly used as:
```text
A) shallow copy
B) deep copy
C) tuple conversion
D) set conversion
```

18. Nested list shallow copy risk:
```text
A) inner lists still shared
B) outer list immutable
C) no risk
D) syntax error
```

19. Deep copy module is:
```text
A) copy
B) collections
C) itertools
D) functools
```

20. `a + b` for lists:
```text
A) creates new concatenated list
B) mutates a only
C) mutates b only
D) invalid always
```

21. `a * 3` for list:
```text
A) repeats sequence
B) multiplies numeric elements only
C) sorts thrice
D) dedupes list
```

22. Membership `x in list` is usually:
```text
A) O(n)
B) O(1)
C) O(log n)
D) O(n log n)
```

23. `len([1,2,3,[4]])` equals:
```text
A) 4
B) 3
C) 5
D) 2
```

24. `sorted(lst)` returns:
```text
A) new sorted list
B) None
C) same list object always
D) iterator
```

25. `lst.sort()` returns:
```text
A) None
B) sorted new list
C) iterator
D) bool
```

26. `reverse()` on list:
```text
A) in-place reverse
B) returns reversed copy
C) sorts descending
D) dedupes
```

27. `reversed(lst)` returns:
```text
A) iterator
B) in-place mutation
C) None
D) tuple
```

28. Case-insensitive sort key often:
```text
A) str.lower
B) ord
C) abs
D) sum
```

29. `index(x)` if missing:
```text
A) raises ValueError
B) returns -1
C) returns None
D) raises IndexError
```

30. `count(x)` returns:
```text
A) occurrence frequency
B) first position
C) last position
D) boolean
```

31. `list()` requires input to be:
```text
A) iterable
B) numeric
C) hashable
D) callable
```

32. `list(123)` causes:
```text
A) TypeError
B) ValueError
C) IndexError
D) works to [1,2,3]
```

33. `[[0]*3]*3` pitfall:
```text
A) shared inner references
B) slow only
C) syntax error
D) memory leak
```

34. Safe matrix creation:
```text
A) [[0 for _ in range(3)] for _ in range(3)]
B) [[0]*3]*3
C) [0,0,0]*3
D) list(0)
```

35. `sum([1,2,3])` gives:
```text
A) 6
B) 123
C) TypeError
D) None
```

36. `max(["Alice","Bob"])` uses:
```text
A) lexicographic comparison
B) length only
C) random pick
D) hash order
```

37. `ord("A")` returns:
```text
A) ASCII/Unicode code point integer
B) string
C) bool
D) list
```

38. `append([1,2])` vs `extend([1,2])`:
```text
A) nested vs flattened add
B) same behavior
C) both errors
D) both remove
```

39. `del a[1:3]` does:
```text
A) delete slice range
B) set to None
C) copy slice
D) sort slice
```

40. `a[:: -1]` and `a[::-1]`:
```text
A) both reverse via slicing
B) both invalid
C) first sorts ascending
D) second mutates
```

41. `for x in lst` yields:
```text
A) elements
B) indices
C) tuples(index,value) always
D) dict keys
```

42. `for i in range(len(lst))` yields:
```text
A) indices
B) elements
C) pairs automatically
D) reversed values
```

43. `enumerate(lst)` yields:
```text
A) index-value pairs
B) values only
C) indices only
D) dict items
```

44. Lists can store:
```text
A) mixed datatypes
B) single datatype only
C) numbers only
D) strings only
```

45. List is best described as:
```text
A) dynamic array-like sequence
B) hash map
C) tree
D) stack-only
```

46. `a[1:1]` result is usually:
```text
A) empty list
B) error
C) None
D) index 1 element
```

47. `a[1:100]` with short list:
```text
A) no error slicing
B) IndexError
C) KeyError
D) TypeError
```

48. `copy.deepcopy` is needed when:
```text
A) nested mutable structures must be independent
B) flat list only
C) sorting
D) membership
```

49. Interview best practice for list pitfalls:
```text
A) test aliasing and edge indices explicitly
B) avoid slicing completely
C) never use append
D) always use recursion
```

## Level 2

### Tricky Predict the Output (50)

1.
```python
a = [1, 2, 3, 4]
print([x*x for x in a])
```

Answer: _____________

2.
```python
a = [1, 2, 3, 4]
print([x for x in a if x % 2 == 0])
```

Answer: _____________

3.
```python
a = [1, 2, 3, 4]
print(["even" if x % 2 == 0 else "odd" for x in a])
```

Answer: _____________

4.
```python
a = [1, 2, 3, 4]
print([x*10 for x in a if x > 2])
```

Answer: _____________

5.
```python
a = [1, 2, 3]
print(list(map(lambda x: x + 5, a)))
```

Answer: _____________

6.
```python
a = [1, 2, 3, 4, 5]
print(list(filter(lambda x: x % 2, a)))
```

Answer: _____________

7.
```python
a = [1, 2, 3, 4]
print(any(x > 3 for x in a), all(x > 0 for x in a))
```

Answer: _____________

8.
```python
a = [0, 0, 1]
print(any(a), all(a))
```

Answer: _____________

9.
```python
a = [1, 2, 3]
print(sum(x*x for x in a))
```

Answer: _____________

10.
```python
a = ['apple', 'banana', 'mango']
print(next((x for x in a if x.startswith('m')), None))
```

Answer: _____________

11.
```python
a = ['apple', 'banana', 'mango']
print(next((x for x in a if x.startswith('z')), 'NA'))
```

Answer: _____________

12.
```python
a = [1, 2, 3, 4, 5]
print([i for i, x in enumerate(a) if x % 2 == 1])
```

Answer: _____________

13.
```python
a = [1, 2, 3]
print([*a, 4, 5])
```

Answer: _____________

14.
```python
a = [1, 2]
b = [3, 4]
print([*a, *b])
```

Answer: _____________

15.
```python
a = [1, 2, 3]
first, *mid, last = a
print(first, mid, last)
```

Answer: _____________

16.
```python
a = [1, 2, 3, 4]
*head, tail = a
print(head, tail)
```

Answer: _____________

17.
```python
a = ['1', '2', '3']
print(list(map(int, a)))
```

Answer: _____________

18.
```python
a = [1, 2, 3]
print(list(map(str, a)))
```

Answer: _____________

19.
```python
a = [1, 2, 3, 4]
print([x for x in a if not x % 2])
```

Answer: _____________

20.
```python
a = [1, 2, 3, 4]
print([x for x in a if x % 2])
```

Answer: _____________

21.
```python
m = [[1, 2], [3, 4], [5, 6]]
print([x for row in m for x in row])
```

Answer: _____________

22.
```python
m = [[1, 2], [3, 4], [5, 6]]
print([row[0] for row in m])
```

Answer: _____________

23.
```python
m = [[1, 2, 3], [4, 5, 6]]
print([sum(row) for row in m])
```

Answer: _____________

24.
```python
m = [[1, 2, 3], [4, 5, 6]]
print([m[r][c] for c in range(3) for r in range(2)])
```

Answer: _____________

25.
```python
grid = [[0 for _ in range(2)] for _ in range(2)]
grid[0][0] = 1
print(grid)
```

Answer: _____________

26.
```python
bad = [[0] * 2] * 2
bad[0][0] = 1
print(bad)
```

Answer: _____________

27.
```python
a = [[1], [2]]
b = a.copy()
b.append([3])
print(a, b)
```

Answer: _____________

28.
```python
a = [[1], [2]]
b = a.copy()
b[0].append(9)
print(a, b)
```

Answer: _____________

29.
```python
import copy
a = [[1], [2]]
b = copy.deepcopy(a)
b[0].append(9)
print(a, b)
```

Answer: _____________

30.
```python
m = [[1, 2], [3, 4]]
print(list(zip(*m)))
```

Answer: _____________

31.
```python
m = [[1, 2], [3, 4]]
print([list(col) for col in zip(*m)])
```

Answer: _____________

32.
```python
rows = [[1, 2], [3, 4]]
rows[1][1] = 99
print(rows)
```

Answer: _____________

33.
```python
a = [1, 2, [3, 4]]
print(len(a), len(a[2]))
```

Answer: _____________

34.
```python
a = [[1,2],[3,4],[5,6]]
print(a[2][1], a[-1][-2])
```

Answer: _____________

35.
```python
a = [[1,2],[3,4],[5,6]]
print(a[-2:])
```

Answer: _____________

36.
```python
a = ['banana', 'an', 'cherry']
print(sorted(a, key=len))
```

Answer: _____________

37.
```python
a = ['banana', 'an', 'cherry']
print(sorted(a, key=len, reverse=True))
```

Answer: _____________

38.
```python
a = ['Alice', 'alice', 'Bob']
a.sort(key=str.lower)
print(a)
```

Answer: _____________

39.
```python
a = [(1, 'b'), (1, 'a'), (2, 'c')]
print(sorted(a))
```

Answer: _____________

40.
```python
a = [(1, 'b'), (1, 'a'), (2, 'c')]
print(sorted(a, key=lambda x: (x[0], x[1])))
```

Answer: _____________

41.
```python
a = [3, 1, 2]
a.sort()
print(a is None)
```

Answer: _____________

42.
```python
a = [3, 1, 2]
print(sorted(a))
print(a)
```

Answer: _____________

43.
```python
a = [1, 2, 3]
b = [10, 20]
print(list(zip(a, b)))
```

Answer: _____________

44.
```python
from itertools import zip_longest
a = [1, 2, 3]
b = [10, 20]
print(list(zip_longest(a, b, fillvalue=0)))
```

Answer: _____________

45.
```python
a = ['x', 'y', 'z']
print(list(enumerate(a, start=1)))
```

Answer: _____________

46.
```python
a = ['a', 'b', 'c']
print('-'.join(a))
```

Answer: _____________

47.
```python
a = [1, 2, 3]
print(a.__contains__(2), a.__contains__(9))
```

Answer: _____________

48.
```python
a = []
try:
    a.pop()
except Exception as e:
    print(type(e).__name__)
```

Answer: _____________

49.
```python
a = [1, 2, 3]
try:
    a.remove(9)
except Exception as e:
    print(type(e).__name__)
```

Answer: _____________

50.
```python
a = [1, 2, 3]
print(a[slice(0, 3, 2)])
```

Answer: _____________

### MCQ Theory (50)

1. List comprehension primarily creates:
```text
A) new list
B) tuple
C) set only
D) generator only
```

2. Generator expression syntax:
```text
A) (x for x in data)
B) [x for x in data]
C) {x for x in data}
D) <x for x in data>
```

3. Comprehension with `if` performs:
```text
A) filtering
B) sorting
C) copying deep
D) grouping dict
```

4. Comprehension expression part performs:
```text
A) mapping/transformation
B) deletion
C) aliasing
D) hashing
```

5. Nested comprehension flatten order typically:
```text
A) for row in m for x in row
B) for x in row for row in m only
C) flatten(m)
D) m.flat()
```

6. `map` in Python 3 returns:
```text
A) iterator
B) list
C) tuple
D) set
```

7. `filter` in Python 3 returns:
```text
A) iterator
B) list
C) dict
D) string
```

8. `list(map(...))` is used to:
```text
A) materialize iterator
B) deep copy list
C) sort values
D) remove duplicates
```

9. `any()` returns True if:
```text
A) at least one truthy item
B) all items truthy
C) list non-empty only
D) all zeros
```

10. `all()` returns True if:
```text
A) all items truthy
B) at least one truthy
C) non-empty only
D) items sorted
```

11. `enumerate(lst)` yields:
```text
A) index-value pairs
B) values only
C) indices only
D) key-value dict pairs
```

12. `enumerate(lst, start=1)` changes:
```text
A) first index value
B) list elements
C) list length
D) sort order
```

13. `zip(a,b)` stops at:
```text
A) shortest input
B) longest input
C) raises mismatch error
D) pads with None by default
```

14. `zip_longest` from itertools allows:
```text
A) padding unequal lengths
B) sorting zipped output
C) index lookup
D) deep copy
```

15. `*` unpack in list literal `[ *a, *b ]` means:
```text
A) merge iterables into new list
B) multiply list
C) deep copy
D) sort combine
```

16. Star unpack assignment `first,*mid,last` gives:
```text
A) middle as list
B) middle as tuple always
C) syntax error
D) no first value
```

17. `sorted(iterable)` accepts:
```text
A) any iterable
B) list only
C) tuple only
D) set disallowed
```

18. `key=` in sort should return:
```text
A) comparison key per item
B) bool only
C) index only
D) None always
```

19. `reverse=True` with sort means:
```text
A) descending by key
B) in-place reverse method call
C) dedupe
D) unstable sort
```

20. Sort stability means:
```text
A) equal keys keep relative order
B) random tie order
C) reverse only
D) no key needed
```

21. `lambda x: x[1]` in sorting tuples means:
```text
A) sort by second item
B) sort by first item
C) sort by tuple length
D) filter tuples
```

22. `str.lower` as sort key enables:
```text
A) case-insensitive ordering
B) numeric sort
C) reverse sort only
D) dedupe
```

23. `a.copy()` on nested list is:
```text
A) shallow copy
B) deep copy
C) alias
D) immutable copy
```

24. `copy.deepcopy(a)` ensures:
```text
A) independent nested objects
B) same nested refs
C) sort order preserved only
D) faster aliasing
```

25. `is` checks:
```text
A) object identity
B) value equality
C) type compatibility
D) hash equality
```

26. `==` for lists checks:
```text
A) element-wise equality
B) identity only
C) length only
D) address only
```

27. `a += [x]` for list typically:
```text
A) mutates existing list
B) always creates new object
C) removes x
D) sorts list
```

28. `a = a + [x]` typically:
```text
A) creates new list object
B) must mutate same object
C) is invalid
D) returns None
```

29. `del a[:]` effect:
```text
A) clear contents in-place
B) delete variable only
C) return new empty list
D) deep delete nested refs
```

30. `slice(1,5,2)` can be applied as:
```text
A) a[slice(1,5,2)]
B) slice(a,1,5,2)
C) a.slice(1,5,2)
D) range only
```

31. `list(dict.fromkeys(lst))` is useful for:
```text
A) order-preserving dedupe
B) random dedupe
C) sorting numeric only
D) deep copy
```

32. `list(set(lst))` may change:
```text
A) element order
B) element values
C) length always same
D) list mutability
```

33. Membership-heavy workflow usually better with:
```text
A) set for lookups
B) list always
C) tuple always
D) string always
```

34. `reversed(lst)` memory profile is:
```text
A) lazy iterator
B) full copied list
C) in-place mutation
D) tuple allocation only
```

35. `.reverse()` return value is:
```text
A) None
B) reversed list
C) iterator
D) bool
```

36. Complexity of `insert(0, x)` in list:
```text
A) O(n)
B) O(1)
C) O(log n)
D) O(n log n)
```

37. Complexity of `append(x)` in list:
```text
A) amortized O(1)
B) O(n) always
C) O(log n)
D) O(n^2)
```

38. Complexity of `pop()` from end:
```text
A) O(1)
B) O(n)
C) O(log n)
D) O(n^2)
```

39. Complexity of `pop(0)` typically:
```text
A) O(n)
B) O(1)
C) O(log n)
D) O(n^2)
```

40. Complexity of `x in list`:
```text
A) O(n)
B) O(1)
C) O(log n)
D) O(n log n)
```

41. `join` on list requires elements of type:
```text
A) str
B) int
C) float
D) any mixed
```

42. `print(*lst)` does:
```text
A) argument unpacking
B) deep copy
C) reverse print
D) dedupe print
```

43. `sum(x*x for x in nums)` uses:
```text
A) generator expression
B) list-only expression
C) map-only expression
D) dict comprehension
```

44. `next((x for x in lst if cond), default)` is commonly used for:
```text
A) first match with fallback
B) all matches
C) sorting
D) copying
```

45. `zip(*matrix)` pattern is used for:
```text
A) transpose-like operation
B) deep copy
C) flatten
D) filter
```

46. `[[0]*m]*n` bug cause:
```text
A) shared inner references
B) slow multiplication
C) bad slicing
D) missing import
```

47. For readable simple transformations, prefer:
```text
A) comprehensions
B) eval
C) global lambdas everywhere
D) recursion only
```

48. When list methods return None, reason is often:
```text
A) in-place mutation design
B) error suppression
C) immutability
D) lazy execution
```

49. Best interview practice for list problems:
```text
A) handle edge cases: empty, one-item, duplicates, nested refs
B) avoid tests
C) use only loops
D) avoid built-ins
```

## Interview Theory (Top 25)

1. Difference between list and tuple in Python?
2. Why are lists mutable and what practical impact does that have?
3. Explain append vs extend with example.
4. When should you use remove vs pop vs del?
5. Why does list.sort() return None?
6. Difference between sorted(lst) and lst.sort().
7. How does slicing work with start:end:step?
8. Why slicing out-of-range does not throw IndexError?
9. Explain negative indexing with examples.
10. What is aliasing in Python lists?
11. Difference between shallow copy and deep copy.
12. Why does [[0]*m]*n cause bugs in nested lists?
13. How to safely create a matrix/list of lists?
14. Complexities of append, pop, insert, remove, in-membership.
15. Why is membership check in list O(n)?
16. How does key-based sorting work?
17. What does sort stability mean and why is it useful?
18. How do you perform multi-key sorting in Python?
19. When to use list comprehension vs map/filter?
20. How does enumerate improve readability?
21. How does zip work with unequal length iterables?
22. How to remove duplicates while preserving order?
23. Common exceptions in list operations and when they happen.
24. How to avoid mutability bugs in function arguments?
25. Best interview-safe checklist for list problems before final submission?

