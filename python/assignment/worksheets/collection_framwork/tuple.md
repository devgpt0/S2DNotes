# Python Tuple Worksheet

Source: python/notes/collection_framework/tuple.md

## Level 1

### Tricky Predict the Output (50)

1.
```python
t = (10, 20, 30, 40, 50)
print(t[0], t[-1])
```

Answer: _____________

2.
```python
t = (10, 20, 30, 40, 50)
print(t[1:4])
```

Answer: _____________

3.
```python
t = (10, 20, 30, 40, 50)
print(t[:3])
```

Answer: _____________

4.
```python
t = (10, 20, 30, 40, 50)
print(t[2:])
```

Answer: _____________

5.
```python
t = (10, 20, 30, 40, 50)
print(t[::-1])
```

Answer: _____________

6.
```python
t = (10, 20, 30, 40, 50)
print(t[::2])
```

Answer: _____________

7.
```python
t = (10, 20, 30, 40, 50)
print(t[1::2])
```

Answer: _____________

8.
```python
t = (10, 20, 30, 40, 50)
print(t[-3:])
```

Answer: _____________

9.
```python
t = (10, 20, 30, 40, 50)
print(t[3:100])
```

Answer: _____________

10.
```python
t = ('a', 'b', 'c', 'd')
print(t[-4], t[-2])
```

Answer: _____________

11.
```python
t = (1, 2, 3, 4, 5, 6)
print(t[5:1:-2])
```

Answer: _____________

12.
```python
t = (1, 2, 3, 4, 5, 6)
print(t[-2::-2])
```

Answer: _____________

13.
```python
t = (1, 2, 3, 4, 5)
print(t[:])
```

Answer: _____________

14.
```python
t = (1, 2, 3, 4, 5)
print(t[::-2])
```

Answer: _____________

15.
```python
t = (1, 2, 3, 4, 5)
print(t[1:1])
```

Answer: _____________

16.
```python
t = 1, 2, 3
print(type(t), t)
```

Answer: _____________

17.
```python
a = (5)
b = (5,)
print(type(a).__name__, type(b).__name__)
```

Answer: _____________

18.
```python
a, b, c = (4, 5, 6)
print(a + b + c)
```

Answer: _____________

19.
```python
t = (1, 2, 3, 4, 5)
a, *mid, b = t
print(a, mid, b)
```

Answer: _____________

20.
```python
t = (1, 2, 3, 4)
*head, tail = t
print(head, tail)
```

Answer: _____________

21.
```python
a, b = 10, 20
a, b = b, a
print(a, b)
```

Answer: _____________

22.
```python
def get_xy():
    return 10, 20
x, y = get_xy()
print(x, y)
```

Answer: _____________

23.
```python
def demo(a, *args, **kwargs):
    print(a)
    print(args)
    print(kwargs)
demo(1, 2, 3, x=4)
```

Answer: _____________

24.
```python
def add3(a, b, c):
    return a + b + c
print(add3(*(1, 2, 3)))
```

Answer: _____________

25.
```python
print((1, 2) + (3, 4))
```

Answer: _____________

26.
```python
print((1, 2) * 3)
```

Answer: _____________

27.
```python
print(2 in (1, 2, 3), 9 not in (1, 2, 3))
```

Answer: _____________

28.
```python
t = (1, 2, 2, 3, 2)
print(t.count(2), t.index(3))
```

Answer: _____________

29.
```python
t = (4, 1, 9, 2)
print(len(t), min(t), max(t), sum(t))
```

Answer: _____________

30.
```python
t = ('Alice', 'Bob', 'Charlie')
print(min(t), max(t))
```

Answer: _____________

31.
```python
t = ([1, 2], [3, 4])
t[0][0] = 99
print(t)
```

Answer: _____________

32.
```python
pairs = [(1, 2), (3, 4)]
for x, y in pairs:
    print(x + y, end=' ')
print()
```

Answer: _____________

33.
```python
point = (0, 7)
match point:
    case (0, y):
        print('Y', y)
    case (x, 0):
        print('X', x)
    case _:
        print('O')
```

Answer: _____________

34.
```python
point = (3, 0)
match point:
    case (0, y):
        print('Y', y)
    case (x, 0):
        print('X', x)
    case _:
        print('O')
```

Answer: _____________

35.
```python
point = (2, 5)
match point:
    case (0, y):
        print('Y', y)
    case (x, 0):
        print('X', x)
    case (x, y):
        print('G', x, y)
```

Answer: _____________

36.
```python
import copy
t1 = (1, [2, 3])
t2 = t1
t3 = copy.copy(t1)
t4 = copy.deepcopy(t1)
t1[1].append(9)
print(t2)
print(t3)
print(t4)
```

Answer: _____________

37.
```python
import copy
t = (1, 2, 3)
print(copy.copy(t) is t)
```

Answer: _____________

38.
```python
t = (1, 2, 3)
print(t[:] is t)
```

Answer: _____________

39.
```python
d = {(1, 2): 'pt'}
print(d[(1, 2)])
```

Answer: _____________

40.
```python
print(hash((1, 2, 3)) is not None)
```

Answer: _____________

41.
```python
t = tuple([1, 2, 3])
print(t)
```

Answer: _____________

42.
```python
t = tuple('abc')
print(t)
```

Answer: _____________

43.
```python
t = (1, 2, 3)
print(sorted(t), type(sorted(t)).__name__)
```

Answer: _____________

44.
```python
t = (1, 2, 3)
print(tuple(reversed(t)))
```

Answer: _____________

45.
```python
t = (1, 2, 3, 4)
print(t[slice(0, 4, 2)])
```

Answer: _____________

46.
```python
t = (1, (2, 3))
a, (b, c) = t
print(a, b, c)
```

Answer: _____________

47.
```python
rgb = (255, 0, 0)
r, g, b = rgb
print(r, g, b)
```

Answer: _____________

48.
```python
a = (1, 2)
b = a
a = a + (3,)
print(a, b)
```

Answer: _____________

49.
```python
t = (1, 2, 3)
for i, v in enumerate(t):
    print(i, v, end=' | ')
print()
```

Answer: _____________

50.
```python
a = (1, 2)
b = [1, 2]
print(type(a).__name__, type(b).__name__)
```

Answer: _____________

### MCQ Theory (50)

1. Tuples in Python are:
```text
A) Ordered and immutable
B) Unordered and mutable
C) Only numeric
D) Key-value only
```

2. Best empty tuple syntax:
```text
A) ()
B) []
C) {}
D) set()
```

3. Single-element tuple is:
```text
A) (5,)
B) (5)
C) [5,]
D) tuple[5]
```

4. `tuple("Ada")` produces:
```text
A) ('A','d','a')
B) ('Ada',)
C) ['A','d','a']
D) TypeError
```

5. Index `-1` means:
```text
A) last element
B) first element
C) middle element
D) invalid index
```

6. Slicing upper bound in `t[1:4]` is:
```text
A) exclusive
B) inclusive
C) random
D) depends on type
```

7. Out-of-range slicing usually:
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

9. `t[0] = 10` on tuple:
```text
A) TypeError
B) ValueError
C) IndexError
D) Works in place
```

10. Tuple supports these direct mutation methods:
```text
A) none
B) append only
C) remove only
D) append and remove
```

11. Tuple methods are mainly:
```text
A) count and index
B) append and extend
C) insert and pop
D) sort and reverse
```

12. `t.index(x)` if not found raises:
```text
A) ValueError
B) IndexError
C) KeyError
D) TypeError
```

13. `+` on tuples does:
```text
A) creates new concatenated tuple
B) mutates left tuple
C) mutates right tuple
D) invalid always
```

14. `* 3` on tuple does:
```text
A) repeats sequence
B) multiplies numeric items only
C) mutates in place
D) sorts
```

15. `a, b = (1, 2, 3)` raises:
```text
A) ValueError
B) IndexError
C) TypeError
D) SyntaxError
```

16. In `a, *mid, b = (1,2,3,4)`, `mid` is:
```text
A) list
B) tuple
C) set
D) dict
```

17. `*args` inside function stores positional args in:
```text
A) tuple
B) list
C) dict
D) set
```

18. `**kwargs` inside function stores keyword args in:
```text
A) dict
B) tuple
C) list
D) set
```

19. `func(*t)` means:
```text
A) unpack tuple into positional args
B) pack args into tuple
C) deep copy tuple
D) reverse tuple
```

20. Tuple can be dict key when:
```text
A) all elements are hashable
B) length is 2
C) contains list
D) sorted only
```

21. Which tuple is unhashable?
```text
A) ([1,2], 3)
B) (1, 2)
C) ('a', 3.14)
D) ((1,2), 3)
```

22. `t[:]` for tuple may:
```text
A) return same object
B) deep copy contents
C) always create new object
D) fail always
```

23. Tuple containing list can:
```text
A) change list contents
B) change tuple length
C) run append on tuple
D) become dict
```

24. `copy.deepcopy` on nested tuple:
```text
A) recursively copies nested objects
B) aliases nested objects
C) is same as assignment
D) mutates source
```

25. `sorted(t)` where `t` is tuple returns:
```text
A) list
B) tuple
C) set
D) iterator
```

26. `reversed(t)` returns:
```text
A) iterator
B) list
C) tuple
D) None
```

27. Which is true for tuple vs list?
```text
A) tuple usually uses less memory
B) tuple always larger memory
C) both always same memory
D) list immutable
```

28. Best use for tuple:
```text
A) fixed records
B) frequent insert/delete
C) in-place sort use cases
D) queue operations
```

29. `tuple([1,2,3])` does:
```text
A) converts iterable to tuple
B) sorts list
C) mutates list to tuple
D) raises error
```

30. `tuple('abc')` gives:
```text
A) ('a','b','c')
B) ('abc',)
C) ['a','b','c']
D) error
```

31. `a, b = b, a` is an example of:
```text
A) tuple packing and unpacking
B) list slicing
C) dict merge
D) set update
```

32. Loop `for x, y in pairs:` requires each element to be:
```text
A) unpackable into two values
B) integer
C) list only
D) dict only
```

33. Pattern `case (0, y)` in `match` means:
```text
A) first value must be 0
B) second must be 0
C) both must be 0
D) tuple length any
```

34. In tuple slicing `t[start:end:step]`, `step=-1` usually means:
```text
A) reverse direction
B) skip nothing
C) deep copy
D) index error
```

35. `len((1,2,3,[4]))` equals:
```text
A) 4
B) 3
C) 5
D) 2
```

36. `min(('Bob','Alice'))` is based on:
```text
A) lexicographic comparison
B) string length
C) random order
D) insertion index
```

37. Tuple literal without parentheses is formed by:
```text
A) commas
B) spaces
C) colons
D) semicolons
```

38. `copy.copy((1,2,3)) is original` is often:
```text
A) True
B) False
C) None
D) Error
```

39. `sum((1,2,3))` returns:
```text
A) 6
B) '123'
C) tuple
D) None
```

40. Which operation is invalid on tuple?
```text
A) t.append(4)
B) t.count(2)
C) t.index(2)
D) 2 in t
```

41. Tuple is categorized as:
```text
A) sequence type
B) mapping type
C) set type
D) numeric type
```

42. If unpacking variable count mismatches values count, you get:
```text
A) ValueError
B) IndexError
C) TypeError
D) KeyError
```

43. Extended unpacking with one starred target:
```text
A) valid
B) invalid always
C) valid only in loops
D) valid only in calls
```

44. `t = (1,2); t += (3,)` results in:
```text
A) new tuple object
B) in-place growth
C) syntax error
D) list conversion
```

45. Tuple used as dictionary key is common for:
```text
A) coordinates
B) mutable logs
C) growing queues
D) dynamic arrays
```

46. Which is not true?
```text
A) tuple methods are many
B) tuple preserves order
C) tuple supports indexing
D) tuple supports slicing
```

47. `print(*t)` with tuple `t` does:
```text
A) argument unpacking in print call
B) mutates tuple
C) deep copy
D) converts to dict
```

48. A tuple can contain mixed types:
```text
A) True
B) False
C) Only in Python 2
D) Only for length 2
```

49. Best phrase for tuple immutability:
```text
A) container immutable, contents may be mutable
B) all nested objects are immutable
C) cannot hold mutable objects
D) always deeply frozen
```

50. In practice, choose list over tuple when:
```text
A) frequent updates are needed
B) fixed shape data
C) hashable key needed
D) read-only record intent
```

## Level 2

### Tricky Questions (50)

1. Create a tuple of three values without parentheses.

Answer: _____________

2. Create an empty tuple and print its type.

Answer: _____________

3. Write the correct syntax for a one-element tuple containing `42`.

Answer: _____________

4. Convert list `[1, 2, 3]` into tuple.

Answer: _____________

5. Convert string `"python"` into tuple of characters.

Answer: _____________

6. Unpack `(10, 20, 30)` into `a, b, c`.

Answer: _____________

7. Unpack `(1, 2, 3, 4, 5)` as `first`, `middle`, `last` using `*`.

Answer: _____________

8. Swap `x` and `y` using tuple unpacking.

Answer: _____________

9. Write a function that returns `x` and `y` as two values.

Answer: _____________

10. Call `f(a,b,c)` using tuple `(1,2,3)` with unpacking.

Answer: _____________

11. Write a function using `*args` that prints the tuple of extras.

Answer: _____________

12. Write a function using `**kwargs` that prints the keyword dict.

Answer: _____________

13. Slice tuple `t` to get elements from index 1 to 3.

Answer: _____________

14. Reverse tuple `t` using slicing syntax.

Answer: _____________

15. Get every second element from tuple `t`.

Answer: _____________

16. Concatenate `(1,2)` and `(3,4)`.

Answer: _____________

17. Repeat `(1,2)` five times.

Answer: _____________

18. Check membership of `"a"` inside tuple `t`.

Answer: _____________

19. Find count of `2` in tuple `t`.

Answer: _____________

20. Find first index of `"x"` in tuple `t`.

Answer: _____________

21. Print `len`, `min`, `max`, `sum` of numeric tuple `t`.

Answer: _____________

22. Demonstrate tuple immutability by attempting assignment at index 0.

Answer: _____________

23. Show inner list mutation inside tuple `([1,2],)`.

Answer: _____________

24. Create dictionary with tuple key `(2,3)` mapping to `"P"`.

Answer: _____________

25. Write code that safely checks if tuple `([1,2],3)` is hashable.

Answer: _____________

26. Loop over `pairs=[(1,'a'),(2,'b')]` and unpack in for-loop.

Answer: _____________

27. Use `match-case` to detect `(0,y)` point on Y-axis.

Answer: _____________

28. Use `match-case` to detect `(x,0)` point on X-axis.

Answer: _____________

29. Add fallback case for general point `(x,y)` in pattern matching.

Answer: _____________

30. Show assignment aliasing for tuple with nested list.

Answer: _____________

31. Show shallow copy behavior using `copy.copy` for tuple with nested list.

Answer: _____________

32. Show deep copy behavior using `copy.deepcopy` for tuple with nested list.

Answer: _____________

33. Show that `copy.copy` may return same object for immutable-only tuple.

Answer: _____________

34. Show that `t[:]` may preserve identity for immutable-only tuple.

Answer: _____________

35. Compare tuple and list memory quickly using `sys.getsizeof`.

Answer: _____________

36. Benchmark tuple vs list iteration quickly using `timeit`.

Answer: _____________

37. Write one practical example where tuple is better than list.

Answer: _____________

38. Write one practical example where list is better than tuple.

Answer: _____________

39. Unpack nested tuple `t = (1, (2, 3))` into `a, b, c`.

Answer: _____________

40. Use `enumerate` to print index-value for tuple `t`.

Answer: _____________

41. Convert reversed iterator of tuple back to tuple.

Answer: _____________

42. Sort tuple values and keep result in a new variable.

Answer: _____________

43. Show a failing unpack due to variable count mismatch and handle exception.

Answer: _____________

44. Build RGB tuple and unpack into `r, g, b`.

Answer: _____________

45. Write code to print first and last element of tuple safely.

Answer: _____________

46. Use slicing object `slice(0,5,2)` on tuple `t`.

Answer: _____________

47. Show tuple packing in function return and unpacking at call site.

Answer: _____________

48. Show `*t` and `**d` together in a function call.

Answer: _____________

49. Demonstrate that tuple supports heterogeneous values.

Answer: _____________

50. Write a one-line mental model comment for packing/unpacking.

Answer: _____________

### MCQ Theory (50)

1. Tuple is best described as:
```text
A) ordered immutable sequence
B) unordered mutable set
C) key-value mapping only
D) numeric scalar type
```

2. Which syntax creates tuple without parentheses?
```text
A) 1, 2, 3
B) [1, 2, 3]
C) {1, 2, 3}
D) <1,2,3>
```

3. Which is one-element tuple?
```text
A) ('x',)
B) ('x')
C) ['x']
D) {'x'}
```

4. Tuple supports:
```text
A) indexing and slicing
B) key lookup only
C) append/pop
D) in-place sort
```

5. Unpacking requires:
```text
A) matching counts unless starred target used
B) always equal counts only
C) no comma on left side
D) function definition only
```

6. In assignment, starred target count allowed is:
```text
A) at most one
B) exactly two
C) unlimited
D) zero only
```

7. `*rest` in unpacking collects into:
```text
A) list
B) tuple
C) set
D) dict
```

8. `return 1, 2` from function returns:
```text
A) tuple-packed values
B) list
C) dict
D) two separate objects with no container
```

9. `a, b = b, a` relies on:
```text
A) packing/unpacking
B) pointer swap only
C) list mutation
D) bitwise ops
```

10. `*args` in params means:
```text
A) pack extra positional args into tuple
B) unpack tuple into params
C) keyword-only capture
D) disallow extras
```

11. `**kwargs` in params means:
```text
A) pack extra keywords into dict
B) unpack dict automatically every time
C) capture positional args
D) make args optional
```

12. In call, `func(*t)` does:
```text
A) unpack iterable as positional args
B) pack into tuple
C) multiply args
D) reverse args
```

13. In call, `func(**d)` does:
```text
A) unpack mapping as keyword args
B) unpack tuple
C) deep copy dict
D) positional expansion
```

14. Tuple methods include:
```text
A) count, index
B) append, pop
C) clear, extend
D) add, discard
```

15. `in` membership on tuple complexity is usually:
```text
A) O(n)
B) O(1)
C) O(log n)
D) O(n log n)
```

16. Hashability rule for tuple keys:
```text
A) all elements must be hashable
B) tuple length must be 2
C) tuple must be sorted
D) tuple must contain only ints
```

17. Tuple containing list is:
```text
A) unhashable
B) hashable
C) hashable if length < 3
D) always invalid object
```

18. Tuple immutability means:
```text
A) structure fixed after creation
B) all nested objects frozen
C) values cannot be read
D) slicing is disabled
```

19. With nested mutable items, tuple can still exhibit:
```text
A) inner mutations
B) syntax errors
C) automatic deep copy
D) conversion to list
```

20. `copy.copy` on immutable-only tuple often:
```text
A) returns same object
B) deep copies internals
C) throws exception
D) converts to list
```

21. `copy.deepcopy` on nested tuple creates:
```text
A) independent nested objects
B) shared nested objects
C) only shallow copy
D) no copy
```

22. `t[:]` for tuple may return same object because:
```text
A) immutability optimization
B) syntax bug
C) garbage collector rule
D) random behavior
```

23. `sorted(tuple_obj)` returns:
```text
A) list
B) tuple
C) set
D) iterator
```

24. `reversed(tuple_obj)` returns:
```text
A) iterator
B) list
C) tuple
D) None
```

25. Pattern matching `case (0, y)` checks:
```text
A) first element equals 0
B) second element equals 0
C) both equal 0
D) no positional relation
```

26. Pattern matching was introduced in:
```text
A) Python 3.10+
B) Python 3.8+
C) Python 2.7+
D) Python 3.9 only
```

27. Tuple vs list for fixed read-only records:
```text
A) tuple preferred
B) list preferred
C) set preferred
D) dict preferred
```

28. Tuple vs list for frequent insert/delete:
```text
A) list preferred
B) tuple preferred
C) set preferred
D) no difference
```

29. `tuple(range(4))` yields:
```text
A) (0, 1, 2, 3)
B) (1, 2, 3, 4)
C) [0, 1, 2, 3]
D) range object unchanged
```

30. Which reflects tuple memory behavior?
```text
A) generally more compact than list
B) always bigger than list
C) same in every case
D) unrelated to container type
```

31. Loop unpacking `for a, b in data:` expects:
```text
A) each item has two unpackable parts
B) each item is int
C) dict keys only
D) list only
```

32. Which statement is true?
```text
A) tuple can hold mixed data types
B) tuple can hold one data type only
C) tuple cannot hold strings
D) tuple cannot hold floats
```

33. Which operation is invalid for tuple `t`?
```text
A) t.append(4)
B) t.count(4)
C) t.index(4)
D) len(t)
```

34. If `t=(1,2,3)`, `t += (4,)` means:
```text
A) new tuple bound to t
B) in-place append
C) error
D) no-op
```

35. `len((1,(2,3),4))` is:
```text
A) 3
B) 4
C) 2
D) 5
```

36. Best key representation for coordinate map is:
```text
A) tuple (x, y)
B) list [x, y]
C) set {x, y}
D) dict {x:y}
```

37. Unpacking error type is usually:
```text
A) ValueError
B) IndexError
C) TypeError
D) KeyError
```

38. Tuple literal is primarily defined by:
```text
A) commas
B) parentheses
C) whitespace
D) quotes
```

39. `print(*t)` uses:
```text
A) argument unpacking
B) tuple packing
C) in-place mutation
D) dict expansion
```

40. Which is a practical tuple use case from notes?
```text
A) coordinates and RGB
B) dynamic queue updates
C) frequent appends
D) matrix row mutation
```

41. Tuple built-ins from notes include:
```text
A) len, min, max, sum
B) append, clear, pop
C) update, items, keys
D) add, discard, union
```

42. `min`/`max` on string tuples compare:
```text
A) lexicographically
B) by insertion order only
C) by length only
D) by hash only
```

43. Best description of tuple copy behavior in notes:
```text
A) shallow copy may share nested mutables
B) copy always deep copies
C) tuples cannot be copied
D) deep copy mutates original
```

44. Notes say tuple protects:
```text
A) structure, not mutable inner state
B) both structure and deep inner state always
C) nothing
D) only numeric elements
```

45. Which aligns with notes for performance?
```text
A) tuple iteration can be slightly faster
B) tuple iteration always much slower
C) tuple cannot be iterated
D) list always faster
```

46. If `a=(1,2); b=a`, then rebinding `a=a+(3,)` makes:
```text
A) b unchanged
B) b automatically updated
C) both errors
D) both None
```

47. Which expression returns tuple slice object result?
```text
A) t[slice(0,4,2)]
B) slice(t,0,4,2)
C) t.slice(0,4,2)
D) tuple.slice(t)
```

48. Correct high-level model from notes:
```text
A) packing: many->one, unpacking: one->many
B) packing and unpacking are identical
C) unpacking only works for lists
D) packing only for dicts
```

49. For fixed API return values, notes recommend:
```text
A) tuple
B) mutable list
C) set
D) generator always
```

50. Most accurate statement:
```text
A) tuple is immutable but can contain mutable members
B) tuple cannot contain lists
C) tuple mutability equals list mutability
D) tuple forbids nested objects
```

## Interview Theory (Top 25)

1. What is a tuple in Python, and how is it different from a list?
2. Why is a comma mandatory for single-element tuples?
3. Explain tuple packing and unpacking with examples.
4. Why does unpacking sometimes raise `ValueError`?
5. What is extended unpacking (`*`) and why does it return a list target?
6. How do negative indexing and slicing work on tuples?
7. Why does tuple slicing not raise IndexError on out-of-range bounds?
8. What are the only two tuple methods and when do you use them?
9. Which built-ins commonly operate on numeric tuples?
10. Explain tuple concatenation and repetition behavior.
11. Why are tuples considered immutable while nested lists inside tuples can still change?
12. What does tuple hashability depend on?
13. Why can `(1, 2)` be a dictionary key but `([1, 2], 3)` cannot?
14. How are `*args` and tuple packing related?
15. How are function call unpacking and `*t` related?
16. How does swapping (`a, b = b, a`) use tuple mechanics?
17. Explain loop unpacking with `for x, y in pairs`.
18. How does structural pattern matching with tuple patterns work?
19. Difference between assignment aliasing, shallow copy, and deep copy for tuples with nested mutables.
20. Why can `copy.copy()` return the same object for immutable-only tuples?
21. Why might `t[:] is t` be `True` for tuples?
22. Tuple vs list memory and iteration performance: practical view.
23. When should you choose tuple over list in real projects?
24. What are common tuple pitfalls in interviews and debugging?
25. Give a concise mental model for tuple packing/unpacking and immutability.
